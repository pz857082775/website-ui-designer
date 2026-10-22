#!/usr/bin/env python3
"""
rag.py — UI 知识库检索（检索增强生成，零依赖）

作用：生成提示词之前，先从"规范文件 + 知识卡"里检索出相关条款，
      把「必须遵守 / 明确禁止 / 参考依据」注入提示词，避免模型随意发挥。

用法：
    python scripts/rag.py index                        # 建索引（规范或知识卡变更后重建）
    python scripts/rag.py query "后台首页 KPI 卡怎么排"
    python scripts/rag.py query "页面太挤了" --top 5
    python scripts/rag.py query "玻璃拟态导航" --platform h5 --format prompt
    python scripts/rag.py query "强调色" --type P --kind card --format json
    python scripts/rag.py stats

参数说明：
    --top N          返回条数，默认 8
    --kind           过滤：card（知识卡）| ref（规范文件）
    --type           过滤知识卡类型：P 参数 / M 手法 / A 反例 / J 判断
    --platform       过滤平台：pc | h5 | miniapp | app
    --format         table（默认）| prompt（可直接注入提示词）| json
    --min-score      低分阈值，默认 1.0；低于此值会提示"无高置信依据"
    --kb             知识卡目录（默认自动找同级 ui-taste-engine/knowledge）
"""
import argparse
import json
import math
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX_DIR = ROOT / ".rag"
INDEX_FILE = INDEX_DIR / "index.json"
CHUNK_MAX = 900
K1, B = 1.5, 0.75

# 领域同义词：把用户的口语映射到规范里的术语
SYNONYMS = {
    "挤": ["间距", "密度", "留白", "行高"],
    "拥挤": ["间距", "密度", "留白"],
    "土": ["饱和度", "配色", "色相"],
    "丑": ["配色", "层级", "间距"],
    "高级": ["留白", "衬线", "低饱和", "字距"],
    "干净": ["留白", "极简", "分隔线"],
    "重点": ["层级", "强调色", "字号"],
    "看不清": ["对比度", "字号"],
    "ai味": ["反例", "套路", "集群", "模板"],
    "ai感": ["反例", "套路", "集群", "模板"],
    "模板感": ["反例", "套路", "集群"],
    "动效": ["动画", "缓动", "时长", "gsap"],
    "卡": ["卡片", "组件"],
    "按钮": ["主按钮", "cta", "强调色"],
    "表格": ["行高", "对齐", "数字", "徽章"],
    "渐变": ["背景", "装饰"],
    "手机": ["h5", "移动", "安全区", "热区"],
    "小程序": ["rpx", "tabbar", "分包"],
    "app": ["安全区", "导航", "手势"],
    "复刻": ["克隆", "取样", "像素"],
    "改版": ["美化", "审计", "诊断"],
}

STOP = set("的 了 和 与 及 或 是 在 有 我 你 他 它 这 那 个 们 吗 呢 吧 啊 要 想 让 把 被 对 从 到 就 都 也 很 更 最 一下 一个 什么 怎么 如何".split())


def norm_text(s: str) -> str:
    return s.replace("\ufeff", "").strip()


def tokenize(s: str):
    s = norm_text(s).lower()
    toks = []
    for w in re.findall(r"[a-z][a-z0-9\-\.]{1,}", s):
        toks.append(w)
    for seg in re.findall(r"[\u4e00-\u9fff]+", s):
        if len(seg) == 1:
            toks.append(seg)
            continue
        toks.extend(seg[i:i + 2] for i in range(len(seg) - 1))
    return [t for t in toks if t not in STOP and len(t) >= 1]


def split_front_matter(text: str):
    m = re.match(r"^\s*---\s*\n(.*?)\n---\s*\n?(.*)$", text, re.S)
    if not m:
        return {}, text
    meta, cur = {}, None
    for line in m.group(1).splitlines():
        if line.lstrip().startswith("- "):
            if cur:
                meta.setdefault(cur, []).append(line.strip()[2:].strip().strip('"'))
            continue
        mm = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
        if not mm:
            continue
        k, v = mm.group(1), mm.group(2).strip().strip('"')
        if not v:
            meta[k] = []
            cur = k
        else:
            cur = None
            meta[k] = v
    return meta, m.group(2)


def chunk_markdown(body: str, max_len=CHUNK_MAX):
    """按 ## / ### 标题切块，过长的块按段落再切。"""
    parts = re.split(r"\n(?=#{2,3}\s)", body)
    out = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        m = re.match(r"^(#{2,3})\s*(.+)", part)
        heading = m.group(2).strip() if m else "（正文）"
        text = part
        while len(text) > max_len:
            cut = text.rfind("\n\n", 0, max_len)
            cut = cut if cut > 200 else max_len
            out.append((heading, text[:cut].strip()))
            text = text[cut:].lstrip()
        if text.strip():
            out.append((heading, text.strip()))
    return out


def find_kb_dir(explicit=None):
    if explicit:
        return Path(explicit)
    env = Path.home() / ".workbuddy" / "skills" / "ui-taste-engine" / "knowledge"
    if env.exists():
        return env
    local = ROOT.parent / "ui-taste-engine" / "knowledge"
    return local if local.exists() else None


def build_docs(kb_dir=None):
    docs = []

    # 规范文件
    for f in sorted((ROOT / "references").glob("*.md")):
        meta, body = split_front_matter(f.read_text(encoding="utf-8"))
        for heading, text in chunk_markdown(body):
            docs.append({
                "kind": "ref", "source": f"references/{f.name}", "id": f.stem,
                "title": f.stem, "heading": heading, "text": text,
                "scope": "", "platform": "", "confidence": 3,
                "tokens": tokenize(heading + " " + text),
            })

    # 知识卡
    kb = find_kb_dir(kb_dir)
    if kb and kb.exists():
        for f in sorted(kb.rglob("*.md")):
            if f.parent == kb:
                continue
            meta, body = split_front_matter(f.read_text(encoding="utf-8"))
            if not meta.get("id"):
                continue
            for heading, text in chunk_markdown(body):
                docs.append({
                    "kind": "card", "source": f"knowledge/{f.parent.name}/{f.name}", "id": str(meta.get("id")),
                    "title": str(meta.get("title", "")), "heading": heading, "text": text,
                    "scope": str(meta.get("scope", "")),
                    "platform": ",".join(meta.get("platform", []) if isinstance(meta.get("platform"), list) else [str(meta.get("platform", ""))]),
                    "confidence": int(str(meta.get("confidence", 3)).strip() or 3),
                    "type": str(meta.get("type", "")),
                    "applies_to": str(meta.get("applies_to", "")),
                    "tokens": tokenize(f"{meta.get('title','')} {meta.get('applies_to','')} {heading} {text}"),
                })
    return docs


def cmd_index(args):
    docs = build_docs(args.kb)
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    n = len(docs)
    df = Counter()
    for d in docs:
        df.update(set(d["tokens"]))
    avgdl = sum(len(d["tokens"]) for d in docs) / max(n, 1)
    payload = {"built_at": date.today().isoformat(), "n": n, "avgdl": avgdl,
               "df": dict(df), "docs": docs}
    INDEX_FILE.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    cards = sum(1 for d in docs if d["kind"] == "card")
    print(f"索引完成：{n} 个片段（规范 {n - cards} / 知识卡 {cards}）")
    print(f"词表 {len(df)} 项，平均长度 {avgdl:.1f}")
    print(f"文件：{INDEX_FILE.relative_to(ROOT)}")
    return 0


def load_index():
    if not INDEX_FILE.exists():
        print("尚未建索引，先运行：python scripts/rag.py index")
        sys.exit(1)
    return json.loads(INDEX_FILE.read_text(encoding="utf-8"))


def expand(query: str):
    q = norm_text(query).lower()
    extra = []
    for k, vs in SYNONYMS.items():
        if k in q:
            extra.extend(vs)
    return tokenize(q) + tokenize(" ".join(extra))


def bm25(qtoks, idx):
    docs, df, avgdl, n = idx["docs"], idx["df"], idx["avgdl"], idx["n"]
    qset = Counter(qtoks)
    scored = []
    for d in docs:
        tf = Counter(d["tokens"])
        dl = max(len(d["tokens"]), 1)
        s = 0.0
        for t, qn in qset.items():
            if t not in tf:
                continue
            idf = math.log(1 + (n - df.get(t, 0) + 0.5) / (df.get(t, 0) + 0.5))
            s += qn * idf * (tf[t] * (K1 + 1)) / (tf[t] + K1 * (1 - B + B * dl / avgdl))
        if s <= 0:
            continue
        # 标题命中加权
        head = d.get("heading", "") + " " + d.get("title", "")
        ht = set(tokenize(head))
        s *= 1 + 0.5 * len(ht & set(qset))
        # 知识卡置信度加权
        if d["kind"] == "card":
            s *= 1 + 0.06 * (int(d.get("confidence", 3)) - 3)
        scored.append((s, d))
    scored.sort(key=lambda x: -x[0])
    # 同一张卡只保留最高分片段；同一来源最多 2 条，保证结果多样
    seen_key, seen_src, dedup = set(), Counter(), []
    for sc, d in scored:
        key = (d["kind"], d["id"]) if d["kind"] == "card" else (d["source"], d["heading"])
        if key in seen_key:
            continue
        if seen_src[d["source"]] >= 2:
            continue
        seen_key.add(key)
        seen_src[d["source"]] += 1
        dedup.append((sc, d))
    return dedup


def filter_docs(scored, kind, typ, platform):
    out = []
    for s, d in scored:
        if kind and d["kind"] != kind:
            continue
        if typ and str(d.get("type", "")).upper() != typ.upper():
            continue
        if platform:
            pf = (d.get("platform") or "").lower()
            if pf and "all" not in pf and platform.lower() not in pf:
                continue
        out.append((s, d))
    return out


def render_prompt(hits, query, low):
    lines = [f"### 知识检索结果（针对：{query}）", ""]
    cards = [h for h in hits if h[1]["kind"] == "card"]
    refs = [h for h in hits if h[1]["kind"] == "ref"]
    hard = [c for c in cards if str(c[1].get("type", "")).upper() in ("P", "M", "J")]
    bans = [c for c in cards if str(c[1].get("type", "")).upper() == "A"]

    lines.append("**一、必须遵守（来自知识卡）**")
    if hard:
        for s, d in hard:
            snippet = re.sub(r"\s+", " ", d["text"])[:90]
            lines.append(f"- [{d['id']}｜置信 {d.get('confidence')}｜适用 {d.get('applies_to') or d.get('scope')}] "
                         f"{d['title']} —— {snippet}")
    else:
        lines.append("- （无命中的知识卡，请按通用规范处理）")

    lines.append("")
    lines.append("**二、明确禁止（来自反例库）**")
    if bans:
        for s, d in bans:
            lines.append(f"- [{d['id']}] {d['title']}")
    else:
        lines.append("- （无反例命中）")

    lines.append("")
    lines.append("**三、参考依据（规范片段，按需引用）**")
    for s, d in refs[:6]:
        snippet = re.sub(r"\s+", " ", d["text"])[:180]
        lines.append(f"- {d['source']} › {d['heading']}：{snippet}…")

    lines.append("")
    lines.append("**四、边界声明**")
    if low:
        lines.append("- 本次检索**无高置信命中**：相关细节属于推断，输出时必须标注“以下为推断”，"
                     "不得当作既定规范。")
    else:
        lines.append("- 以上为知识库内的依据；未出现在此处的细节按通用规范处理，并在输出中标注来源或推断性质。")
    return "\n".join(lines)


def cmd_query(args):
    idx = load_index()
    qtoks = expand(args.query)
    if not qtoks:
        print("查询为空")
        return 1
    hits = filter_docs(bm25(qtoks, idx), args.kind, args.type, args.platform)
    hits = [h for h in hits if h[0] >= 0.2][: args.top]
    low = (not hits) or (hits[0][0] < args.min_score)

    if args.format == "json":
        print(json.dumps([{"score": round(s, 3), "kind": d["kind"], "id": d["id"],
                           "heading": d["heading"], "source": d["source"],
                           "confidence": d.get("confidence")} for s, d in hits],
                         ensure_ascii=False, indent=2))
        return 0

    if args.format == "prompt":
        print(render_prompt(hits, args.query, low))
        return 0

    print(f"查询：{args.query}    命中 {len(hits)} 条（词元 {len(qtoks)}）\n")
    if not hits:
        print("无命中。按通用规范处理，并在输出中标注为推断，不得编造依据。")
        return 0
    for i, (s, d) in enumerate(hits, 1):
        tag = d["kind"] == "card" and f"{d['id']}·{d.get('type')}" or d["source"].split("/")[-1]
        print(f"{i:2}. [{s:5.2f}] {tag:<18} {d['heading'][:40]:<40} {d['source']}")
    if low:
        print("\n提示：最高分低于阈值，视为无高置信依据——细节属推断，输出需标注。")
    return 0


def cmd_stats(args):
    idx = load_index()
    docs = idx["docs"]
    cards = [d for d in docs if d["kind"] == "card"]
    refs = [d for d in docs if d["kind"] == "ref"]
    print("索引状态")
    print("-" * 36)
    print(f"构建日期      {idx['built_at']}")
    print(f"片段总数      {idx['n']}（规范 {len(refs)} / 知识卡 {len(cards)}）")
    print(f"词表大小      {len(idx['df'])}")
    print(f"平均片段长度  {idx['avgdl']:.1f} 词元")
    by_type = Counter(d.get("type") for d in cards)
    print("知识卡类型    " + " / ".join(f"{k}:{v}" for k, v in by_type.items() if k))
    srcs = {d["source"] for d in refs}
    print(f"覆盖规范文件  {len(srcs)} 份")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="UI 知识库检索（RAG）")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("index"); p.add_argument("--kb", default=None); p.set_defaults(fn=cmd_index)
    p = sub.add_parser("query")
    p.add_argument("query")
    p.add_argument("--top", type=int, default=8)
    p.add_argument("--kind", choices=["card", "ref"])
    p.add_argument("--type", choices=["P", "M", "A", "J", "p", "m", "a", "j"])
    p.add_argument("--platform", choices=["pc", "h5", "miniapp", "app"])
    p.add_argument("--format", choices=["table", "prompt", "json"], default="table")
    p.add_argument("--min-score", type=float, default=1.0)
    p.set_defaults(fn=cmd_query)
    p = sub.add_parser("stats"); p.set_defaults(fn=cmd_stats)
    a = ap.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())

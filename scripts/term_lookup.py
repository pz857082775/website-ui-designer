#!/usr/bin/env python3
"""
term_lookup.py — 按用户原话反查 UI 术语（零依赖）

为什么：用户说"太挤了/底下挡着了/没重点"，需要立刻翻译成术语 + 参数。
检索主键是"用户会怎么说"，不是"术语叫什么"。

用法：
    python scripts/term_lookup.py "太挤了"
    python scripts/term_lookup.py "按钮被黑条挡住" --top 3
    python scripts/term_lookup.py --list
    python scripts/term_lookup.py "卡" --json
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GLOSSARY = ROOT / "library" / "ui-glossary.md"

# 症状 → 应优先命中的术语（用户描述的是症状，术语描述的是成因）
SYMPTOM_BOOST = {
    "挡住": ["安全区", "固定层", "层级", "胶囊避让"],
    "遮挡": ["安全区", "固定层", "层级"],
    "盖住": ["固定层", "层级"],
    "点不到": ["安全区", "触控目标", "固定层"],
    "挤": ["间距系统", "表格密度", "行高", "空区域"],
    "密密麻麻": ["行高", "表格密度"],
    "太空": ["空区域", "间距系统"],
    "土": ["中性阶", "饱和度", "色彩令牌"],
    "脏": ["中性阶", "饱和度"],
    "花": ["强调色", "色彩令牌"],
    "看不清": ["对比度", "中性阶", "遮罩"],
    "太淡": ["对比度", "中性阶"],
    "没重点": ["视觉焦点", "字阶"],
    "不知道看哪": ["视觉焦点"],
    "乱": ["栅格", "间距系统"],
    "卡": ["过渡", "骨架屏", "列表"],
    "白屏": ["骨架屏", "空状态"],
    "对不齐": ["栅格", "等宽数字"],
    "生硬": ["缓动", "过渡"],
}


def parse_entries(path: Path):
    if not path.exists():
        return []
    rows, category = [], ""
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            category = line[3:].strip()
            continue
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 4:
            continue
        if set(cells[0]) <= set("-: ") or cells[0] in ("术语", "状态"):
            continue
        term, alias, definition, params = cells[0], cells[1], cells[2], cells[3]
        term_cn = "".join(re.findall(r"[\u4e00-\u9fff]+", re.split(r"[（(]", term)[0]))
        term_en = " ".join(re.findall(r"[A-Za-z][A-Za-z\- ]+", term)).strip()
        rows.append({
            "category": category, "term": term, "term_cn": term_cn, "term_en": term_en,
            "alias": alias, "definition": definition, "params": params,
        })
    return rows


def bigrams(s: str):
    s = re.sub(r"[\s，。、；：！？,.;:!?（）()\"'“”‘’]", "", s)
    return {s[i:i + 2] for i in range(len(s) - 1)} | ({s} if len(s) <= 3 else set())


def score(entry, query):
    q = query.strip()
    hits, s = [], 0.0
    for idx, field in enumerate((entry["alias"], entry["term_cn"], entry["term_en"])):
        weight = 1.0 if idx == 0 else 0.45   # 术语名命中降权，避免"按钮"抢过"安全区"
        if not field:
            continue
        parts = re.split(r"[、/·,，\s]+", field.replace("""
""", ""))
        for p in parts:
            p = p.strip()
            if not p:
                continue
            if q in p or (p in q and len(p) >= 2):
                hits.append(p)
                # 别名命中权重最高：用户原话是检索主键
                s += (8 if q == p else (6 if len(p) >= 3 else 3)) * weight
    if not hits:
        qb, eb = bigrams(q), bigrams(entry["alias"] + entry["definition"])
        overlap = qb & eb
        if overlap:
            s += len(overlap) / max(len(qb), 1) * 4
    return s, hits


def main():
    ap = argparse.ArgumentParser(description="按用户原话反查 UI 术语")
    ap.add_argument("query", nargs="?", default="")
    ap.add_argument("--top", type=int, default=3)
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    entries = parse_entries(GLOSSARY)
    if not entries:
        print(f"未找到词库：{GLOSSARY}")
        return 1

    if args.list:
        from collections import Counter
        c = Counter(e["category"] for e in entries)
        print(f"共 {len(entries)} 条，{len(c)} 类：")
        for k, v in c.items():
            print(f"  {k:<16} {v} 条")
        return 0

    if not args.query:
        print('用法：python scripts/term_lookup.py "太挤了"')
        return 1

    scored = []
    for e in entries:
        s, hits = score(e, args.query)
        for kw, terms in SYMPTOM_BOOST.items():
            if kw in args.query and e["term_cn"] in terms:
                rank = terms.index(e["term_cn"])
                s += max(8 - rank * 2, 2)      # 越靠前越可能是根因
                hits.append("症状:" + kw)
        if s > 0:
            scored.append((s, hits, e))
    scored.sort(key=lambda x: -x[0])
    top = scored[: args.top]

    if args.json:
        print(json.dumps([{
            "score": round(s, 2), "term": e["term"], "category": e["category"],
            "definition": e["definition"], "params": e["params"], "matched": hits,
        } for s, hits, e in top], ensure_ascii=False, indent=2))
        return 0

    if not top:
        print(f'未命中："{args.query}"')
        print("→ 换种说法再查（如「太挤」→「间距」、「挡住」→「遮挡」、「看不清」→「对比度」）")
        return 0

    print(f'查询：{args.query}　命中 {len(scored)} 条，取前 {len(top)}\n')
    for i, (s, hits, e) in enumerate(top, 1):
        print(f"{i}. 【{e['term']}】{e['category']}")
        print(f"   定义：{e['definition']}")
        print(f"   参数：{e['params']}")
        if hits:
            print(f"   命中：{'、'.join(dict.fromkeys(hits))}")
        print()
    print("提示：回答时先给术语 + 一句人话解释，再落到参数；一次最多 1–3 条。")
    return 0


if __name__ == "__main__":
    sys.exit(main())

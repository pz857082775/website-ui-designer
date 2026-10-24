#!/usr/bin/env python3
"""
audit_contrast.py — 配色可读性审计（WCAG 2.1，零依赖）

检查：
1. 浅色与深色两套令牌中，「背景 × 文字」组合的对比度
2. CSS 规则里同时出现 color + background 的字面色值组合
3. 是否存在深色模式定义（缺失则警告）

用法：
    python scripts/audit_contrast.py tests/*.html
    python scripts/audit_contrast.py page.html --verbose
    python scripts/audit_contrast.py page.html --min 4.5 --ui-min 3

退出码：0 = 通过；1 = 存在低于阈值的组合
"""
import argparse
import re
import sys
from pathlib import Path

HEX = re.compile(r"#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b")
VAR = re.compile(r"--([a-zA-Z0-9\-_]+)\s*:\s*([^;{}]+);")
RULE = re.compile(r"\{([^{}]*)\}")

BG_HINTS = ("bg", "background", "surface", "card", "panel", "page", "sheet", "elev")
FG_HINTS = ("ink", "text", "fg", "foreground", "label", "body")


def is_bg(name: str) -> bool:
    return any(re.search(rf"(^|[-_]){h}([-_]|$)", name.lower()) for h in BG_HINTS)


def is_fg(name: str) -> bool:
    return any(re.search(rf"(^|[-_]){h}([-_]|$)", name.lower()) for h in FG_HINTS)


def hex_to_rgb(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def luminance(rgb):
    def ch(c):
        c /= 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(x) for x in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(c1, c2):
    l1, l2 = luminance(hex_to_rgb(c1)), luminance(hex_to_rgb(c2))
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def first_hex(value):
    m = HEX.search(value or "")
    return "#" + m.group(1) if m else None


def blocks(css):
    """返回 [(选择器, 块内容)]，只做一层，够用。"""
    out = []
    for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", css):
        out.append((m.group(1).strip(), m.group(2)))
    return out


def collect_vars(block_text):
    out = {}
    for name, val in VAR.findall(block_text):
        h = first_hex(val)
        if h:
            out[name] = h
    return out


def audit_html(path: Path, min_text=4.5, min_ui=3.0, verbose=False, explicit=None):
    html = path.read_text(encoding="utf-8", errors="replace")
    styles = "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", html, re.S))
    problems, notes, pairs = [], [], []

    # --- 1. 令牌模式 ---
    root_vars, dark_vars = {}, {}
    for sel, body in blocks(styles):
        v = collect_vars(body)
        if not v:
            continue
        if "prefers-color-scheme: dark" in sel or re.search(r"\[data-theme=[\"']?dark", sel) or ".dark" in sel:
            dark_vars.update(v)
        elif ":root" in sel or "html" == sel.strip() or "body" == sel.strip():
            root_vars.update(v)

    has_dark = bool(dark_vars) or "prefers-color-scheme" in styles
    if not has_dark:
        notes.append("未检测到深色模式定义（建议补 [data-theme=dark] 或 prefers-color-scheme）")

    def check_theme(vs, label):
        if not vs:
            return
        # 任何以 -ink 结尾的变量都是"压在某色底上的文字"，与它的底色单独配对
        for name, val in list(vs.items()):
            if not name.endswith("-ink"):
                continue
            base = name[:-4]
            if base in vs:
                r = ratio(vs[base], val)
                pairs.append((label, f"--{base}", f"--{name}", r))
                if r < min_text:
                    problems.append(
                        f"[{label}] --{name} on --{base} = {r:.2f}:1 < {min_text}:1（按钮文字不可读）")
        # 只把中性表面当作正文背景；彩色底只与其专属 -ink 配对（上面已处理）
        bgs = {k: v for k, v in vs.items() if is_bg(k)}
        fgs = {k: v for k, v in vs.items()
               if is_fg(k) and k not in bgs and not k.endswith("-ink")}
        for bn, bv in bgs.items():
            for fn, fv in fgs.items():
                r = ratio(bv, fv)
                pairs.append((label, f"--{bn}", f"--{fn}", r))
                if r < min_text:
                    problems.append(
                        f"[{label}] --{fn} on --{bn} = {r:.2f}:1 < {min_text}:1  （文字不可读）")

    check_theme(root_vars, "浅色")
    check_theme(dark_vars, "深色")

    # 显式配对：用于自定义命名的令牌（如 --paper / --dark-ink）
    if explicit:
        merged = dict(root_vars); merged.update(dark_vars)
        for fg_name, bg_name in explicit:
            fv, bv = merged.get(fg_name), merged.get(bg_name)
            if not (fv and bv):
                notes.append(f"[显式配对] 找不到 {fg_name} 或 {bg_name}")
                continue
            r = ratio(bv, fv)
            pairs.append(("显式", f"--{bg_name}", f"--{fg_name}", r))
            if r < min_text:
                problems.append(f"[显式] --{fg_name} on --{bg_name} = {r:.2f}:1 < {min_text}:1")

    # --- 2. 同规则内的字面 color + background ---
    for sel, body in blocks(styles):
        if "color:" not in body:
            continue
        m_color = re.search(r"(?<!background-)(?<!border-)color\s*:\s*([^;]+)", body)
        m_bg = re.search(r"background(?:-color)?\s*:\s*([^;]+)", body)
        if not (m_color and m_bg):
            continue
        c1, c2 = first_hex(m_color.group(1)), first_hex(m_bg.group(1))
        if not (c1 and c2):
            continue
        r = ratio(c1, c2)
        pairs.append(("规则", f"{c2}", f"{c1}", r))
        if r < min_text:
            problems.append(f"[规则 {sel[:40]}] 文字 {c1} on 背景 {c2} = {r:.2f}:1")

    # --- 3. 明显风险：文字用浅色调 + 软底徽章 ---
    for sel, body in blocks(styles):
        if re.search(r"filter|gradient|backdrop", body):
            continue
        m_color = re.search(r"(?<!background-)color\s*:\s*(rgba?\([^)]*\)|#[0-9a-fA-F]{3,6})", body)
        m_bg = re.search(r"background(?:-color)?\s*:\s*rgba\(\s*255\s*,\s*255\s*,\s*255\s*,\s*\.?0?\.\d+", body)
        if m_color and m_bg:
            notes.append(f"[疑似] {sel[:40]} 半透明白底 + 字面色，请人工确认对比")

    return problems, notes, pairs, (root_vars, dark_vars)


def main():
    ap = argparse.ArgumentParser(description="配色可读性审计")
    ap.add_argument("files", nargs="+")
    ap.add_argument("--min", type=float, default=4.5, help="正文阈值，默认 4.5")
    ap.add_argument("--ui-min", type=float, default=3.0, help="UI 元素阈值，默认 3.0")
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--pairs", default="", help='显式配对，如 "--ink:--paper,--dark-ink:--dark"')
    args = ap.parse_args()

    files = []
    for f in args.files:
        p = Path(f)
        files.extend(sorted(Path().glob(f)) if any(c in f for c in "*?") else [p])

    explicit = []
    for chunk in args.pairs.split(","):
        chunk = chunk.strip()
        if ":" in chunk:
            fg, bg = chunk.split(":", 1)
            explicit.append((fg.strip().lstrip("-"), bg.strip().lstrip("-")))

    total_bad = 0
    for f in files:
        if not f.exists():
            print(f"[跳过] {f} 不存在")
            continue
        problems, notes, pairs, _ = audit_html(f, args.min, args.ui_min, args.verbose, explicit)
        total_bad += len(problems)
        status = "FAIL" if problems else "PASS"
        print(f"\n[{status}] {f}")
        if args.verbose:
            for theme, bn, fn, r in pairs:
                flag = "ok " if r >= args.min else "LOW"
                print(f"   {flag} [{theme}] {fn} on {bn}: {r:.2f}:1")
        else:
            worst = min((p[3] for p in pairs), default=0)
            print(f"   检查 {len(pairs)} 组配色，最低 {worst:.2f}:1（阈值 {args.min}）")
        for p in problems:
            print("   违规 " + p)
        for n in notes:
            print("   提示 " + n)

    print(f"\n—— 合计 {total_bad} 处对比度违规 ——")
    print("提示：UI 元素（边框/图标/焦点环）阈值是 3:1，请人工抽查 2-3 处。")
    return 1 if total_bad else 0


if __name__ == "__main__":
    sys.exit(main())

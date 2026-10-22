#!/usr/bin/env python3
"""
preflight.py — 生成的 UI 页面交付前自检

用法：
    python scripts/preflight.py <页面.html> [更多页面...]
    python scripts/preflight.py tests/*.html

退出码：0 = 通过（可能有警告），1 = 有致命问题

检查项（致命 ERROR / 警告 WARN）：
  E1 预隐藏内容但没有 GSAP 存在性守卫（CDN 挂掉 → 页面空白）
  E2 缺少 prefers-reduced-motion 降级
  E3 缺少 viewport meta（移动端不可用）
  E4 使用了第三方图表库 CDN（应内联 SVG）
  W1 出现 emoji 图标（应换 SVG）
  W2 有数字但未启用 tabular-nums
  W3 出现 lorem / 占位文案
  W4 <img> 缺 alt
  W5 动效动布局属性（width/height/top/left 出现在 tween vars 中）
  W6 出现滚动劫持迹象（preventDefault + wheel/touchmove）
"""
import re
import sys
from pathlib import Path

EMOJI = re.compile(
    "[\U0001F300-\U0001FAFF\U0001F600-\U0001F64F\U0001F680-\U0001F6FF"
    "\U00002600-\U000027BF\U0001F1E0-\U0001F1FF\u2b50\u2705\u274c\u2728]"
)


def check(path: Path):
    text = path.read_text(encoding="utf-8", errors="replace")
    errs, warns = [], []

    # E1 预隐藏 + 无守卫
    prehide = re.search(r"\.(js-anim|has-gsap)\s+\.anim\s*\{\s*opacity\s*:\s*0", text)
    guard = re.search(r"if\s*\(\s*[!]?window\.gsap\s*\)", text) or re.search(
        r"if\s*\(\s*window\.gsap\s*\)", text
    )
    if prehide and not guard:
        errs.append("E1 内容被 CSS 预隐藏但无 GSAP 存在性守卫 —— CDN 失败会导致整页空白")
    if prehide and guard:
        warns.append("W0 使用了 CSS 预隐藏（有守卫，可接受；更稳的做法是交给 gsap.from 自己设初始态）")

    # E2 reduced-motion
    if "prefers-reduced-motion" not in text:
        errs.append("E2 缺少 prefers-reduced-motion 降级")

    # E3 viewport
    if 'name="viewport"' not in text:
        errs.append("E3 缺少 viewport meta")

    # E4 图表库 CDN
    for lib in ("chart.js", "echarts", "highcharts", "d3.v", "apexcharts"):
        if lib in text.lower():
            errs.append(f"E4 引用了第三方图表库（{lib}）——应改为内联 SVG")

    # W1 emoji
    emojis = EMOJI.findall(text)
    if emojis:
        uniq = "".join(sorted(set(emojis)))[:12]
        warns.append(f"W1 出现 emoji 字符 {uniq} —— 应替换为 SVG 图标")

    # W2 tabular-nums
    if re.search(r"\d{3,}", text) and "tabular-nums" not in text:
        warns.append("W2 页面含 3 位以上数字但未启用 tabular-nums")

    # W3 占位文案
    if re.search(r"lorem ipsum|Lorem ipsum|占位文字", text):
        warns.append("W3 出现 lorem / 占位文案")

    # W4 img alt
    for m in re.finditer(r"<img\b[^>]*>", text, re.I):
        if "alt=" not in m.group(0).lower():
            warns.append("W4 存在缺少 alt 的 <img>")
            break

    # W5 动画布局属性
    layout_anim = re.search(
        r"gsap\.(?:to|from|fromTo)\([^)]*\{[^}]*\b(?:width|height|top|left|margin)\s*:",
        text,
        re.S,
    )
    if layout_anim:
        warns.append("W5 动画中出现了布局属性（width/height/top/left）—— 应改为 transform")

    # W6 滚动劫持
    if re.search(r"preventDefault\(\)", text) and re.search(r"wheel|touchmove", text):
        warns.append("W6 疑似滚动劫持（preventDefault + wheel/touchmove）")

    return errs, warns


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 1
    files = []
    for a in argv[1:]:
        p = Path(a)
        files.extend(sorted(Path().glob(a)) if any(c in a for c in "*?") else [p])

    total_e = total_w = 0
    for f in files:
        if not f.exists():
            print(f"[SKIP] {f} 不存在")
            continue
        errs, warns = check(f)
        total_e += len(errs)
        total_w += len(warns)
        status = "FAIL" if errs else ("WARN" if warns else "PASS")
        print(f"\n[{status}] {f}")
        for e in errs:
            print(f"   ERROR {e}")
        for w in warns:
            print(f"   warn  {w}")

    print(f"\n—— 合计：{total_e} 个致命问题，{total_w} 个警告 ——")
    return 1 if total_e else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

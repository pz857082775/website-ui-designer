#!/usr/bin/env python3
"""
audit_all.py — 交付前统一闸门（一条命令跑完两类审计）

为什么需要它：preflight 与 audit_contrast 是两个脚本，实际交付时经常只跑一个。
本脚本串起来，给出**单一结论**，并列出必须先修的三处。

用法：
    python scripts/audit_all.py tests/*.html
    python scripts/audit_all.py page.html --skip-contrast
    python scripts/audit_all.py tests/*.html --pairs="--ink:--paper,--dark-ink:--dark"

退出码：0 = 全部通过；1 = 有阻塞项
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PY = sys.executable


def run(cmd):
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


def main():
    ap = argparse.ArgumentParser(description="交付前统一闸门")
    ap.add_argument("files", nargs="+")
    ap.add_argument("--skip-preflight", action="store_true")
    ap.add_argument("--skip-contrast", action="store_true")
    ap.add_argument("--pairs", default="", help="传给 audit_contrast 的显式配对")
    args = ap.parse_args()

    files = []
    for f in args.files:
        p = Path(f)
        files.extend(sorted(Path().glob(f)) if any(c in f for c in "*?") else [p])
    files = [f for f in files if f.suffix.lower() in (".html", ".htm")]

    if not files:
        print("没有找到 HTML 文件")
        return 1

    blockers, warnings = [], []
    report = []

    if not args.skip_preflight:
        code, out = run([PY, str(ROOT / "preflight.py")] + [str(f) for f in files])
        for line in out.splitlines():
            s = line.strip()
            if s.startswith("[FAIL]") or s.startswith("E1") or s.startswith("E2") or s.startswith("E3") \
               or s.startswith("E4") or s.startswith("E5"):
                blockers.append("preflight · " + s)
            elif s.startswith("[PASS]"):
                pass
            elif re.match(r"^\[?W\d", s):
                warnings.append("preflight · " + s)
        m = re.search(r"合计：(\d+) 个致命问题，(\d+) 个警告", out)
        report.append(("preflight（7 类硬伤）", m.group(0) if m else ("FAIL" if code else "PASS")))
        if code != 0 and not m:
            blockers.append("preflight · 执行失败，检查文件路径")

    if not args.skip_contrast:
        cmd = [PY, str(ROOT / "audit_contrast.py")] + [str(f) for f in files]
        if args.pairs:
            cmd.append(f"--pairs={args.pairs}")
        code, out = run(cmd)
        for line in out.splitlines():
            s = line.strip()
            if s.startswith("违规") or s.startswith("[显式]"):
                blockers.append("contrast · " + s)
        m = re.search(r"合计 (\d+) 处对比度违规", out)
        report.append(("contrast（浅/深全配对）", m.group(0) if m else ("FAIL" if code else "PASS")))

    print("\n=== 交付闸门 ===")
    for i, (name, verdict) in enumerate(report, 1):
        print(f"{i}. {name:<24} {verdict}")

    if warnings:
        print(f"\n警告 {len(warnings)} 条（不阻塞，但建议评估）：")
        for w in warnings[:6]:
            print("  - " + w)

    if blockers:
        print(f"\n必须先修 {len(blockers)} 处，前三条：")
        for b in blockers[:3]:
            print("  ! " + b)
        print("\n结论：FAIL —— 修完再交付。")
        return 1

    print(f"\n检查文件 {len(files)} 个 · 阻塞 0 · 警告 {len(warnings)}")
    print("结论：PASS —— 自动项通过。还需人工：15 项检查全 1 + 7 维评分平均 ≥8（见 templates/scorecard.md）。")
    return 0


if __name__ == "__main__":
    sys.exit(main())

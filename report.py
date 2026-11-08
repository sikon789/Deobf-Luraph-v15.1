#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
report.py —— 可读性分析报告生成（多份产物横向对比 + 定性说明）
"""
import sys
import re
import subprocess
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from readability import analyze, score, bar


def samples(t):
    """抽样几段回调，看具体是什么样子"""
    s = Path(t).read_text(encoding="utf-8", errors="ignore")
    # 找一个带 ⚠ 的回调，和一个带真实逻辑的回调
    blocks = []
    for m in re.finditer(r'(\w+):(\w+)\("([^"]+)",[^\n]*\n((?:\t\{1,2\}[^\n]*\n){1,6})', s):
        body = m.group(4)
        blocks.append((m.group(2), m.group(3), body.strip()[:200]))
    return blocks


def main():
    files = sys.argv[1:]
    if not files:
        print("用法: report.py <文件1> <文件2> ...")
        return 1

    data = [(f, analyze(f)) for f in files]
    scored = [(f, d, *score(d)) for f, d in data]

    print("=" * 84)
    print("  反混淆产物可读性分析报告")
    print("=" * 84)
    print()
    print(f"  {'产物':<34}{'字节':>10}{'行数':>8}{'得分':>7}")
    print("  " + "-" * 70)
    for f, d, s, _ in scored:
        nm = Path(f).name
        print(f"  {nm:<34}{d['bytes']:>10,}{d['lines']:>8,}{s:>7}")
    print()

    # 维度矩阵
    print("  ── 维度明细 ──")
    names = [x[0] for x in scored[0][3]]
    print(f"  {'维度':<14}", end="")
    for f, d, s, _ in scored:
        print(f"{Path(f).name[:16]:>18}", end="")
    print()
    print("  " + "-" * 70)
    for i, dim in enumerate(names):
        print(f"  {dim:<14}", end="")
        for f, d, s, detail in scored:
            print(f"{detail[i][1]:>18}", end="")
        print()
    print("  " + "-" * 70)
    print(f"  {'总分':<14}", end="")
    for f, d, s, detail in scored:
        print(f"{s:>18}", end="")
    print()
    print()

    # 关键定性发现
    print("  ── 定性发现 ──")
    for f, d, s, detail in scored:
        nm = Path(f).name
        print(f"\n  【{nm}】")
        omit = d["warn_marks"]
        if omit:
            print(f"    · {omit} 处函数体标注「逻辑缺失 / 未记录」——这是内容缺失，不是排版问题")
        print(f"    · 控制流语句 {d['control']} 个，"
              f"函数 {d['functions']} 个，机名 {d['machine_names']} 个")
        if d["comments"] > 50:
            print(f"    · 有 {d['comments']} 行人工注释 / 章节标题（可读性好，但属人工加工）")
        if d["temp_vars"] > 100:
            print(f"    · {d['temp_vars']} 个临时变量名（v3/v8 这类）——"
                  f"语义完整但原名丢失")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())

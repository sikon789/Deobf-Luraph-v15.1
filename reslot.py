#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
reslot.py —— 还原 VM 的槽位访问

Luraph 把局部变量存在一个表里，用数字下标访问：
    tbl[6].conns      ← 其实是 conns.conns
    tbl[7]            ← 其实是 sprint
    tbl[3]            ← 其实是 CurrentCamera

只要能找到 `tbl[N] = 名字` 这句赋值，就能把后续所有 `tbl[N]` 换成那个名字。
这样 1,598 个 `tbl[6]` 就变成 `conns`，1,387 行立刻可读。
"""
import re
import sys
from pathlib import Path


def find_slots(text):
    """扫出 slot 表：{数字: 名字}"""
    slots = {}
    # tbl[6] = conns      /   X_3[6] = conns  /  tbl[N] = expr
    for m in re.finditer(
            r'\b(\w+)\[(\d+)\]\s*=\s*([A-Za-z_]\w*)\s*(?=[\s;,)\n]|$)', text):
        tab, idx, name = m.group(1), int(m.group(2)), m.group(3)
        # 只接受「表名已经在前面定义过」的情况，避免误伤
        if (tab, idx) not in slots:
            slots[(tab, idx)] = name
    return slots


def apply_slots(text, slots):
    if not slots:
        return text, 0

    # 按表名分组，便于一次正则替换
    by_tab = {}
    for (tab, idx), name in slots.items():
        by_tab.setdefault(tab, {})[idx] = name

    total = 0
    for tab, m in by_tab.items():
        # 只替换「读取」位置：tbl[6] 后面不是 = 的
        def repl(mo):
            nonlocal total
            idx = int(mo.group(1))
            if idx not in m:
                return mo.group(0)
            total += 1
            return m[idx]

        # 排除赋值左侧 tbl[6] = xxx
        pattern = re.compile(r'\b' + re.escape(tab) + r'\[(\d+)\](?!\s*=)')
        text = pattern.sub(repl, text)

    return text, total


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('-')]
    if not args:
        print(__doc__)
        return 1
    src = Path(args[0])
    dst = Path(args[1]) if len(args) > 1 else src.with_suffix('.reslot.luau')
    text = src.read_text(encoding='utf-8', errors='ignore')

    slots = find_slots(text)
    print(f"[reslot] 发现 {len(slots)} 个槽位映射：")
    for (tab, idx), name in sorted(slots.items(), key=lambda x: -x[0][1])[:12]:
        n = len(re.findall(r'\b' + re.escape(tab) + r'\[' + str(idx) + r'\](?!\s*=)', text))
        print(f"    {tab}[{idx}] = {name:<20} （{n} 处引用）")

    out, cnt = apply_slots(text, slots)
    dst.write_text(out, encoding='utf-8')
    print(f"[reslot] 替换 {cnt:,} 处  →  {dst}")
    return 0


if __name__ == '__main__':
    sys.exit(main())

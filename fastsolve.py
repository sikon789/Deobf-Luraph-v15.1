#!/usr/bin/env python3
"""fastsolve.py <target.lua> [outdir]
两段式快速解：
  A) 2 秒：buffer 模拟跑一遍，dump 所有解码后的缓冲区 —— 能拿到外层 loader 解出来的下一层源码
  B) 可选：DEOB_FAST=1 + DEVIRT_TIME_BUDGET 跑 deob.js 做符号执行（慢，但那是唯一的"源码"来源）
只用 A，不碰符号执行。
"""
import os, re, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
LUAU = os.path.join(HERE, 'luraph151_c', 'bin', 'luau')

def run_capture(target, workdir, stub=False, minlen=48):
    runner = os.path.join(workdir, '_runner.lua')
    cmd = [sys.executable, os.path.join(HERE, 'mkfast.py'), target, runner, str(minlen)]
    if stub:
        cmd.append('--stub')
    subprocess.run(cmd, check=True, capture_output=True)
    t0 = time.time()
    with open(os.path.join(workdir, '_out.txt'), 'w') as fh:
        subprocess.run([LUAU, runner], stdout=fh, stderr=subprocess.STDOUT, timeout=300)
    dt = time.time() - t0
    txt = open(os.path.join(workdir, '_out.txt'), encoding='utf-8', errors='replace').read()
    return txt, dt

def read_varint(d, o):
    v, sh = 0, 0
    while o < len(d) and sh < 35:
        b = d[o]; o += 1; v |= (b & 0x7F) << sh; sh += 7
        if not (b & 0x80): break
    return v, o

def bc_strings(data):
    """尽力从 Luau 字节码里抠字符串表；两种 header 长度都试，取解析最干净的。"""
    best = None
    for skip in (2, 3):
        try:
            cnt, o = read_varint(data, skip)
            if not (0 < cnt < 5000): continue
            start, out = o, []
            for _ in range(cnt):
                ln, o = read_varint(data, o)
                if ln < 0 or o + ln > len(data): raise ValueError
                if ln: out.append(data[o:o+ln].decode('utf-8', 'replace'))
                o += ln
            if best is None or o - start > best[0]:
                best = (o - start, out)
        except Exception:
            continue
    return best[1] if best else []

def classify(data):
    if not data:
        return 'empty'
    head = data[:400]
    printable = sum(1 for b in head if 32 <= b < 127 or b in (9, 10, 13))
    ratio = printable / max(1, len(head))
    if ratio > 0.9 and re.match(rb'^\s*(--|return|local|function|\w+\s*=)', head):
        return 'lua-source'
    if data[:3] == b'\x1bLua' or (data[0] < 32 and data[0] > 0 and data[1] < 32):
        return 'bytecode?'
    if ratio > 0.85:
        return 'encoded-ascii'
    return 'binary'

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    target = sys.argv[1]
    outdir = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, 'fast_' + os.path.basename(target).split('.')[0])
    os.makedirs(outdir, exist_ok=True)
    print(f'[*] {target}')
    txt, dt = run_capture(target, outdir)
    m = re.search(r'\[RUNERR\] (.+)', txt)
    if m:
        print(f'[!] 运行时中断: {m.group(1)[:110]}')
    got = 0
    for i, hexs in re.findall(r'\[HEX (\d+)\] ([0-9a-f]+)', txt):
        data = bytes.fromhex(hexs)
        kind = classify(data)
        path = os.path.join(outdir, f'blob{i}.bin')
        open(path, 'wb').write(data)
        extra = ''
        if kind == 'lua-source':
            lp = os.path.join(outdir, f'layer{i}.lua')
            open(lp, 'wb').write(data)
            extra = f'  -> {os.path.basename(lp)}'
        print(f'    blob{i}: {len(data):>8d} B  {kind:<13s}{extra}')
        if kind in ('bytecode?', 'binary') and len(data) < 200000:
            strs = bc_strings(data)
            if strs:
                show = [s for s in strs if len(s) > 2][:6]
                if show:
                    print('        字符串表: ' + ' | '.join(repr(x[:40]) for x in show))
        got += 1
    print(f'[+] {got} 块 / {dt:.1f} 秒  ->  {outdir}')

if __name__ == '__main__':
    main()

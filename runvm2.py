#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""runvm2.py —— 用模板文件渲染，彻底避开 f-string 转义地狱"""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
LUAU = HERE / 'bin' / 'luau.aarch64'
TEMPLATE = (HERE / 'run_template.lua').read_text(encoding='utf-8')

STUB = """
-- Roblox 桩：只补类型，不干扰 VM 数值
local function RT(name)
    local t = {}
    return setmetatable(t, {
        __index = function(_, k)
            return function() return RT(name) end
        end,
        __call = function() return RT(name) end,
        __tostring = function() return name end,
    })
end
Color3, Vector3, Vector2, UDim, UDim2, Rect, CFrame = RT('Color3'), RT('Vector3'), RT('Vector2'), RT('UDim'), RT('UDim2'), RT('Rect'), RT('CFrame')
NumberRange, NumberSequence, ColorSequence, TweenInfo = RT('NumberRange'), RT('NumberSequence'), RT('ColorSequence'), RT('TweenInfo')
"""


def main():
    sample = Path(sys.argv[1] if len(sys.argv) > 1 else '/tmp/lv/8.lua')
    ast = json.loads(subprocess.run(
        [str(HERE / 'bin' / 'luau-ast.aarch64'), str(sample), '--ast-json'],
        capture_output=True, text=True, timeout=180).stdout)
    src = sample.read_text(encoding='utf-8', errors='ignore')
    lines = src.split('\n')

    def off(l, c):
        return sum(len(x) + 1 for x in lines[:l]) + c

    def text(node):
        m = re.match(r'(\d+),(\d+) - (\d+),(\d+)', node.get('location', ''))
        sl, sc, el, ec = map(int, m.groups())
        return src[off(sl, sc):off(el, ec)]

    expr = ast['root']['body'][0]['list'][0]['func']['func']['expr']
    items = expr['args'][0]['items']
    slots = {}
    for it in items:
        k = it.get('key', {})
        key = k.get('value') if k.get('type') == 'AstExprConstantString' else (
            str(k.get('value')) if k.get('type') == 'AstExprConstantNumber' else None)
        if key is not None:
            slots[key] = it['value']

    table_text = text(expr['args'][0])
    l6_text = text(slots['L6'])
    # patch: nil -> universal object at the single return point
    patched = l6_text.replace('local d,X=33;', 'local d,X=33; __L6LOG(d,X);')
    if patched != l6_text:
        print('[+] L6 patched: nil guard injected')
        l6_text = patched
    else:
        print('[!] L6 patch NOT applied')
    f6 = slots['F6']['value']

    out = TEMPLATE
    out = out.replace('--$STUB', STUB)
    out = out.replace('--$TABLE', table_text)
    out = out.replace('--$L6', l6_text)
    out = out.replace('__F6__', '[==[' + f6 + ']==]')

    tmp = Path(tempfile.mkdtemp()) / 'run.lua'
    tmp.write_text(out, encoding='utf-8')
    print(f'[+] {tmp}')
    outf = Path('/tmp/luau_out.txt')
    with open(outf, 'wb') as fh:
        r = subprocess.run([str(LUAU), str(tmp)], stdout=fh, stderr=subprocess.PIPE, timeout=600)
    out = outf.read_text(errors='ignore')
    print(f'[+] stdout {len(out)} bytes -> {outf}')
    print(out[:3000])
    if r.stderr:
        print('--- stderr ---')
        print(r.stderr[:1500])


if __name__ == '__main__':
    main()

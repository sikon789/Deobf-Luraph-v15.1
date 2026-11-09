#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dynlift.py —— 动态截获 Luraph 的 Luau 字节码，再反编译回源码

思路（不解 VM，绕过去）：
    Luraph v15.1 的加载器最终一定调用 luau_load(bytecode, env, settings)。
    字节码在那之前已经解好密、拼好片、是明文。
    所以在那个调用点之前把 src 抓下来就行 —— 不需要破 VM，不需要逆向
    它的解密算法，也不需要真实的 Roblox 环境。

    抓到字节码后交给 Tovek（lift.py）反编译，得到接近原始的可读源码。

安全边界：
    · 只在本地桩环境跑，不联网（game:HttpGet 被桩掉）
    · 有超时
    · 不执行反编译产物，只做文本输出
"""
import re
import sys
import subprocess
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent


def find_luau():
    for cand in (HERE / "bin" / "luau.aarch64", HERE / "bin" / "luau.x86_64",
                 HERE / "bin" / "luau"):
        if cand.is_file():
            return cand
    import shutil
    return shutil.which("luau")


LOADER_SIGNS = [
    ('_vmcore.luau_load', '标准 VM 模块'),
    ('luau_load', 'luau_load 调用'),
    ('luau_deserialize', 'luau_deserialize'),
    ('vmcore', 'vmcore 表'),
]


def probe_loader(src):
    """诊断这个样本能不能走动态截获。
    返回 (ok, 说明)。ok=False 时给出具体原因，不要假装能跑。"""
    hits = [(pat, desc) for pat, desc in LOADER_SIGNS if pat in src]
    if not hits:
        return False, ("样本里找不到 luau_load / vmcore / luau_deserialize。\n"
                       "        说明它的 VM 是内联展开的，或者加载器被改名了。\n"
                       "        当前动态路径锚定唯一写法，处理不了这种。")
    if not any(p in src for p, _ in hits if p == '_vmcore.luau_load'):
        return False, (f"有 VM 痕迹（{hits[0][1]}），但没有 `_vmcore.luau_load` 这类调用点。\n"
                       "        VM 可能是内联展开的，截获点不固定。\n"
                       "        需要针对这个变体单独定位。")
    return True, f"检测到加载器：{hits[0][1]}"


def find_hook_point(src):
    """找 luau_load 的调用语句起点。
    直接锚在 `local _lo,_main=_pc(_vmcore.luau_load` 上，
    不做回退扫描 —— 回退会跳到别的 local，注入后 src 还不是字符串。"""
    pats = [
        r'local\s+_lo\s*,\s*_main\s*=\s*_pc\(\s*_vmcore\.luau_load',
        r'local\s+\w+\s*,\s*\w+\s*=\s*_pc\(\s*_vmcore\.luau_load',
        r'local\s+\w+\s*=\s*[\w.]+\(\s*_vmcore\.luau_load',
    ]
    for pat in pats:
        m = re.search(pat, src)
        if m:
            return m.start()
    # 退路：函数定义之后第一个 luau_load 调用
    for m in re.finditer(r'_vmcore\.luau_load\s*,', src):
        return m.start()
    return None


HOOK = (
    # 只读 src，不做任何会改变它的操作。
    # （早先版本先调了 luau_deserialize 做前置判断，结果把 src 换成了别的类型，
    #  后面 #src 就报 "attempt to get length of a number"）
    'do local _h={} local _n=#src '
    'for _i=1,_n do _h[#_h+1]=string.format("%02x",string.byte(src,_i)) end '
    'print("@@BC@@".._n) '
    'local _ch={} for _i=1,#_h do _ch[#_ch+1]=_h[_i] '
    'if #_ch>=4000 then print("@@H@@"..table.concat(_ch)) _ch={} end end '
    'if #_ch>0 then print("@@H@@"..table.concat(_ch)) end '
    'print("@@END@@") end '
)


def extract_bc(html_or_lua_path, workdir=None):
    """核心：从样本里截出字节码，返回 bytes 或 None"""
    raw = Path(html_or_lua_path).read_text(encoding="utf-8", errors="ignore")

    # 如果是 HTML，抽出 Luraph 代码那一行
    if "<html" in raw[:500].lower() or "<!doctype" in raw[:200].lower():
        lines = raw.split("\n")
        code = max(lines, key=len)
        print(f"     从 HTML 抽出代码行：{len(code):,} 字符")
    else:
        code = raw

    # 已知的 Luraph 语法瑕疵：少一个 end。逐级尝试修补
    candidates = []
    fixes = [
        ('else y=0;end;end return function() end end,Ty=function',
         'else y=0;end;end end return function() end end,Ty=function'),
    ]
    for a, b in fixes:
        if a in code:
            candidates.append(code.replace(a, b, 1))
    candidates.append(code)   # 原版放最后兜底

    luau = find_luau()
    if not luau:
        print("     ✗ 找不到 luau 运行时（先跑 python fetch_bin.py）")
        return None

    for ci, cand in enumerate(candidates):
        pos = find_hook_point(cand)
        if pos is None:
            continue
        hooked = cand[:pos] + HOOK + cand[pos:]
        td = Path(tempfile.mkdtemp(prefix="dynlift_"))
        f = td / "hook.lua"
        f.write_text(hooked, encoding="utf-8")
        print(f"     注入点 @{pos:,}，运行桩环境…（第 {ci+1}/{len(candidates)} 个候选）")
        try:
            r = subprocess.run([str(luau), str(f)],
                               capture_output=True, text=True, timeout=180)
        except subprocess.TimeoutExpired:
            print("     ✗ 超时（可能有死循环防护）")
            continue
        out = (r.stdout or "") + "\n" + (r.stderr or "")
        m = re.search(r"@@BC@@(\d+)", out)
        if not m:
            tail = (r.stderr or r.stdout or "").strip().split("\n")[0][:100]
            print(f"     ✗ 没抓到字节码：{tail}")
            continue
        declared = int(m.group(1))
        hexes = "".join(re.findall(r"@@H@@([0-9a-f]+)", out))
        if len(hexes) < declared * 2:
            print(f"     ✗ 字节码不完整（{len(hexes)//2:,}/{declared:,}）")
            continue
        bc = bytes.fromhex(hexes[:declared * 2])
        print(f"     ✓ 截获字节码 {len(bc):,} 字节")
        return bc
    return None


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    src = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else str(Path(src).with_suffix(".luau"))

    print(f"[1] 截获字节码：{src}")
    bc = extract_bc(src)
    if not bc:
        print("[✗] 截获失败")
        return 1

    tmpbc = Path(tempfile.mkdtemp(prefix="bc_")) / "payload.bin"
    tmpbc.write_bytes(bc)
    print(f"[2] 反编译 → {out}")
    r = subprocess.run([sys.executable, str(HERE / "lift.py"),
                        str(tmpbc), out], capture_output=True, text=True)
    print((r.stdout or "").strip()[-500:])
    if r.returncode != 0:
        print((r.stderr or "").strip()[-500:])
        return 1
    p = Path(out)
    if p.is_file():
        print(f"[✓] {p}  {p.stat().st_size:,} 字节  "
              f"{p.read_text(encoding='utf-8', errors='ignore').count(chr(10))+1:,} 行")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())

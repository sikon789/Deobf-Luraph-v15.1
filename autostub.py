#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
autostub.py —— 自动补齐 Luau CLI 缺失的 Roblox 全局，让样本能一路跑下去

思路：
    Luau CLI 没有 Roblox 类型（Color3 / Vector2 / Rect / UDim2 / game / workspace …）。
    每缺一个，样本就崩一次。这里反复运行，解析错误信息里缺的名字，
    补一个 stub，再跑，直到跑通或达到迭代上限。

    每轮补的东西会累积到最终 stub 文件里，可以直接拿去做执行轨迹。

用法:
    python autostub.py <样本.lua> [--max-round 40] [--save stub.lua] [--timeout 60]
"""
import re
import sys
import subprocess
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent

BASE_STUB = '''-- 自动生成的 Roblox 环境补齐
-- 返回一个「看起来像数字」的对象：能算术、能比较、能转数字
local __num_mt
__num_mt = {
    __index = function() return 0 end,
    __tostring = function() return "0" end,
    __add = function() return 0 end, __sub = function() return 0 end,
    __mul = function() return 0 end, __div = function() return 0 end,
    __mod = function() return 0 end, __pow = function() return 0 end,
    __idiv = function() return 0 end, __unm = function() return 0 end,
    __concat = function() return "" end,
    __len = function() return 0 end,
    __eq = function() return false end,
    __lt = function() return false end,
    __le = function() return false end,
}
local function __value()
    return setmetatable({}, __num_mt)
end

-- 类型表：Color3.new(...) / Vector2.new(...) 这类必须能调用并返回可用对象
local function __typetbl(name)
    local t = {}
    return setmetatable(t, {
        __index = function(_, k)
            if type(k) == 'number' then return 0 end
            if k == 'new' or k == 'fromRGB' or k == 'fromHex' or k == 'fromScale'
               or k == 'fromOffset' or k == 'fromEnum' or k == 'fromAxisAngle' then
                return function(...) return __value() end
            end
            return function(...) return __value() end
        end,
        __call = function() return __value() end,
        __tostring = function() return name end,
    })
end

-- 服务/实例桩：任何方法都能调，返回可继续索引的对象
local __inst_cache = {}
local function __inst(name)
    if __inst_cache[name] then return __inst_cache[name] end
    local t = {}
    __inst_cache[name] = t
    return setmetatable(t, {
        __index = function(_, k)
            if type(k) == 'number' then return nil end
            -- 已知需要返回具体类型的
            local special = {
                ScreenGui = 'Instance', Frame = 'Instance',
                TextLabel = 'Instance', TextButton = 'Instance',
            }
            return setmetatable({}, {
                __index = function(_, k2)
                    if type(k2) == 'number' then return nil end
                    return __inst(name .. '.' .. tostring(k) .. '.' .. tostring(k2))
                end,
                __call = function() return __inst(name .. '.' .. tostring(k) .. '()') end,
                __tostring = function() return name .. '.' .. tostring(k) end,
            })
        end,
        __newindex = function() end,
        __call = function() return __inst(name .. '()') end,
        __tostring = function() return name end,
        __eq = function() return false end,
    })
end

local __FUNC_STUBS = {
    Wait = function() end, wait = function() end,
    tick = function() return os.clock() end,
    time = function() return os.clock() end,
    spawn = function(f) if type(f) == 'function' then pcall(f) end end,
    task = {
        wait = function() end,
        spawn = function(f) if type(f) == 'function' then pcall(f) end end,
        delay = function(_, f) if type(f) == 'function' then pcall(f) end end,
        defer = function(f) if type(f) == 'function' then pcall(f) end end,
        cancel = function() end,
    },
    typeof = function(v) return type(v) end,
    getgenv = function() return _G end,
    getfenv = getfenv,
    setfenv = setfenv,
    warn = function() end,
    identifyexecutor = function() return "stub", "1.0" end,
    gethui = function() return __inst("gethui") end,
    getscriptclosure = function() return function() end end,
    hookfunction = function(a, b) return a end,
    checkcaller = function() return false end,
    setreadonly = function() end,
    isreadonly = function() return false end,
    cloneref = function(x) return x end,
    firetouchinterest = function() end,
    fireclickdetector = function() end,
    request = function() return { StatusCode = 200, Body = "" } end,
    http_request = function() return { StatusCode = 200, Body = "" } end,
}

-- 类型表
local __TYPES = {
    'Color3', 'Vector2', 'Vector3', 'Vector3int16', 'Vector2int16',
    'Rect', 'UDim', 'UDim2', 'CFrame', 'BrickColor', 'Font',
    'NumberSequence', 'ColorSequence', 'NumberRange', 'PhysicalProperties',
    'TweenInfo', 'Ray', 'Region3', 'Region3int16', 'Random', 'DateTime',
    'Instance', 'Enum', 'EnumItem', 'OverlapParams', 'RaycastParams',
    'NumberSequenceKeypoint', 'ColorSequenceKeypoint', 'Axes', 'Faces',
    'Content', 'Path2DControlPoint', 'SharedTable', 'buffer',
}
'''

APPLY_STUB = '''
-- 把这些补进全局（样本直接读 _G）
-- Luau CLI 的 _G 是 readonly，不能直接写。
-- 做法：拿到当前环境表（getfenv(0) 或 getfenv(1)），往那里注入。
local _ENV_T = (getfenv and (getfenv(0) or getfenv(1))) or _G
for _, n in ipairs(__TYPES) do
    if rawget(_ENV_T, n) == nil then _ENV_T[n] = __typetbl(n) end
end
for k, v in pairs(__FUNC_STUBS) do
    if rawget(_ENV_T, k) == nil then _ENV_T[k] = v end
end
if rawget(_ENV_T, 'game') == nil then _ENV_T.game = __inst('game') end
if rawget(_ENV_T, 'workspace') == nil then _ENV_T.workspace = __inst('workspace') end
if rawget(_ENV_T, 'script') == nil then _ENV_T.script = __inst('script') end
if rawget(_ENV_T, 'Enum') == nil then _ENV_T.Enum = __typetbl('Enum') end
_ENV_T.__inst = __inst
_ENV_T.__value = __value
_ENV_T.__typetbl = __typetbl
'''


def find_luau():
    for c in (HERE / 'bin' / 'luau.aarch64', HERE / 'bin' / 'luau.x86_64',
              HERE / 'bin' / 'luau'):
        if c.is_file():
            return c
    import shutil
    return shutil.which('luau')


MISS_RE = re.compile(r"attempt to index (\w+) with '([^']+)'")


def run(sample_text, stub_extra, luau, timeout=60):
    """跑一次，返回 (ok, 错误信息)"""
    hdr = BASE_STUB + stub_extra + APPLY_STUB
    td = Path(tempfile.mkdtemp(prefix='autostub_'))
    f = td / 'run.lua'
    f.write_text(hdr + '\n' + sample_text, encoding='utf-8')
    try:
        r = subprocess.run([str(luau), str(f)], capture_output=True,
                           text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return 'timeout', '执行超时（可能进了死循环或等事件）'
    err = (r.stderr or '') + (r.stdout or '')
    if not err.strip():
        return True, ''
    # 只取第一行错误
    first = next((l for l in err.split('\n') if ':' in l and
                  ('attempt' in l or 'expected' in l or 'stack overflow' in l
                   or 'Error' in l)), err.split('\n')[0])
    return False, first


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    max_round = 40
    save = None
    timeout = 60
    for i, a in enumerate(sys.argv):
        if a == '--max-round' and i + 1 < len(sys.argv):
            max_round = int(sys.argv[i + 1])
        if a == '--save' and i + 1 < len(sys.argv):
            save = sys.argv[i + 1]
        if a == '--timeout' and i + 1 < len(sys.argv):
            timeout = int(sys.argv[i + 1])

    if not args:
        print(__doc__)
        return 1

    sample = Path(args[0]).read_text(encoding='utf-8', errors='ignore')
    luau = find_luau()
    if not luau:
        print("[✗] 找不到 luau")
        return 1

    extra = []
    seen = set()
    for rd in range(1, max_round + 1):
        ok, err = run(sample, '\n'.join(extra), luau, timeout)
        if ok is True:
            print(f"\n[✓] 第 {rd} 轮跑通，无报错")
            break
        if ok == 'timeout':
            print(f"\n[⏱] 第 {rd} 轮：{err}")
            break
        m = MISS_RE.search(err)
        if not m:
            print(f"[轮 {rd}] 非缺失类错误：{err[:160]}")
            break
        target, field = m.group(1), m.group(2)
        key = (target, field)
        if key in seen:
            print(f"[轮 {rd}] 同一个位置反复失败，放弃：{err[:160]}")
            break
        seen.add(key)
        print(f"[轮 {rd:>2}] 缺 {target}.{field} → 补 stub")
        # 给这个全局换成万能类型表
        extra.append(f'_ENV_T.{target} = rawget(_ENV_T, "{target}") or __typetbl("{target}")\n'
                     f'if type(rawget(_ENV_T, "{target}")) ~= "table" then _ENV_T.{target} = __typetbl("{target}") end')
        # 若它已经存在但缺字段，做一次包装
        extra.append(f'do local _t = rawget(_ENV_T, "{target}") '
                     f'if type(_t) == "table" and _t.{field} == nil then '
                     f'local _o = _t '
                     f'_ENV_T.{target} = setmetatable({{}}, {{__index = function(_, k) '
                     f'if k == "{field}" then return function(...) return __value() end end '
                     f'local v = _o[k] if v ~= nil then return v end '
                     f'return function(...) return __value() end end, '
                     f'__call = function() return __value() end}}) end end')

    if save:
        hdr = BASE_STUB + '\n'.join(extra) + APPLY_STUB
        Path(save).write_text(hdr, encoding='utf-8')
        print(f"[+] stub 已保存 → {save}")
    return 0


if __name__ == '__main__':
    sys.exit(main())

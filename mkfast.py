#!/usr/bin/env python3
"""mkfast.py <target.lua> <out_runner.lua> [minlen] [--stub]
把目标脚本嵌进 runner，用纯 Lua buffer 模拟接管全部 buffer 操作，
可选叠加 Roblox 万能桩，跑完后 dump 所有 buffer（hex）——绕过符号执行直接拿解码结果。
"""
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))

# 多路径回退：脚本同级 → 上级 → 上上级
def _find(fname):
    for root in (HERE, os.path.dirname(HERE), os.path.dirname(os.path.dirname(HERE))):
        p = os.path.join(root, fname)
        if os.path.isfile(p):
            return p
    return None

args = [a for a in sys.argv[1:] if not a.startswith('--')]
stub = '--stub' in sys.argv
if len(args) < 2:
    sys.stderr.write('用法: mkfast.py <target.lua> <out_runner.lua> [minlen] [--stub]\n')
    sys.exit(2)
src_path, out_path = args[0], args[1]
minlen = args[2] if len(args) > 2 else "512"

src = open(src_path, 'rb').read().decode('utf-8', 'replace')

emu_path = _find('bufemu.lua')
if not emu_path:
    sys.stderr.write('[mkfast] 找不到 bufemu.lua（应在脚本目录或其上级）\n')
    sys.exit(3)
emu = open(emu_path, 'r', encoding='utf-8').read().replace('return BE', '')

stub_src = ''
if stub:
    stub_path = _find('robstub.lua')
    if stub_path:
        stub_src = "(function()\n" + open(stub_path, 'r', encoding='utf-8').read() + "\nend)()"

edge, n = '', 0
while ('[' + edge + '[') in src or (']' + edge + ']') in src:
    edge += '='
    n += 1

runner = '''
local MINLEN = %s
local SRC = [%s[
%s
]%s]
%s
local ROB = %s
local realprint = print
local function hexof(s)
  local parts = {}
  for i = 1, #s, 4096 do
    parts[#parts + 1] = (string.gsub(string.sub(s, i, i + 4095), ".", function(c)
      return string.format("%%02x", string.byte(c))
    end))
  end
  return table.concat(parts)
end
local ENV = setmetatable({ buffer = BE, print = realprint, warn = realprint }, {
  __index = function(t, k)
    if ROB then local v = ROB[k]; if v ~= nil then return v end end
    local v = _G[k]
    if v ~= nil then return v end
    if ROB then return ROB.ANY(tostring(k)) end
    return nil
  end
})
local ok, err = xpcall(function()
  local loader = loadstring or load
  local setter = setfenv or function(f) return f end
  local chunk, lerr = loader(SRC, "=target")
  if not chunk then error("load failed: " .. tostring(lerr)) end
  setter(chunk, ENV)
  local r = chunk()
  if type(r) == "function" then r() end
end, function(e) return tostring(e) .. string.char(10) .. debug.traceback("", 2) end)
if not ok then realprint("[RUNERR] " .. tostring(err)) end
local bufs = BE.__dump(MINLEN)
realprint(string.format("[BUFS] %%d", #bufs))
for i = 1, #bufs do
  local b = bufs[i]
  local s = BE.tostring(b)
  realprint(string.format("[BUF %%d] len=%%d", i, #s))
  realprint("[HEX " .. i .. "] " .. hexof(s))
end
''' % (minlen, edge, src, edge, emu, stub_src if stub else 'nil')

open(out_path, 'w').write(runner)
print('wrote', out_path, len(runner), 'bytes; bracket', n, 'stub', bool(stub))

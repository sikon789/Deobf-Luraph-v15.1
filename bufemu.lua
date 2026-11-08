-- 纯 Lua 模拟 Luau buffer 库：所有 buffer 操作走这里，最后可整体 dump。
-- 用稀疏表存字节（写 O(1)），避免 string 拼接的 O(n^2)。
local byte, sub, char, concat = string.byte, string.sub, string.char, table.concat

local BE = {}
local all = {}
local seq = 0
local LIMIT = 32 * 1024 * 1024

local function mk(n, init)
  n = n or 0
  seq = seq + 1
  local b = {t = {}, n = n, init = init, id = seq}
  if #all < 4096 then all[#all + 1] = b end
  return b
end

function BE.create(n) return mk(n) end
function BE.fromstring(s) return mk(#s, s) end
function BE.len(b) return b.n end
function BE.clone(b)
  local c = mk(b.n, b.init)
  for k, v in pairs(b.t) do c.t[k] = v end
  return c
end
function BE.copy(dst, doff, src, soff, sz)
  for i = 0, sz - 1 do
    local v = src.t[soff + i]
    if v == nil then v = src.init and byte(src.init, soff + i + 1) or 0 end
    dst.t[doff + i] = v
  end
end
function BE.fill(b, off, val, sz)
  for i = 0, sz - 1 do b.t[off + i] = val end
end
function BE.tostring(b)
  local parts, chunk = {}, {}
  local cnt = 0
  for i = 0, b.n - 1 do
    local v = b.t[i]
    if v == nil then v = b.init and byte(b.init, i + 1) or 0 end
    cnt = cnt + 1
    chunk[cnt] = v
    if cnt == 1024 then parts[#parts + 1] = char(table.unpack(chunk)); chunk = {}; cnt = 0 end
  end
  if cnt > 0 then parts[#parts + 1] = char(table.unpack(chunk)) end
  return concat(parts)
end

local function getb(b, o)
  if type(b) ~= "table" then
    print("[BEERR] buffer=" .. tostring(b) .. " off=" .. tostring(o))
    print(debug.traceback("", 3))
    error("bad buffer", 0)
  end
  local v = b.t[o]
  if v ~= nil then return v end
  return b.init and byte(b.init, o + 1) or 0
end
local function putb(b, o, v) b.t[o] = v % 256 end

local function rd(b, o, n)
  local t = {}
  for i = 0, n - 1 do t[i + 1] = getb(b, o + i) end
  return t
end

function BE.readi8(b, o) local v = getb(b, o); return v >= 128 and v - 256 or v end
function BE.readu8(b, o) return getb(b, o) end
function BE.readi16(b, o) local a, c = getb(b, o), getb(b, o + 1)
  local v = a + c * 256; return v >= 32768 and v - 65536 or v end
function BE.readu16(b, o) return getb(b, o) + getb(b, o + 1) * 256 end
function BE.readi32(b, o)
  local v = getb(b, o) + getb(b, o + 1) * 256 + getb(b, o + 2) * 65536 + getb(b, o + 3) * 16777216
  if v >= 2147483648 then v = v - 4294967296 end
  return v end
function BE.readu32(b, o) return getb(b, o) + getb(b, o + 1) * 256 + getb(b, o + 2) * 65536 + getb(b, o + 3) * 16777216 end
function BE.readf32(b, o) return 0 end
function BE.readf64(b, o) return 0 end
function BE.readstring(b, o, n) return char(table.unpack(rd(b, o, n))) end

function BE.writei8(b, o, v) putb(b, o, v) end
function BE.writeu8(b, o, v) putb(b, o, v) end
function BE.writei16(b, o, v) v = v % 65536; putb(b, o, v); putb(b, o + 1, math.floor(v / 256)) end
function BE.writeu16(b, o, v) BE.writei16(b, o, v) end
function BE.writei32(b, o, v)
  v = v % 4294967296
  putb(b, o, v % 256); putb(b, o + 1, math.floor(v / 256) % 256)
  putb(b, o + 2, math.floor(v / 65536) % 256); putb(b, o + 3, math.floor(v / 16777216) % 256)
end
function BE.writeu32(b, o, v) BE.writei32(b, o, v) end
function BE.writef32(b, o, v) end
function BE.writef64(b, o, v) end
function BE.writestring(b, o, s, cnt)
  cnt = cnt or #s
  for i = 1, cnt do putb(b, o + i - 1, byte(s, i)) end
end

function BE.__dump(minlen)
  minlen = minlen or 512
  local out = {}
  for i = 1, #all do
    local b = all[i]
    if b.n >= minlen then
      out[#out + 1] = b
    end
  end
  return out
end

return BE

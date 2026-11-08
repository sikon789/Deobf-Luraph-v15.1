-- 静默万能桩：Roblox 类型全部变成"任何属性都能取、任何调用都返回自己"的对象。
-- 目的只是让解密路径跑通，不追求语义正确。
local ANYMT = {}
local cache = {}

local function ANY(name)
  local c = cache[name]
  if c then return c end
  local o = setmetatable({ __name = name }, ANYMT)
  cache[name] = o
  return o
end

ANYMT.__index = function(t, k)
  local v = ANY(t.__name .. "." .. tostring(k))
  rawset(t, k, v)
  return v
end
ANYMT.__newindex = function() end
local LOGN = 0
function ROBLOGSET(v) end
ANYMT.__call = function(t, ...)
  if ROB and ROB.__stop then error("ANY:" .. t.__name, 0) end
  if ROB and ROB.__log and LOGN < 400 then
    LOGN = LOGN + 1
    ROB.__out(string.format("[CALL %d] %s", LOGN, t.__name))
  end
  return ANY(t.__name .. "()")
end
ANYMT.__tostring = function(t) return t.__name end
ANYMT.__concat = function(a, b) return 0 end
ANYMT.__add = function() return 0 end
ANYMT.__sub = function() return 0 end
ANYMT.__mul = function() return 0 end
ANYMT.__div = function() return 0 end
ANYMT.__mod = function() return 0 end
ANYMT.__pow = function() return 0 end
ANYMT.__unm = function() return 0 end
ANYMT.__eq = function() return false end
ANYMT.__lt = function() return false end
ANYMT.__le = function() return false end
ANYMT.__len = function() return 0 end

ROB = {}
ROB.ANY = ANY
ROB.__ANYMT = ANYMT
for _, n in ipairs({ "Rect", "Vector2", "Vector3", "Vector2int16", "Vector3int16", "Region3",
  "UDim", "UDim2", "Color3", "ColorSequence", "ColorSequenceKeypoint", "NumberRange",
  "NumberSequence", "NumberSequenceKeypoint", "CFrame", "Instance", "Enum", "BrickColor",
  "TweenInfo", "Ray", "Random", "Faces", "Axes", "PhysicalProperties", "RaycastParams",
  "OverlapParams", "CatalogSearchParams", "DateTime", "Font", "Path2D", "PathWaypoint",
  "DockWidgetPluginGuiInfo", "RotationCurveKey", "Rect", "SharedTable" }) do
  ROB[n] = ANY(n)
end
ROB.game = ANY("game")
ROB.workspace = ANY("workspace")
ROB.script = ANY("script")
ROB.shared = {}
ROB.plugin = ANY("plugin")

function ROB.typeof(v)
  if type(v) == "table" and getmetatable(v) == ANYMT then return v.__name:match("^[%w_]+") or "Instance" end
  return typeof(v)
end

return ROB

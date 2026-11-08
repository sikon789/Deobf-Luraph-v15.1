local ENV = setmetatable({}, { __index = getfenv(), __newindex = function(t,k,v) rawset(t,k,v) end })
-- Roblox 模拟环境（通用桩）：用于验证解混淆后的脚本是否能真正执行
local NUMERIC = {}
for _, k in ipairs({
	"X", "Y", "Z", "W", "R", "G", "B", "Width", "Height", "Value", "Min", "Max",
	"Transparency", "Rotation", "Thickness", "LayoutOrder", "ZIndex", "TextSize",
	"TextTransparency", "BackgroundTransparency", "AspectRatio", "Magnitude",
	"Position", "Size", "Access", "Intensity", "Density", "Offset", "Scale",
	"AbsoluteSize", "AbsolutePosition", "ViewportSize", "Unit", "Fuzzyness",
	"BorderSizePixel", "ScrollBarThickness", "CanvasPosition", "CanvasSize",
	"PlaybackSpeed", "Volume", "TimePosition", "Length", "Speed", "Health",
	"MaxHealth", "WalkSpeed", "JumpPower", "DisplayOrder", "PaddingTop",
	"PaddingBottom", "PaddingLeft", "PaddingRight", "Scale",
}) do
	NUMERIC[k] = true
end

local function mk(name)
	local obj = {}
	local mt = {}
	mt.__index = function(_, k)
		if type(k) == "number" then return nil end
		if NUMERIC[k] then return 0 end
		local child = mk(name .. "." .. tostring(k))
		rawset(obj, k, child)
		return child
	end
	mt.__newindex = function() end
	mt.__call = function() return mk(name .. "()") end
	mt.__tostring = function() return "<" .. name .. ">" end
	mt.__len = function() return 0 end
	mt.__eq = function() return false end
	mt.__lt = function() return false end
	mt.__le = function() return false end
	mt.__concat = function() return "" end
	mt.__add = function() return 0 end
	mt.__sub = function() return 0 end
	mt.__mul = function() return 0 end
	mt.__div = function() return 0 end
	mt.__unm = function() return 0 end
	return setmetatable(obj, mt)
end

local ok, _ = pcall(function() return buffer end)

-- 类
for _, n in ipairs({
	"Color3", "UDim2", "UDim", "Vector2", "Vector3", "CFrame", "Rect",
	"NumberSequence", "ColorSequence", "NumberSequenceKeypoint",
	"ColorSequenceKeypoint", "TweenInfo", "Font", "Instance", "BrickColor",
	"Ray", "Region3", "Faces", "PhysicalProperties", "NumberRange",
	"PathWaypoint", "Random", "DateTime", "OverlapParams", "RaycastParams",
	"TextChatMessageProperties", "SharedTable", "Content", "AnimationClip",
}) do
	ENV[n] = mk(n)
end

ENV.Enum = mk("Enum")
ENV.game = mk("game")
ENV.workspace = mk("workspace")
ENV.Workspace = ENV.workspace
ENV.script = mk("script")
ENV.shared = {}
ENV.players = mk("players")
ENV.plugin = mk("plugin")


-- 任务调度：同步执行，方便暴露真实错误
ENV.task = {
	spawn = function(f, ...) local ok, e = pcall(f, ...) if not ok then print("[task.spawn err] " .. tostring(e)) end end,
	defer = function(f, ...) local ok, e = pcall(f, ...) if not ok then print("[task.defer err] " .. tostring(e)) end end,
	delay = function(_, f) end,
	wait = function() return 0 end,
	cancel = function() end,
}
ENV.wait = function() return 0 end
ENV.tick = function() return 0 end
ENV.time = function() return os.time() end
ENV.typeof = type
ENV.getgenv = function() return _G end
ENV.getsenv = ENV.getgenv
ENV.setfenv = function(f) return f end
ENV.getfenv = function() return _G end
ENV.readfile = function() return nil end
ENV.writefile = function() end
ENV.isfile = function() return false end
ENV.isfolder = function() return false end
ENV.makefolder = function() end
ENV.listfiles = function() return {} end
ENV.identifyexecutor = function() return "luau", "1.0" end
ENV.request = function() return { StatusCode = 200, Body = "{}" } end
ENV.http_request = ENV.request
ENV.syn = ENV.request
ENV.warn = function(...) print("[warn]", ...) end
ENV.sethiddenproperty = function() end
ENV.firetouchtransmitter = function() end
ENV.getnilinstances = function() return {} end
ENV.gethui = function() return mk("CoreGui") end
ENV.setclipboard = function() end
ENV.getclipboard = function() return "" end
ENV.checkcaller = function() return true end

-- loadstring 必须继承同一环境（否则内层 chunk 看不到 game 等）
local __real_load = loadstring or load
ENV.loadstring = function(s, name)
	local f = __real_load(s, name or "Luraph")
	if f then setfenv(f, ENV) end
	return f
end
ENV.load = ENV.loadstring

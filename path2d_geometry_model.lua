-- Bounded mathematical Path2D model; inject after STUBS, before PAY.
-- Official formula: creator-docs/content/en-us/ui/2D-paths.md#Generation-details.
-- No Roblox engine numerical equivalence claimed. Open, exactly two-point paths.
-- Only fixed-offset Frame dimensions are supported. No layout/UIScale/rotation.
-- Tangent normalization, rendered Rect padding and multi-segment t mapping
-- are not specified sufficiently by public docs: fail closed for those APIs.
local __pathrecords={}
local __pathresults={}
local __pathsizes={}
local __pathcalls={}
local function __pathcopy(p)
 return {Position=p.Position,LeftTangent=p.LeftTangent,RightTangent=p.RightTangent}
end
function __PATH_RECORD(name,obj,value)
 if name=='Size' then __pathsizes[obj]=value end
 if name=='SetControlPoints' then
  assert(#value<=100,'PATH_LIMIT: maximum 100 control points')
  local snapshot={}
  for i,p in ipairs(value) do snapshot[i]=__pathcopy(p) end
  __pathrecords[#__pathrecords+1]={name,obj,snapshot}
 else __pathrecords[#__pathrecords+1]={name,obj,value} end
end
local function __pathfail(name)
 error('PATH_GEOMETRY_UNIMPLEMENTED:'..name,0)
end
local function __pathcoeff(u)
 if u==nil then return {0,0,0,0} end
 return {u.X.Scale,u.X.Offset,u.Y.Scale,u.Y.Offset}
end
local function __pathadd(a,b)
 return {a[1]+b[1],a[2]+b[2],a[3]+b[3],a[4]+b[4]}
end
local function __pathsegment(obj)
 local points=obj:GetControlPoints()
 if #points<2 then error('PATH_CONTROL_POINTS: need at least two points',0) end
 if #points~=2 then __pathfail('multi-segment parameter mapping') end
 local a,b=points[1],points[2]
 local p,q=__pathcoeff(a.Position),__pathcoeff(b.Position)
 return {p,__pathadd(p,__pathcoeff(a.RightTangent)),__pathadd(q,__pathcoeff(b.LeftTangent)),q}
end
local function __patht(t)
 if type(t)~='number' or t~=t or t<0 or t>1 then
  error('PATH_PARAMETER_UNSUPPORTED: expected finite 0 <= t <= 1',0)
 end
 return t
end
local function __pathposition(c,t)
 local u=1-t
 local a,b,d,e=u*u*u,3*u*u*t,3*u*t*t,t*t*t
 local r={}
 for i=1,4 do r[i]=a*c[1][i]+b*c[2][i]+d*c[3][i]+e*c[4][i] end
 return r
end
local function __pathdimensions(obj)
 local parent=obj.Parent
 if parent==nil then __pathfail('missing container dimensions') end
 local size=__pathsizes[parent]
 if not size or size.X.Scale~=0 or size.Y.Scale~=0 then
  __pathfail('container AbsoluteSize/layout')
 end
 return size.X.Offset,size.Y.Offset
end
local function __pathpixels(c,w,h)
 local p={}
 for i=1,4 do p[i]={c[i][1]*w+c[i][2],c[i][3]*h+c[i][4]} end
 return p
end
local function __pathspeed(p,t)
 local u=1-t
 local dx=3*(u*u*(p[2][1]-p[1][1])+2*u*t*(p[3][1]-p[2][1])+t*t*(p[4][1]-p[3][1]))
 local dy=3*(u*u*(p[2][2]-p[1][2])+2*u*t*(p[3][2]-p[2][2])+t*t*(p[4][2]-p[3][2]))
 return math.sqrt(dx*dx+dy*dy)
end
-- Composite 5-point Gauss-Legendre quadrature, no recursive Lua calls.
local function __pathintegral(p,t)
 local nodes={0,0.5384693101056831,-0.5384693101056831,0.906179845938664,-0.906179845938664}
 local weights={0.5688888888888889,0.4786286704993665,0.4786286704993665,0.2369268850561891,0.2369268850561891}
 local total=0
 for bin=1,128 do
  local half=t/256
  local mid=(2*bin-1)*half
  for j=1,5 do total+=half*weights[j]*__pathspeed(p,mid+half*nodes[j]) end
 end
 return total
end
function __PATH_CALL(obj,name,...)
 local args=table.pack(...)
 -- Store raw values only at VM depth: no type/tostring/recursive dumping here.
 __pathcalls[#__pathcalls+1]={name,obj,args}
 local result
 if name=='GetMaxControlPoints' then result=100
 elseif name=='UpdateControlPoint' or name=='InsertControlPoint' or name=='RemoveControlPoint' then
  local index,point=args[1],args[2]
  local current=obj:GetControlPoints()
  local count=#current
  if type(index)~='number' or index%1~=0 or index<1 or index>count+(if name=='InsertControlPoint' then 1 else 0) then
   error('PATH_CONTROL_POINT_INDEX: out of range',0)
  end
  if name=='InsertControlPoint' and count>=100 then error('PATH_LIMIT: maximum 100 control points',0) end
  local updated={}
  for i,p in ipairs(current) do updated[i]=__pathcopy(p) end
  if name=='RemoveControlPoint' then table.remove(updated,index)
  else
   if not point or not point.Position then error('PATH_CONTROL_POINT: Position required',0) end
   if name=='InsertControlPoint' then table.insert(updated,index,__pathcopy(point))
   else updated[index]=__pathcopy(point) end
  end
  obj:SetControlPoints(updated)
  __pathresults[#__pathresults+1]={name,'void'}
  return
 elseif name=='GetPositionOnCurve' then
  local t=__patht(args[1])
  local value=__pathposition(__pathsegment(obj),t)
  -- Uses existing UDim2 constructor, whose integer Offset conversion is a
  -- host boundary; do not quantize handles/intermediate Bezier coefficients.
  result=STUBS.UDim2.new(value[1],value[2],value[3],value[4])
 elseif name=='GetLength' or name=='GetPositionOnCurveArcLength' then
  local c=__pathsegment(obj)
  local w,h=__pathdimensions(obj)
  local p=__pathpixels(c,w,h)
  local length=__pathintegral(p,1)
  if name=='GetLength' then result=length
  else
   local fraction=__patht(args[1])
   if length==0 then __pathfail('zero-length arc inversion') end
   local lo,hi=0,1
   for i=1,42 do
    local mid=(lo+hi)/2
    if __pathintegral(p,mid)<fraction*length then lo=mid else hi=mid end
   end
   local t=if fraction==0 then 0 elseif fraction==1 then 1 else (lo+hi)/2
   local value=__pathposition(c,t)
   result=STUBS.UDim2.new(value[1],value[2],value[3],value[4])
  end
 else __pathfail(name) end
 __pathresults[#__pathresults+1]={name,result}
 return result
end
-- Invoked only AFTER the VM has unwound, including on errors.
local function __PATH_DUMP()
 local function dump(value,path,depth)
  if depth>5 then print('PATH_TRUNCATED',path);return end
  if type(value)=='table' then
   for k,v in pairs(value) do dump(v,path..'.'..tostring(k),depth+1) end
  else print('PATH_VALUE',path,type(value),tostring(value)) end
 end
 for i,a in ipairs(__pathrecords) do dump(a[3],'record.'..i..'.'..a[1],0) end
 for i,a in ipairs(__pathcalls) do dump(a[3],'call.'..i..'.'..a[1],0) end
 for i,a in ipairs(__pathresults) do dump(a[2],'result.'..i..'.'..a[1],0) end
end

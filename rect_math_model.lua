-- Explicit Rect arithmetic model; not native Roblox datatype identity.
do
 local R,mt={},{ }
 function R.new(a,b,c,d)
  local x0,y0,x1,y1
  if typeof(a)=='vector' and typeof(b)=='vector' and c==nil then
   x0,y0,x1,y1=a.X,a.Y,b.X,b.Y
  else x0,y0,x1,y1=a,b,c,d end
  assert(type(x0)=='number' and type(y0)=='number' and type(x1)=='number' and type(y1)=='number','Rect.new requires 4 numbers or 2 vectors')
  return setmetatable({Min=vector.create(math.min(x0,x1),math.min(y0,y1),0),Max=vector.create(math.max(x0,x1),math.max(y0,y1),0)},mt)
 end
 mt.__index=function(t,k)
  if k=='Width' then return t.Max.X-t.Min.X end
  if k=='Height' then return t.Max.Y-t.Min.Y end
 end
 mt.__eq=function(a,b)return a.Min==b.Min and a.Max==b.Max end
 STUBS.Rect=R
end

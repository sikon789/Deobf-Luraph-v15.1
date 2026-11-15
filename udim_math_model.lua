-- Explicit arithmetic model; not native Roblox datatype identity.
do
 local U,mt,methods={},{},{}
 function U.new(scale,offset) return setmetatable({Scale=scale or 0,Offset=math.floor(offset or 0)},mt) end
 mt.__index=methods
 function mt.__add(a,b) return U.new(a.Scale+b.Scale,a.Offset+b.Offset) end
 function mt.__sub(a,b) return U.new(a.Scale-b.Scale,a.Offset-b.Offset) end
 function mt.__unm(a) return U.new(-a.Scale,-a.Offset) end
 function mt.__eq(a,b) return a.Scale==b.Scale and a.Offset==b.Offset end
 function methods:Lerp(b,t) return U.new(self.Scale+(b.Scale-self.Scale)*t,self.Offset+(b.Offset-self.Offset)*t) end
 STUBS.UDim=U
 local D,dm,methods2={},{},{}
 function D.new(a,b,c,d)
  if type(a)=='table' and type(b)=='table' then return setmetatable({X=a,Y=b},dm) end
  return setmetatable({X=U.new(a,b),Y=U.new(c,d)},dm)
 end
 function D.fromScale(x,y) return D.new(x,0,y,0) end
 function D.fromOffset(x,y) return D.new(0,x,0,y) end
 dm.__index=function(t,k) if k=='Width' then return t.X elseif k=='Height' then return t.Y else return methods2[k] end end
 dm.__add=function(a,b)return D.new(a.X+b.X,a.Y+b.Y)end
 dm.__sub=function(a,b)return D.new(a.X-b.X,a.Y-b.Y)end
 dm.__unm=function(a)return D.new(-a.X,-a.Y)end
 dm.__eq=function(a,b)return a.X==b.X and a.Y==b.Y end
 function methods2:Lerp(b,t)return D.new(self.X:Lerp(b.X,t),self.Y:Lerp(b.Y,t))end
 STUBS.UDim2=D
end

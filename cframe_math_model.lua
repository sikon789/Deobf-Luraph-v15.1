-- DIAGNOSTIC numeric compatibility, not native Roblox CFrame type/rounding.
-- Row-major rotation, column-vector convention: (p,R)*(q,S)=(p+Rq,RS).
local CF,mt,methods={},{},{}
local vc=vector.create
local function make(x,y,z,a,b,c,d,e,f,g,h,i)
 return setmetatable({x or 0,y or 0,z or 0,a or 1,b or 0,c or 0,d or 0,e or 1,f or 0,g or 0,h or 0,i or 1},mt)
end
local function rot(t,v)
 return vc(t[4]*v.X+t[5]*v.Y+t[6]*v.Z,t[7]*v.X+t[8]*v.Y+t[9]*v.Z,t[10]*v.X+t[11]*v.Y+t[12]*v.Z)
end
function CF.new(...)
 local n=select('#',...);local a={...};print('CFRAME_NEW_ARGS',n,...)
 if n==0 then return make() end
 if n==1 and typeof(a[1])=='vector' then local p=a[1];return make(p.X,p.Y,p.Z) end
 if n==2 and typeof(a[1])=='vector' and typeof(a[2])=='vector' then
  local p,target=a[1],a[2];local back=vector.normalize(p-target)
  local right=vector.cross(vc(0,1,0),back)
  assert(vector.magnitude(right)>0,'CFrame.new vertical lookAt requires native edge convention')
  right=vector.normalize(right);local up=vector.cross(back,right)
  return make(p.X,p.Y,p.Z,right.X,up.X,back.X,right.Y,up.Y,back.Y,right.Z,up.Z,back.Z)
 end
 if n==3 then return make(a[1],a[2],a[3]) end
 if n==12 then return make(unpack(a)) end
 if n==7 then
  local x,y,z,qx,qy,qz,qw=unpack(a)
  return make(x,y,z,1-2*(qy*qy+qz*qz),2*(qx*qy-qz*qw),2*(qx*qz+qy*qw),2*(qx*qy+qz*qw),1-2*(qx*qx+qz*qz),2*(qy*qz-qx*qw),2*(qx*qz-qy*qw),2*(qy*qz+qx*qw),1-2*(qx*qx+qy*qy))
 end
 error('CFrame.new unsupported overload '..n,0)
end
function CF.Angles(x,y,z)
 print('CFRAME_ANGLES_ARGS',x,y,z)
 local a,b,c,d,e,f=math.cos(x),math.sin(x),math.cos(y),math.sin(y),math.cos(z),math.sin(z)
 -- Rx(x) Ry(y) Rz(z), Roblox fromEulerAnglesXYZ convention.
 return make(0,0,0,c*e,-c*f,d,a*f+b*d*e,a*e-b*d*f,-b*c,b*f-a*d*e,b*e+a*d*f,a*c)
end
CF.fromEulerAnglesXYZ=CF.Angles
function CF.fromEulerAnglesYXZ(x,y,z)
 print('CFRAME_YXZ_ARGS',x,y,z)
 local a,b,c,d,e,f=math.cos(x),math.sin(x),math.cos(y),math.sin(y),math.cos(z),math.sin(z)
 -- Ry(y) Rx(x) Rz(z).
 return make(0,0,0,c*e+d*b*f,-c*f+d*b*e,d*a,a*f,a*e,-b,-d*e+c*b*f,d*f+c*b*e,c*a)
end
CF.fromOrientation=CF.fromEulerAnglesYXZ
function CF.fromAxisAngle(axis,angle)
 print('CFRAME_AXISANGLE_ARGS',axis,angle)
 local n=vector.magnitude(axis);assert(n>0,'zero axis requires native convention')
 local x,y,z=axis.X/n,axis.Y/n,axis.Z/n
 local c,s=math.cos(angle),math.sin(angle);local t=1-c
 return make(0,0,0,c+x*x*t,x*y*t-z*s,x*z*t+y*s,y*x*t+z*s,c+y*y*t,y*z*t-x*s,z*x*t-y*s,z*y*t+x*s,c+z*z*t)
end
function CF.lookAt(p,target,up)
 print('CFRAME_LOOKAT_ARGS',p,target,up)
 up=up or vc(0,1,0)
 local back=vector.normalize(p-target);local right=vector.cross(up,back)
 assert(vector.magnitude(right)>0,'CFrame.lookAt degenerate convention unmodeled')
 right=vector.normalize(right);up=vector.cross(back,right)
 return make(p.X,p.Y,p.Z,right.X,up.X,back.X,right.Y,up.Y,back.Y,right.Z,up.Z,back.Z)
end
function CF.lookAlong(p,direction,up)
 print('CFRAME_LOOKALONG_ARGS',p,direction,up)
 up=up or vc(0,1,0)
 local back=-vector.normalize(direction);local right=vector.cross(up,back)
 assert(vector.magnitude(right)>0,'CFrame.lookAlong degenerate convention unmodeled')
 right=vector.normalize(right);up=vector.cross(back,right)
 return make(p.X,p.Y,p.Z,right.X,up.X,back.X,right.Y,up.Y,back.Y,right.Z,up.Z,back.Z)
end
function mt.__mul(a,b)
 if typeof(b)=='vector' then return vc(a[1],a[2],a[3])+rot(a,b) end
 assert(getmetatable(b)==mt,'CFrame multiplication operand')
 local p=vc(a[1],a[2],a[3])+rot(a,vc(b[1],b[2],b[3]));local t={p.X,p.Y,p.Z}
 for row=0,2 do for col=0,2 do local s=0;for k=0,2 do s+=a[4+3*row+k]*b[4+3*k+col] end;t[4+3*row+col]=s end end
 return make(unpack(t))
end
function mt.__add(a,b) local t=table.clone(a);t[1]+=b.X;t[2]+=b.Y;t[3]+=b.Z;return make(unpack(t)) end
function mt.__sub(a,b) return a+(-b) end
function mt.__eq(a,b) for i=1,12 do if a[i]~=b[i] then return false end end;return true end
function methods:GetComponents() return unpack(self,1,12) end
methods.components=methods.GetComponents
function methods:Inverse()
 local x,y,z=self[1],self[2],self[3]
 return make(-(self[4]*x+self[7]*y+self[10]*z),-(self[5]*x+self[8]*y+self[11]*z),-(self[6]*x+self[9]*y+self[12]*z),self[4],self[7],self[10],self[5],self[8],self[11],self[6],self[9],self[12])
end
function methods:ToWorldSpace(other) return self*other end
function methods:ToObjectSpace(other) return self:Inverse()*other end
function methods:PointToWorldSpace(v) return self*v end
function methods:PointToObjectSpace(v) return self:Inverse()*v end
function methods:VectorToWorldSpace(v) return rot(self,v) end
function methods:VectorToObjectSpace(v) return rot(self:Inverse(),v) end
function mt.__index(t,k)
 if k=='Position' or k=='p' then return vc(t[1],t[2],t[3]) end
 if k=='X' then return t[1] elseif k=='Y' then return t[2] elseif k=='Z' then return t[3] end
 if k=='RightVector' or k=='XVector' then return vc(t[4],t[7],t[10]) end
 if k=='UpVector' or k=='YVector' then return vc(t[5],t[8],t[11]) end
 if k=='ZVector' then return vc(t[6],t[9],t[12]) end
 if k=='LookVector' then return vc(-t[6],-t[9],-t[12]) end
 if k=='Rotation' then return make(0,0,0,unpack(t,4,12)) end
 if methods[k] then return methods[k] end
 print('CFRAME_MISSING_MEMBER',k);return nil
end
CF.identity=make()
STUBS.CFrame=CF

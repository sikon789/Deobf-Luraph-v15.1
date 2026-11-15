-- Finite EnumItem-shaped compatibility objects, not native identity.
do
 local E=STUBS.Enum
 local function namespace(name,names)
  local t,items={},{}
  for i,n in ipairs(names) do local item=table.freeze({Name=n,Value=i-1,EnumType=t});t[n]=item;items[i]=item end
  function t:GetEnumItems() return table.clone(items) end
  function t:FromName(n) return rawget(t,n) end
  function t:FromValue(value) for _,v in ipairs(items) do if v.Value==value then return v end end end
  return t
 end
 E.Axis=namespace('Axis',{'X','Y','Z'})
 E.NormalId=namespace('NormalId',{'Right','Top','Back','Left','Bottom','Front'})
 E.RotationOrder=namespace('RotationOrder',{'XYZ','XZY','YZX','YXZ','ZXY','ZYX'})
 function STUBS.Vector3.FromAxis(item)
  assert(item.EnumType==E.Axis,'Axis item required')
  local m={X=vector.create(1,0,0),Y=vector.create(0,1,0),Z=vector.create(0,0,1)}
  return m[item.Name]
 end
 function STUBS.Vector3.FromNormalId(item)
  assert(item.EnumType==E.NormalId,'NormalId item required')
  local m={Right=vector.create(1,0,0),Left=vector.create(-1,0,0),Top=vector.create(0,1,0),Bottom=vector.create(0,-1,0),Front=vector.create(0,0,-1),Back=vector.create(0,0,1)}
  return m[item.Name]
 end
end

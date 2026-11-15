"""Reproducible bounded runner with verified library-shape/native identity fixes.
Host API behavioral coverage is partial; NOT a full Roblox emulator.
"""
from pathlib import Path
import subprocess
r=Path(__file__).parent;p=r/'7.verified-env.lua'
subprocess.run(['python3',str(r/'gen_simple.py'),str(r/'7.inner.lua'),str(r/'7.inner.bytecode.bin'),str(p)],check=True)
s=p.read_text().replace('__steps > 100000','__steps > 2000000')
patch='''
for _,name in ipairs({'Instance','Vector2','Vector3','CFrame','Color3','UDim','UDim2','Rect','NumberRange','TweenInfo','NumberSequence','ColorSequence','Ray','Region3','PhysicalProperties','RaycastParams','OverlapParams','Font','Random','Path2DControlPoint'}) do
 STUBS[name]={new=function(...) return mkstub() end}
end
STUBS.vector={create=function(...) return mkstub() end}
STUBS.task=__NATIVE_TASK
if __NATIVE_INSTANCE then STUBS.Instance=__NATIVE_INSTANCE end
'''
s=s.replace('local PAY = buffer.fromstring(',patch+'local PAY = buffer.fromstring(')
needle='local getfenv = function() return vmenv end'
assert s.count(needle)==1
s=s.replace(needle,'''for key,val in pairs(vmenv) do hostenv[key]=val end
    hostenv.getfenv=getfenv
    hostenv.loadstring=__RAW
    local getfenv=getfenv''')
s=s.replace('G[W]=m;',"G[W]=m;if type(m)=='string' then print('VERIFIED_STRING',W,(m:gsub('.',function(c)return string.format('%02x',string.byte(c))end))) end;")
s=s.replace('pcall(ret, mkstub(), mkstub(), mkstub())','pcall(ret)')
p.write_text(s)
print('Generated',p,'requires deps/build/native-host or native Instance host variant')

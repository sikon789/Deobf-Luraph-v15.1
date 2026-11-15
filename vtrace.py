"""长轨迹 v4：把 __rec 定义在文件最顶层（保证 h64 循环可见），
其余不动。仍基于 7.opaque-gate-continuation.lua。"""
import os,subprocess
from pathlib import Path
r=Path('/var/minis/shared/luraph_v151')
src=(r/'7.opaque-gate-continuation.lua').read_text()
LIMIT=os.environ.get('LT_LIMIT','60000')
src=src.replace('if __steps > 2000000 then','if __steps > %s then'%LIMIT,1)
TOP = '''local __tr = {}
local function __rec(...)
  local t={...}
  local s=''
  for i=1,#t do s=s..(i>1 and '\\t' or '')..tostring(t[i]) end
  __tr[#__tr+1]=s
  if #__tr>=400 then print(table.concat(__tr,'\\n'));__tr={} end
end
local __flush = function() if #__tr>0 then print(table.concat(__tr,'\\n'));__tr={} end end
'''
src = TOP + src
added=0
for lv in ('if h==64 then while true do','if h==84 then while true do','if h==144 then while true do'):
    if src.count(lv)==1:
        src=src.replace(lv, lv+" __rec('T',h,w,g[w])");added+=1
print('injected sites',added)
p=r/'7.long4.trace.lua';p.write_text(src)
out=r/'7.long4.trace.log'
with out.open('wb') as f:
    try:
        z=subprocess.run(['deps/build/native-unicode',str(p)],stdout=f,stderr=subprocess.STDOUT,timeout=int(os.environ.get('LT_TO','280')))
        print('rc',z.returncode)
    except subprocess.TimeoutExpired: print('TIMEOUT')
lines=out.read_text(errors='replace').splitlines()
rec=[l for l in lines if l.startswith('T\t')]
print('lines',len(lines),'records',len(rec))
if rec:
    pcs=[int(l.split('\t')[3]) for l in rec]
    hs=sorted(set(l.split('\t')[2] for l in rec))
    print('PC range',min(pcs),max(pcs),'h',hs,'reach6386',max(pcs)>=6386)
print('tail',lines[-2:] if lines else '')

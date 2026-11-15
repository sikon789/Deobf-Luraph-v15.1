import os,subprocess,re
from pathlib import Path
r=Path('/var/minis/shared/luraph_v151')
src=(r/'7.opaque-gate-continuation.lua').read_text()
LIMIT=os.environ.get('LT_LIMIT','60000')
src=src.replace('if __steps > 2000000 then','if __steps > %s then'%LIMIT,1)
TOP = '''local __tr = {}
local function __rec(h,w,op,k,d,L)
  __tr[#__tr+1] = 'T\\1'..h..'\\1'..w..'\\1'..op..'\\1'..k..'\\1'..d..'\\1'..L
  if #__tr>=2000 then print(table.concat(__tr,'\\2'));__tr={} end
end
'''
src = TOP + src
REC=" __rec(h,w,g[w],k[w],d[w],L[w])"
count=0
a='if h==64 then while true do'
if src.count(a)==1:
    src=src.replace(a, a+REC); count+=1
b='if h==144 then while true do  local b=g[w]'
if src.count(b)==1:
    # local 声明之后插入：改成 local b=g[w];__rec(...)
    src=src.replace(b, 'if h==144 then while true do  local b=g[w];__rec(h,w,b,k[w],d[w],L[w])'); count+=1
print('injected',count)
p=r/'7.long5.trace.lua'; p.write_text(src)
out=r/'7.long5.trace.log'
with out.open('wb') as f:
    try:
        z=subprocess.run(['deps/build/native-unicode',str(p)],stdout=f,stderr=subprocess.STDOUT,timeout=int(os.environ.get('LT_TO','250')))
        print('rc',z.returncode)
    except subprocess.TimeoutExpired: print('TIMEOUT')
txt=out.read_text(errors='replace')
recs=re.findall(r'T\x01(\d+)\x01(\d+)\x01(\d+)\x01(\d+)\x01(\d+)\x01(\d+)', txt)
print('records',len(recs))
if recs:
    print('PC range',min(int(x[1]) for x in recs),max(int(x[1]) for x in recs))
    print('sample',recs[:3])
else:
    print(txt[-400:])

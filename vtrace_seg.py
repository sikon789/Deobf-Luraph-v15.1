"""修正：按"每次 op151 执行时的 d[w]+1 起始 + L[w] 长度"精确登记区段，
并且每次 op151 都产生一个新的区段登记（覆盖旧的）。
同时用序号区分，避免重叠混淆。"""
import re,subprocess
from pathlib import Path
R=Path('/var/minis/shared/luraph_v151')
src=(R/'7.opaque-gate-continuation.lua').read_text()
needle="if w==4163 or w==4172 or w==6384 or w==6386 then print('OPAQUE_ROUTE',w,g[w],E[2]) end;local D,T=g[w];if D<83"
assert src.count(needle)==1
hook = """if w==4163 or w==4172 or w==6384 or w==6386 then print('OPAQUE_ROUTE',w,g[w],E[2]) end;
if g[w]==151 then
  __sid=(__sid or 0)+1;
  local st=d[w]+1; local n=L[w];
  for i=st,st+n-1 do __seg[i]=__sid end;
end;
if __seg[w] then
  print('I\\1'..__seg[w]..'\\1'..w..'\\1'..tostring(g[w])..'\\1'..tostring(k[w])..'\\1'..tostring(d[w])..'\\1'..tostring(L[w]))
end;
local D,T=g[w];if D<83"""
src=src.replace(needle,hook)
src='local __seg={}\n'+src
p=R/'7.seg2.lua'; p.write_text(src)
out=R/'7.seg2.log'
with out.open('wb') as f:
    try: subprocess.run(['deps/build/native-unicode',str(p)],stdout=f,stderr=subprocess.STDOUT,timeout=250)
    except subprocess.TimeoutExpired: print('TIMEOUT')
t=out.read_text(errors='replace')
recs=re.findall(r'I\x01(\d+)\x01(\d+)\x01(\d+)\x01(\d+)\x01(\d+)\x01(\d+)', t)
print('记录',len(recs))
from collections import Counter
sids=Counter(int(r[0]) for r in recs)
print('区段数',len(sids),'每段记录数 top5',sids.most_common(5))
print('唯一 pc 数',len({int(r[1]) for r in recs}))

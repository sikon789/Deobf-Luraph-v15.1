"""验证：op151 执行前后，目标区段的 g 值是否等于随后执行时的 op。
在 op151 执行前记录 g[st..st+n]，执行后再次记录，并与实际执行的 op 比对。"""
import re,subprocess
from pathlib import Path
R=Path('/var/minis/shared/luraph_v151')
src=(R/'7.opaque-gate-continuation.lua').read_text()
needle="if w==4163 or w==4172 or w==6384 or w==6386 then print('OPAQUE_ROUTE',w,g[w],E[2]) end;local D,T=g[w];if D<83"
assert src.count(needle)==1
hook = """if w==4163 or w==4172 or w==6384 or w==6386 then print('OPAQUE_ROUTE',w,g[w],E[2]) end;
__n151=(__n151 or 0);if g[w]==151 and __n151<25 then
  __n151=(__n151 or 0)+1;
  __st=d[w]+1;__n=L[w];__pw=w;
  local before={}; for i=__st,__st+__n-1 do before[i]=g[i] end;
  __pending={st=__st,n=__n,w=__pw,before=before};
end;
if __pending then
  local i=w;
  if i>=__pending.st and i<__pending.st+__pending.n then
    local b=__pending.before[i]
    print('CHK\\t'..i..'\\tb'..tostring(b)..'\\ta'..tostring(g[i]))
    if i==__pending.st+__pending.n-1 then __pending=nil end
  end
end;
local D,T=g[w];if D<83"""
src=src.replace(needle,hook)
p=R/'7.chk151.lua'; p.write_text(src)
out=R/'7.chk151.log'
with out.open('wb') as f:
    try: subprocess.run(['deps/build/native-unicode',str(p)],stdout=f,stderr=subprocess.STDOUT,timeout=220)
    except subprocess.TimeoutExpired: print('TIMEOUT')
t=out.read_text(errors='replace')
chk=[l for l in t.splitlines() if l.startswith('CHK')]
print('CHK 数',len(chk))
same=sum(1 for l in chk if l.split('\t')[2][1:]==l.split('\t')[3][1:])
print('before == after 的比例',same,'/',len(chk))
for l in chk[:12]: print(l)

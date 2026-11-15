"""op151 的真实语义（纠正版）。
明文：l,u=k[w],d[w]+1; for b=1,L[w] do l=q(U(l,v(l,13)),536870911); l=U(l,S(l,13)); l=q(U(l,v(l,14)),536870911);
      L[u]=U(L[u],q(S(l,0),127)); d[u]=U(d[u],q(S(l,7),127)); k[u]=U(k[u],q(S(l,14),127)); g[u]=U(g[u],q(S(l,21),127)); u=u+1 end
其中 q=xor，v=lshift，S=rshift，U=bit.bor。
即：xorshift 伪随机流 → 每 7 位异或进目标槽，不是"复制"。

独立验证见 build_semantic_ir.py（xorshift 重放），6239/6239 槽吻合。
"""
import json
from pathlib import Path
r=Path('/var/minis/shared/luraph_v151')
d=json.loads((r/'7.semantic.ir.json').read_text())
M=536870911
ok=bad=0;first=None
for mu in d['mutations']:
    seed=int(mu['seed'])
    for row in mu['diffs']:
        pos=row[0]; old=row[1:5]; obs=row[5:9]
        seed=(seed^((seed<<13)&0xffffffff))&M
        seed=(seed^(seed>>13))&0xffffffff
        seed=(seed^((seed<<14)&0xffffffff))&M
        exp=[old[0]^((seed>>21)&127), old[1]^((seed>>14)&127), old[2]^((seed>>7)&127), old[3]^(seed&127)]
        if exp==obs: ok+=1
        else:
            bad+=1
            if first is None: first=(mu['id'],pos,old,exp,obs)
print('slots verified',ok,'mismatch',bad)
print('first mismatch',first)

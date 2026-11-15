"""按版本顺序重放全部 op151 mutation，重建每个版本的 g/k/d/L 表。
起点：7.dispatch.ir.csv 的静态快照（version 0）。"""
import json
from pathlib import Path
r=Path('/var/minis/shared/luraph_v151')
M=536870911
# version 0
tbl={c:{} for c in 'gkLd'}
for line in (r/'7.dispatch.ir.csv').read_text().splitlines()[1:]:
    f=line.split(',')
    if len(f)<5 or any(x=='' for x in f): continue
    pc=int(f[0]); tbl['g'][pc]=int(f[1]); tbl['k'][pc]=int(f[2]); tbl['d'][pc]=int(f[3]); tbl['L'][pc]=int(f[4])
d=json.loads((r/'7.semantic.ir.json').read_text())
vers={}
for mu in d['mutations']:
    vers.setdefault(int(mu['version']),[]).append(mu)
out={}
for v in sorted(vers):
    for mu in vers[v]:
        seed=int(mu['seed']); start=int(mu['start']); count=int(mu['count'])
        for u in range(start,start+count):
            seed=(seed^((seed<<13)&0xffffffff))&M
            seed=(seed^(seed>>13))&0xffffffff
            seed=(seed^((seed<<14)&0xffffffff))&M
            tbl['L'][u]=tbl['L'].get(u,0)^(seed&127)
            tbl['d'][u]=tbl['d'].get(u,0)^((seed>>7)&127)
            tbl['k'][u]=tbl['k'].get(u,0)^((seed>>14)&127)
            tbl['g'][u]=tbl['g'].get(u,0)^((seed>>21)&127)
    out[v]={c:dict(tbl[c]) for c in 'gkLd'}
tot=len(vers)
print('versions replayed',tot)
last=max(vers)
(r/'7.dispatch.final.json').write_text(json.dumps({'version':last,'g':tbl['g'],'k':tbl['k'],'d':tbl['d'],'L':tbl['L']}))
print('final version',last,'slots',len(tbl['g']))

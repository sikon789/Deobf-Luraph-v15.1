"""用真实轨迹重建分派表：
轨迹每步带 op151_version，op 就是该时刻的真实操作码。
按 version 分组取多数（同一 PC 同版本应稳定），输出每个版本的 (pc,direct op) 表。"""
import json
from pathlib import Path
from collections import defaultdict
r=Path('/var/minis/shared/luraph_v151')
steps=json.loads((r/'7.semantic.ir.json').read_text())['steps']
tbl=defaultdict(lambda: defaultdict(list))
for s in steps:
    v=int(s['op151_version']); pc=int(s['pc']); op=int(s['opcode'])
    tbl[v][pc].append(op)
# 检查同 (v,pc) 是否一致
conflicts=0
for v in tbl:
    for pc,ops in tbl[v].items():
        if len(set(ops))>1: conflicts+=1
print('版本数',len(tbl),'(v,pc) 冲突数',conflicts)
for v in sorted(tbl):
    print(f'v{v}: {len(tbl[v])} 个 PC, {sum(len(x) for x in tbl[v].values())} 步')
out={str(v):{str(pc):ops[0] for pc,ops in d.items()} for v,d in tbl.items()}
(r/'7.dispatch.by_version.json').write_text(json.dumps(out))
print('写出 7.dispatch.by_version.json')

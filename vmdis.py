"""用真实轨迹重建的 v20 表反编译。
opcode -> 语义体：优先用 mode64 语义表（167 项，按 opcode 精确索引）。
pc 不在该版本表里时明确标注 out-of-version，不猜。"""
import json,re,sys
from pathlib import Path
r=Path('/var/minis/shared/luraph_v151')
VER=json.loads((r/'7.dispatch.by_version.json').read_text())
sem=json.loads((r/'7.all_modes.semantics.json').read_text())['modes']['64']['opcodes']
BY={}
for e in sem:
    op=e.get('opcode')
    lo=e['integer_region']['lower_inclusive'];hi=e['integer_region']['upper_inclusive']
    if op is not None: BY[int(op)]=e
    elif lo is not None and hi is not None:
        for x in range(lo,hi+1): BY.setdefault(x,e)
def clean(s):
    s=re.sub(r'\n\s*do\s*\n','\n',s); s=re.sub(r'\n\s*end\s*\n','\n',s)
    return ' '.join(x.strip() for x in s.splitlines() if x.strip())
def dis(pc,ver='20'):
    t=VER[ver]
    op=t.get(str(pc))
    if op is None: return f'{pc}\t(该版本轨迹无此 PC，未执行)'
    e=BY.get(op)
    body=clean(e['body_lua']) if e else f'(opcode {op} 无语义)'
    return f'{pc}\top{op}\t{body[:140]}'
if __name__=='__main__':
    a,b=int(sys.argv[1]),int(sys.argv[2])
    for pc in range(a,b+1): print(dis(pc))

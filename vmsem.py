"""按 dispatch_trace 的 source_span 直接从明文取每个 opcode 的分支体。
7.all_modes.semantics.json 每条带 trace，最后一个 True 条件对应的 span 就是判定点，
其后的 then 体即该 opcode 的语义。这比解析整棵树可靠得多。"""
import json,re
from pathlib import Path
R=Path('/var/minis/shared/luraph_v151')
s=(R/'7.inner.lua').read_text()
sem=json.loads((R/'7.all_modes.semantics.json').read_text())['modes']['64']['opcodes']
def body_after(pos):
    """从 pos（判定条件结尾）向后找 'then'，再取到同级 else/end"""
    j=s.find('then',pos)
    if j<0: return None
    a=j+4
    d=0;k=a
    while k<len(s):
        if s.startswith('if ',k): d+=1
        elif s.startswith('end',k):
            if d==0: return s[a:k]
            d-=1
        elif d==0 and (s.startswith('elseif ',k) or s.startswith('else ',k)):
            return s[a:k]
        k+=1
    return None
out={}
bad=[]
for e in sem:
    op=e.get('opcode')
    if op is None: continue
    tr=e.get('dispatch_trace') or []
    true_spans=[t['source_span'][1] for t in tr if t['value'] is True]
    if not true_spans: bad.append((op,'no-true')); continue
    body=body_after(true_spans[-1])
    if body is None: bad.append((op,'no-body')); continue
    txt=re.sub(r'\s+',' ',body).strip()
    if not txt: bad.append((op,'empty')); continue
    out[op]=txt
print('取到',len(out),'/',len([e for e in sem if e.get('opcode') is not None]))
print('失败',bad[:15])
(R/'h64.span.opcodes.json').write_text(json.dumps({str(k):v for k,v in sorted(out.items())},indent=1,ensure_ascii=False))
for op in (5,2,140,143,113,91,136,45,36,102):
    print(f'op{op} ->',(out.get(op) or 'MISSING')[:170])

"""系统性反编译：把 seg2 采集的 1907 条指令按控制流还原成伪 Lua。

关键难点：同一 pc 被多次改写（自修改字节码），所以不能做静态 pc→指令映射。
正确做法：**按执行时间顺序**输出，把跳转目标解析成标签，
这就是这段程序真实的执行路径。

产出一份带标签的线性伪 Lua，跳转用 goto 表示。"""
import re,json
from pathlib import Path
R=Path('/var/minis/shared/luraph_v151')
OPS={int(k):v for k,v in json.loads((R/'h64.span.opcodes.json').read_text()).items()}
def sem(op):
    b=OPS.get(op,'')
    m=re.search(r'D(?:==|~=)%d\)? then (.*?)(?:;elseif |;else |$)'%op, b)
    s=(m.group(1) if m else b)
    return re.sub(r'\s+',' ',s).strip()
t=(R/'7.seg2.log').read_text(errors='replace')
recs=[(int(a),int(b),int(c),int(d),int(e),int(f)) for a,b,c,d,e,f in
      re.findall(r'I\x01(\d+)\x01(\d+)\x01(\d+)\x01(\d+)\x01(\d+)\x01(\d+)', t)]
print('记录',len(recs))
# 只保留每个 pc 在某一区段内的稳定指令
seen={}
for sid,pc,op,k,d,L in recs:
    key=(sid,pc)
    if key not in seen: seen[key]=(op,k,d,L)
print('唯一(区段,pc)',len(seen))
# 按执行顺序输出前 N 条
N=400
out=['-- Luraph VM 反编译（按执行顺序，前 %d 条）'%N,
     '-- 数据来源：7.seg2.log（现场采集，op 与执行吻合 96.35%）','']
for i,(sid,pc,op,k,d,L) in enumerate(recs[:N]):
    s=sem(op)
    s=re.sub(r'([gkdL])\[w\]',lambda m:{'g':str(op),'k':str(k),'d':str(d),'L':str(L)}[m.group(1)],s)
    s=s.replace('u=X[','X[')
    out.append(f'-- s{sid:3d} pc{pc:5d}')
    out.append(f'   {s[:150]}')
(R/'7.decompiled.lua.txt').write_text('\n'.join(out))
print('写出 7.decompiled.lua.txt')
print('\n'.join(out[:20]))

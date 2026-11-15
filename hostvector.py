from pathlib import Path
import subprocess
r=Path(__file__).parent;b=r/'deps/build';inc=r/'deps/luau-0.746'
s=(b/'native_resume_main.cpp').read_text()
anchor='luaL_openlibs(L);'
assert s.count(anchor)==1
s='void register_vector_properties(struct lua_State*);\n'+s.replace(anchor,anchor+'register_vector_properties(L);')
p=b/'native_vector_main.cpp';p.write_text(s)
cmd=['g++','-O2','-std=c++17','-I'+str(inc/'VM/include'),'-I'+str(inc/'Compiler/include'),'-I'+str(inc/'Common/include'),str(p)]
cmd += [str(r/x) for x in ['native_host_instances.cpp','native_capture_loader.cpp','native_vector_properties.cpp']]
cmd += [str(b/f'libLuau.{x}.a') for x in ['Compiler','Ast','Bytecode','VM','Common']]
cmd += ['-lpthread','-ldl','-lm','-o',str(b/'native-vector')]
subprocess.run(cmd,check=True)
with (r/'7.vector-properties.log').open('wb') as f:
 subprocess.run([str(b/'native-vector'),str(r/'7.cframe-math.lua')],cwd=r,stdout=f,stderr=subprocess.STDOUT,timeout=25)
print((r/'7.vector-properties.log').read_text()[-3000:])

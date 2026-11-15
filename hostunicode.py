from pathlib import Path
import subprocess
r=Path(__file__).parent;b=r/'deps/build';inc=r/'deps/luau-0.746'
s=(b/'native_vector_main.cpp').read_text()
a='luaL_openlibs(L);';assert s.count(a)==1
s='void register_native_unicode(struct lua_State*);\n'+s.replace(a,a+'register_native_unicode(L);')
p=b/'native_unicode_main.cpp';p.write_text(s)
cmd=['g++','-O2','-std=c++17']+['-I'+str(inc/x/'include') for x in ['VM','Compiler','Common']]
cmd += [str(p)]+[str(r/x) for x in ['native_path2d_instances.cpp','native_capture_loader.cpp','native_vector_properties.cpp','native_unicode.cpp']]
cmd += [str(b/f'libLuau.{x}.a') for x in ['Compiler','Ast','Bytecode','VM','Common']]
subprocess.run(cmd+['-lutf8proc','-lpthread','-ldl','-lm','-o',str(b/'native-unicode')],check=True)

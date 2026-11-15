"""Independent bounded runner. Does not alter VM predicates/instructions."""
from pathlib import Path
import subprocess
import hashlib
r = Path(__file__).resolve().parent
source = (r/'7.path-input-clean.lua').read_text()
a = source.index('local __pathrecords={}\n')
b = source.index('local PAY = buffer.fromstring(', a)
source = source[:a] + (r/'path2d_geometry_model.lua').read_text() + '\n' + source[b:]
# Keep the original diagnostic condition and its stop. Only defer logging.
a = source.index(' print(\'NATURAL_NUMERIC_RESULT\',E[2],E[3],E[173]);')
b = source.index(" error('NATURAL_NUMERIC_BOUND',0)", a)
source = source[:a] + ' __pathgate={E[2],E[3],E[173]};\n' + source[b:]
# Gate storage declared outside VM, not inside deeply nested functions.
source = 'local __pathgate=nil\n' + source
needle = '\n__run()\n'
assert source.count(needle) == 1
source = source.replace(needle, '''
local __runok,__runerr=pcall(__run)
print('PATH_RUN',__runok,__runerr)
if __pathgate then print('NATURAL_NUMERIC_RESULT',unpack(__pathgate)) end
__PATH_DUMP()
for i=math.max(1,#__naturalvalues-35),#__naturalvalues do
 local a=__naturalvalues[i];print('NATURAL_VALUE',a[1],type(a[2]),tostring(a[2]))
end
''')
output = r/'7.path2d-geometry.lua'
output.write_text(source)
host = r/'deps/build/native-unicode'
if not host.exists(): host=r/'deps/build/native-path2d'
log = r/'7.path2d-geometry.log'
print('HOST',host,'MODEL_SHA256',hashlib.sha256((r/'path2d_geometry_model.lua').read_bytes()).hexdigest())
with log.open('wb') as f:
 try:
  result=subprocess.run([str(host),str(output)],cwd=r,stdout=f,stderr=subprocess.STDOUT,timeout=25)
  print('EXIT',result.returncode)
 except subprocess.TimeoutExpired:
  print('TIMEOUT_25S')
print(log.read_text()[-14000:])

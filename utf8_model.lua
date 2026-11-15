-- Preserve original native Unicode primitives; normalization is unresolved.
do
 local native=utf8
 local u={}
 for k,v in pairs(native) do u[k]=v end
 -- Do not replace NFC with identity: unsupported normalization must stop honestly.
 STUBS.utf8=u
end

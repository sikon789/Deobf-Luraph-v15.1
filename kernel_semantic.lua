-- Luraph v15.1 反混淆产品：主控函数已语义化
-- 规则：m[数字] 已替换为 VM 原语真实 API 名

-- ===== r6 (原始长度 353) =====
function(m,j,b,T,v,r,O,w,F)if T<=23 then return 1;elseif T<=24 then local T=vm.buffer_readu8(r,3+v);local q,k,l,V,I=b-128,(O-128)*16384,128*(j-128),2097152*(T%128),T%128;local j=2097152*(T-I);I=k+q+(l+(j+V));return 2,42,w,r,4+v,F,I;else local j,T=w[1],vm.string_gsub(vm.string_sub(m.F6,5),m.p6,m.l6);local v,r,O=vm.buffer_fromstring(T),#T-1,5+0;T=0-O;return 2,41,{nil,O,r+0,T,j},0,{},v,b;end;end

-- ===== v6 (原始长度 332) =====
function(m,j,b,T,v,r,O,w,F,q)if w<=40 then local k=(r-128)*128+(b+(F-128)*16384);return 28,3+v,T,j,k;elseif w<=41 then local b,w,F=O[4],O[2],O[3];local k,l=b+w,w<=0;w,b=k>=F,k<=F;F=l and w or not l and b;O[4]=k;if F then return 3,v,k,j,r;else return 7,v,T,j,r;end;else local j=vm.buffer_readu8(q,v);return not(j<128)and 29 or 1,v,T,j,r;end;end

-- ===== e6 (原始长度 274) =====
function(m,j,b,T,v,r,O,w,F,q)if v<=18 then local k=128*(q-128)+F;return 28,b,O+2,T,k;elseif v<=19 then local v=vm.buffer_readu8(b,2+O);return not(v>=128)and 16 or 24,b,O,v,q;else local v=vm.buffer_create(T);vm.buffer_copy(v,0,b,O,T);local b=T+O;r[w]=v;m[2]=b;return 23,m:L6(r,j,169)(nil,m.D),O,T,q;end;end

-- ===== s6 (原始长度 72) =====
function(m)return true,8,nil,nil,nil,nil,nil,nil,nil,nil,nil,nil,nil;end

-- ===== g6 (原始长度 240) =====
function(m,j,b,T,v,r,O,w,F,q,k)if j<=26 then local l,V=85*(w-O),(T-39)*614125;local O=7225*(b-39)+((q-39)*1+(l+v))+V;r[k]=O;return 35,O,b;elseif j<=27 then local j=vm.buffer_readu8(F,r+1);return j<128 and 18 or 21,w,j;else q[k]=T;return 38,w,b;end;end

-- ===== d6 (原始长度 146) =====
function(m,j,b,T,v,r,O)if v<=21 then local v=vm.buffer_readu8(b,2+r);return not(128>v)and 15 or 40,r,O,v;else local m=(O-128)*128+j;return 20,r+2,m,T;end;end

-- ===== k6 (原始长度 851) =====
function(m,...)local j,b,T,v,r,O,w,F,q,k,l,V,I=m:s6();local P,S,K,W,H,z,Q,o,n,E,p,c=b,T,v,r,O,w,F,q,k,l,V,I;while j do if P<=20 then if P<=9 then if P<=4 then P,W,z,Q,o,n,E=m:j6(W,Q,P,H,o,K,z,n,E);elseif P<=6 then P,W,H,Q=m:K6(Q,H,o,W,P,S);else P,S,K,W,H,z,n=m:u6(S,W,K,n,z,P,H);end;elseif P<=14 then P,W,Q=m:G6(K,Q,P,H,W);elseif P<=17 then P,W,z,o,n=m:O6(K,P,E,n,o,Q,p,W,z);else P,K,W,o,n=m:e6(z,K,o,P,H,W,Q,E,n);end;elseif P<=31 then if P<=25 then if P<=22 then P,W,o,p=m:d6(n,K,p,P,W,o);else b,l,r,T,I,v,V=m:r6(o,z,P,W,K,Q,S,H);if b==1 then return K;elseif b==2 then P,S,K,W,H,z=l,r,T,I,v,V;end;end;elseif P<=28 then P,z,E=m:g6(P,E,n,p,W,c,z,K,Q,o);else P,z,o,n,E,p,c=m:o6(n,z,P,K,p,c,W,o,E);end;elseif P<=36 then P,K,W,z,Q,o=m:H6(Q,P,z,K,o,H,W,n,E);elseif P<=39 then P,S,W,Q,o=m:X6(o,W,K,Q,S,H,P);else P,W,z,Q,n=m:v6(Q,p,z,W,n,S,P,E,K);end;end;end

-- ===== O6 (原始长度 427) =====
function(m,j,b,T,v,r,O,w,F,q)if b<=15 then local k=vm.buffer_readu8(j,3+F);local l,V,I,P,S=v-128,(T-128)*16384,(w-128)*128,k%128*2097152,k%128;local w=(k-S)*2097152;k=P+V+(l+w+I);return 28,4+F,q,r,k;elseif b<=16 then local b,w=128*(q-128),16384*(O-128);local O=b+r+w;return 42,3+F,O,r,v;else local b=vm.buffer_readu8(j,3+F);local m,j,O,w=r-128,16384*(v-128),128*(T-128),b%128*2097152;local T=(b-b%128)*2097152+(m+(j+O)+w);return 20,4+F,q,T,v;end;end

-- ===== o6 (原始长度 312) =====
function(m,j,b,T,v,r,O,w,F,q)if T<=29 then local k=vm.buffer_readu8(v,1+w);return not(k>=128)and 5 or 31,b,k,j,q,r,O;elseif T<=30 then local j=b%256;local T=(b-j)/256;local k=T%256;T=(T-k)/256;local l=T%256;return 26,k,F,l,(T-l)/256,(j-39)*52200625,39;else local j=vm.buffer_readu8(v,2+w);return 128>j and 36 or 32,b,F,j,q,r,O;end;end

-- ===== u6 (原始长度 289) =====
function(m,j,b,T,v,r,O,w)if O<=7 then local F=j[5];m.P=w;local q,k=m.P,m[2];local l=vm.buffer_readu8(q,k);return not(128<=l)and 14 or 13,F,q,k,{},l,v;elseif O<=8 then local O=1+0;return 6,{j,0-O,255+0,O,nil},133,25,w,r,v;else local v=vm.buffer_readu8(T,b+1);return not not(v>=128)and 0 or 22,j,T,b,w,r,v;end;end

-- ===== K6 (原始长度 231) =====
function(m,m,j,b,T,v,r)if v<=5 then local v=(m-128)*128+b;return 37,T+2,j,v;else local b,v,O=r[2],r[4],r[3];local w,F=b+v,v<=0;v,b=w>=O,w<=O;O=F and v or not F and b;r[2]=w;if O then return 10,T,w,m;else return 25,T,j,m;end;end;end

-- ===== X6 (原始长度 350) =====
function(m,j,b,T,v,r,O,w)if w<=37 then local F,q,k=v-83470,vm.buffer_readu8(T,b),1+b;O[7]=not(q==0);q=vm.table_create(F);O[5]=q;local m=1+0;return 38,{r,1-m,m,nil,F+0},k,q,j;elseif w<=38 then local m,T,O=r[2],r[3],r[5];local w,F=m+T,T<=0;m,T=w>=O,w<=O;O=F and m or not F and T;r[2]=w;if O then return 4,r,b,v,w;else return 39,r,b,v,j;end;else return 2,r[1],b,v,j;end;end

-- ===== G6 (原始长度 376) =====
function(m,j,b,T,v,r)if T<=11 then if T<=10 then local O=(v*j+r)%256;local w=(r+O*j)%256;local F=(r+w*j)%256;local q=(r+F*j)%256;local k,l,V,I=m.P6,256*w,65536*F,q*16777216;k[v]=l+O+(V+I);m.M6[v]=q;return 6,r,b;else return 28,r+1,b;end;elseif T<=12 then return 20,r+1,b;elseif T<=13 then local T=vm.buffer_readu8(j,1+r);return not not(T>=128)and 19 or 33,r,T;else return 42,r+1,b;end;end

-- ===== H6 (原始长度 462) =====
function(m,j,b,T,v,r,O,w,F,q)if b<=33 then if b<=32 then local k=vm.buffer_readu8(v,3+w);local l,V,I,P=j-128,(r-128)*16384,(F-128)*128,k%128*2097152;local S=l+2097152*(k-k%128)+(P+(I+V));return 37,v,w+4,T,S,r;else local k=j+(T-128)*128;return 42,v,w+2,k,j,r;end;elseif b<=34 then local k=128*(r-128)+((F-128)*16384+q);return 20,v,3+w,T,j,k;elseif b<=35 then vm.buffer_writeu32(O,v,T);return 41,v+4,w,T,j,r;else local m=128*(j-128);local j=16384*(r-128)+F+m;return 37,v,w+3,T,j,r;end;end

-- ===== j6 (原始长度 465) =====
function(m,j,b,T,v,r,O,w,F,q)if T<=1 then if T<=0 then local k=vm.buffer_readu8(O,j+2);return not not(128<=k)and 17 or 34,j,w,b,r,F,k;else return 37,j+1,w,b,r,F,q;end;elseif T<=2 then local k=vm.buffer_readu8(O,j);return not not(128<=k)and 9 or 12,j,w,4,k,F,q;elseif T<=3 then local T,k=vm.buffer_readu32(v,w),vm.buffer_readu8(v,4+w);local v=4294967296*k+T;local l=j[v];if not not l then return 35,j,l,b,r,F,q;else return 30,j,T,k,v,F,q;end;else local T=vm.buffer_readu8(O,j);return 128>T and 11 or 27,j,w,b,r,T,q;end;end

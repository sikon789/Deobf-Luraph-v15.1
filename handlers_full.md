# Luraph v15.1 Handler 全量剖析

样本：`8.lua` (329241 字节)

handler 数：76


## `A`  (2,227592 - 2,227979)

参数: m, j, b, T, v, r, O, w, F, q, k, l, V  长度: 387

```lua
function(m,j,b,T,v,r,O,w,F,q,k,l,V)if T<=138 then if T<=137 then local I=(F-128)*128+v;return 61,2+V,I,q,O,k;else b[l]=w;return 160,V,F,q,O,k;end;elseif T<=139 then local b=m[27](j,V);return not not(128<=b)and 50 or 56,V,F,b,O,k;elseif T<=140 then local b=(O-128)*128;local T=r+((k-128)*16384+b);return 88,3+V,F,q,T,k;else local b=m[27](j,1+V);return 128>b and 2 or 115,V,F,q,O,b;end;end
```


## `B`  (2,298710 - 2,299124)

参数: m, j, b, T, v, r, O, w, F, q  长度: 414

```lua
function(m,j,b,T,v,r,O,w,F,q)if b<=148 then if b<=147 then local k=(F-128)*128+r;return 144,O,2+T,w,q,k,j;else local r=q-73306;local k,l,V=m[118](r),m[118](r),1+0;return 58,{nil,V,1-V,O,r+0},T,w,k,l,j;end;elseif b<=149 then local r=m[27](v,2+T);return not not(r>=128)and 98 or 48,O,T,w,q,F,r;elseif b<=150 then return 61,O,T+1,w,q,F,j;else local b=m[27](v,2);return not not(b>=128)and 128 or 20,O,T,b,q,F,j;end;end
```


## `C`  (2,238021 - 2,238440)

参数: m, j, b, T, v, r, O, w  长度: 419

```lua
function(m,j,b,T,v,r,O,w)if v<=134 then local F,q,k=O[5],O[3],O[2];local l,V=F+q,q<=0;q,F=l>=k,l<=k;k=V and q or not V and F;O[5]=l;if k then return 139,l,r,j;else return 32,T,r,j;end;elseif v<=135 then local v=m[27](w,b);return not not(128<=v)and 24 or 64,T,v,j;else local m,b,v=O[3],O[2],O[4];local w,F=m+b,b<=0;m,b=w>=v,w<=v;v=F and m or not F and b;O[3]=w;if v then return 51,T,r,w;else return 158,T,r,j;end;end;end
```


## `E`  (2,297074 - 2,297224)

参数: m, j, b, T, v, r, O  长度: 150

```lua
function(m,j,b,T,v,r,O)if j<=152 then local j=m[27](T,v);return not not(j>=128)and 132 or 4,v,b,j;else local m=(b-128)*128+O;return 11,v+2,m,r;end;end
```


## `F`  (2,263406 - 2,263729)

参数: m, j, b, T, v, r, O, w  长度: 323

```lua
function(m,j,b,T,v,r,O,w)if v<=88 then local F=m[27](b,T);return F<128 and 30 or 92,F,w,O;elseif v<=89 then local v,F,q=j[4],j[2],j[5];local k,l=v+F,F<=0;v,F=k>=q,k<=q;q=l and v or not l and F;j[4]=k;if q then return 49,r,w,k;else return 31,r,w,O;end;else local j=m[27](b,2+T);return not(128<=j)and 140 or 156,r,j,O;end;end
```


## `G`  (2,230063 - 2,230483)

参数: m, j, b, T, v, r, O, w, F, q, k  长度: 420

```lua
function(m,j,b,T,v,r,O,w,F,q,k)if j<=36 then if j<=35 then local l=m[27](r,k+1);return not(l>=128)and 59 or 162,T,k,l,q,v;else local l=m[27](r,2+k);return not(128<=l)and 54 or 83,T,k,F,q,l;end;elseif j<=37 then local l,V,I=m[27](r,3+k),q-128,(O-128)*16384;local m=V+((w-128)*128+(l%128*2097152+2097152*(l-l%128)+I));return 119,T,k+4,F,m,v;elseif j<=38 then b[q]=O;return 58,T,k,F,q,v;else return 135,T[4],k,F,q,v;end;end
```


## `H`  (2,264895 - 2,265190)

参数: m, j, b, T, v, r, O, w, F, q, k, l  长度: 295

```lua
function(m,j,b,T,v,r,O,w,F,q,k,l)if T<=71 then if T<=70 then local V=m[27](F,j+2);return not not(V>=128)and 107 or 3,v,l,V,k;else local m=r+(k-128)*128;return 148,v,l+2,q,m;end;elseif T<=72 then return 19,v,l+1,q,k;elseif T<=73 then return 33,v[3],l,q,k;else b[O]=w-w%1;return 22,v,l,q,k;end;end
```


## `I`  (2,297227 - 2,297564)

参数: m, j, b, T, v, r, O, w  长度: 337

```lua
function(m,j,b,T,v,r,O,w)if v<=160 then local F,q,k=T[4],T[2],T[3];local l,V=F+q,q<=0;F,q=l>=k,l<=k;k=V and F or not V and q;T[4]=l;if k then return 79,O,j,l;else return 131,O,j,r;end;elseif v<=161 then local T=m[27](b,2+w);return not not(128<=T)and 7 or 27,O,T,r;else local T=m[27](b,2+w);return not not(128<=T)and 13 or 8,T,j,r;end;end
```


## `K`  (2,264239 - 2,264519)

参数: m, j, b, T, v, r, O, w, F, q, k  长度: 280

```lua
function(m,j,b,T,v,r,O,w,F,q,k)if T<=27 then local l=(w-128)*128;local V=b+16384*(F-128)+l;return 61,O,j+3,v,V,q,r;elseif T<=28 then local b=m[27](k,1);return not(b>=128)and 109 or 151,O,j,b,w,q,r;else local b,T,r=m[67](k,j),4+j,1+0;return 136,{nil,r,1-r,b+0,O},T,v,w,1,{};end;end
```


## `L`  (2,229145 - 2,229178)

参数: m  长度: 33

```lua
function(m,...)(...)[...]=nil;end
```


## `N`  (2,299339 - 2,328687)

参数: y, y  长度: 29348

```lua
local function N(y,y)local u,_,A,G,t,a,U,x,i,d,X,g,f,C,M,D,B,mU,jU,bU=P,S,K,W,H,z,Q,o,n,E,p,c,s,R,L,Z,J,e,Y,h;local function P(...)local S,K=942185312;local W,H,z,Q=1954318648;local o,n,E=u;local p=1471330291;local c,s,R=o(b),r,q;local b,r,q,L,Z,J,e,Y,h,u,TU,vU,rU,OU,wU,FU,qU=_(),d,X,U,G,t,a,x,i,g,f,C,M,D,B,mU,jU;local _,G,t,a,U=A(function(...)local A,x,i,d,X,g,f,C,M;local D=R==172;if D then while true do local B=T[s];local mU=B<32;if mU then local mU=B<16;if mU then local mU=B>=8;if mU then local mU=B<12;if mU then local mU=B>=10;if mU then local mU=B==11;if mU then g=w[s];i,C,f=c[g],c[g+1],c[g+2];c[g]=i(C,f);else local mU,jU,kU=w[s],l[s],V[s];local lU,VU=Z(jU,4294967295),Z(kU,4294967295);local jU,IU,PU,SU=Z(lU,65535),J(lU,16),Z(VU,65535),J(VU,16);kU=Z(jU*PU+e(Z(jU*SU+IU*PU,65535),16),4294967295);SU=nil;repeat lU=kU%4294967296;if lU~=lU then SU=0;break;end;SU=lU-lU%1;until true;c[mU]=SU;end;else local mU=B~=9;if mU then g=y[V[s]];c[w[s]]=g[4][g[6]];else g,i,C=V[s],w[s],F[s];f=c[g];L(c,g+1,g+i,C+1,f);end;end;else local mU=B>=14;if mU then local mU=B~=15;if mU then c[V[s]]=m[F[s]];c[V[s+1]]=F[s+1];c[V[s+2]]=F[s+2];c[V[s+3]]=c[w[s+3]];s+=3;else s=V[s];end;else local mU=B~=13;if mU then g,i=V[s]+1,F[s];local mU=s;for jU=1,w[mU],1 do i=Z(Y(i,(e(i,13))),536870911);i=Y(i,(J(i,13)));i=Z(Y(i,(e(i,14))),536870911);V[g]=Y(V[g],(Z(J(i,0),127)));w[g]=Y(w[g],(Z(J(i,7),127)));F[g]=Y(F[g],(Z(J(i,14),127)));T[g]=Y(T[g],(Z(J(i,21),127)));g=g+1;end;T[s]=55;else g=w[s];i,C,f=c[g],c[g+1],c[g+2];c[g]=i(C,f);c[V[s+1]]=c[w[s+1]];s+=1;end;end;end;else local mU=B>=4;if mU then local mU=B<6;if mU then local mU=B~=5;if mU then c[F[s]]=c[V[s]]();else W=c[V[s]];end;else local mU=B~=7;if mU then local mU=c[w[s]]==F[s];if mU then s=V[s];end;else g,i,C,f=V[s],w[s],F[s],Y(W,Z(J(W,14),262143),(Z(J(W,28),15)));M=g<16384 and 7 or(g<2097152 and 14 or 21);d,A=J(g,M),Z(g,e(1,M)-1);local mU=s;w[mU]=Y(i,6,(Z(J(f,7),127)));mU=s;V[mU]=Y(A,41,(Z(f,127)));mU=s;F[mU]=Y(C,11,(Z(J(f,14),127)));mU=s;T[mU]=Y(d,73,(Z(J(f,21),127)));s-=1;end;end;else local mU=B>=2;if mU then local mU=B==3;if mU then c[V[s]]=p;else c[V[s]]=#c[w[s]];end;else local mU=B==1;if mU then c[F[s]]=y[V[s]][c[w[s]]];else c[F[s]]=b[k[s]];end;end;end;end;else local mU=B>=24;if mU then local mU=B<28;if mU then local mU=B<26;if mU then local mU=B==25;if mU then c[w[s]]=c[F[s]](k[s]);else g,i,C=F[s],w[s],V[s];f,M,d=g+C-1,g+i,h(c[g](r(c,g+1,g+i)));L(d,1,C,g,c);end;else local mU=B==27;if mU then c[V[s]]=y[F[s]];else g,i={...},V[s];L(g,1,F[s],i,c);end;end;else local mU=B<30;if mU then local mU=B~=29;if mU then c[V[s]]=c[w[s]];else local mU,jU=n,E;if mU then for kU in q,mU,nil do if mU then local lU=mU[kU];if lU then lU[4]=lU;lU[5]=c[kU];lU[6]=5;mU[kU]=nil;end;end;end;end;if jU then for kU,lU in q,jU,nil do mU=lU[5];if jU then local lU=jU[kU];if lU then local VU,IU=kU+mU-1,o(mU);L(c,kU,VU,1,IU);lU[4]=IU;lU[6]=1;jU[kU]=nil;end;end;end;end;local mU,jU,kU=w[s],c[F[s]],c[V[s]];return true,true,mU,h(jU,kU);end;else local mU=B~=31;if mU then R=w[s];s=F[s]+1;break;else s=c[F[s]];end;end;end;else local mU=B<20;if mU then local mU=B<18;if mU then local mU=B==17;if mU then c[w[s]]=c[V[s]]+c[F[s]];else local mU,jU,kU=V[s],c[F[s]],c[w[s]];local lU,VU=Z(jU,4294967295),Z(kU,4294967295);local kU,IU,PU,SU=Z(lU,65535),J(lU,16),Z(VU,65535),J(VU,16);jU=Z(kU*PU+e(Z(kU*SU+IU*PU,65535),16),4294967295);kU=nil;repeat SU=jU%4294967296;if SU~=SU then kU=0;break;end;kU=SU-SU%1;until true;c[mU]=kU;end;else local mU=B==19;if mU then g,i=V[s]+1,Y(w[s],(Z(Y(W,(Z(J(W,29),7))),536870911)));local mU=s;for jU=1,F[mU],1 do i=Z(Y(i,(e(i,13))),536870911);i=Y(i,(J(i,13)));i=Z(Y(i,(e(i,14))),536870911);V[g]=Y(V[g],(Z(J(i,0),127)));w[g]=Y(w[g],(Z(J(i,7),127)));F[g]=Y(F[g],(Z(J(i,14),127)));T[g]=Y(T[g],(Z(J(i,21),127)));g=g+1;end;T[s]=55;else c[w[s]][c[V[s]]]=c[F[s]];end;end;else local mU=B>=22;if mU then local mU=B==23;if mU then c[V[s]]=m[F[s]];c[V[s+1]]=F[s+1];c[V[s+2]]=F[s+2];s+=2;else local mU,jU,kU=w[s],V[s],F[s];local lU,VU=Z(jU,4294967295),Z(kU,4294967295);local jU,IU,PU,SU=Z(lU,65535),J(lU,16),Z(VU,65535),J(VU,16);lU=Z(jU*PU+e(Z(jU*SU+IU*PU,65535),16),4294967295);kU=nil;repeat VU=lU%4294967296;if VU~=VU then kU=0;break;end;kU=VU-VU%1;until true;c[mU]=kU;end;else local mU=B==21;if mU then c[V[s]]=F[s];else c[V[s]]=m[F[s]];end;end;end;end;end;else local mU=B>=48;if mU then local mU=B<56;if mU then local mU=B>=52;if mU then local mU=B<54;if mU then local mU=B~=53;if mU then p=c[w[s]];else g,i,C=V[s],{...},w[s];L(i,1,g-1,C,c);c[C+g-1]=h(u(g,...));end;else local u=B==55;if u then else g,i=w[s],c[F[s]];c[g+1]=i;c[g]=i[k[s]];end;end;else local u=B<50;if u then local u=B~=49;if u then c[w[s]]=not c[V[s]];else local u,mU,jU=F[s],w[s],v[5];local kU=Y(jU[u],418689291);jU[u]=kU;jU,u=v[4],kU+1;kU=TU(jU,u);local lU,VU;if kU<128 then lU,VU=kU,u+1;else local IU=TU(jU,u+1);if IU<128 then lU,VU=(kU-128)*128+IU,u+2;else local PU=TU(jU,u+2);if PU<128 then lU,VU=(kU-128)*128+(IU-128)*16384+PU,u+3;else local SU=TU(jU,u+3);lU,VU=kU-128+(IU-128)*16384+(PU-128)*128+SU%128*2097152+(SU-SU%128)*2097152,u+4;end;end;end;kU,u=mU*16843009,VU+lU;local IU=u-lU%4;for PU=VU,IU-1,4 do vU(jU,PU,(Y(rU(jU,PU),kU)));end;for kU=IU,u-1,1 do OU(jU,kU,(Y(TU(jU,kU),mU)));end;u,IU,lU=s,s,s;F[s]=93;w[u]=81;V[IU]=189;T[lU]=55;end;else local u=B==51;if u then g,i=V[s]+1,Y(w[s],(Z(Y(p,(Z(J(p,29),7))),536870911)));local u=s;for mU=1,F[u],1 do i=Z(Y(i,(e(i,13))),536870911);i=Y(i,(J(i,13)));i=Z(Y(i,(e(i,14))),536870911);V[g]=Y(V[g],(Z(J(i,0),127)));w[g]=Y(w[g],(Z(J(i,7),127)));F[g]=Y(F[g],(Z(J(i,14),127)));T[g]=Y(T[g],(Z(J(i,21),127)));g=g+1;end;T[s]=55;else c[F[s]](c[w[s]]);end;end;end;else local u=B>=60;if u then local u=B>=62;if u then local u=B==63;if u then local u,mU=n,E;if u then for jU in q,u,nil do if u then local kU=u[jU];if kU then kU[4]=kU;kU[5]=c[jU];kU[6]=5;u[jU]=nil;end;end;end;end;if mU then for jU,kU in q,mU,nil do u=kU[5];if mU then local kU=mU[jU];if kU then local lU=o(u);L(c,jU,jU+u-1,1,lU);kU[4]=lU;kU[6]=1;mU[jU]=nil;end;end;end;end;return false,false;else H=K[8];z=K[5];Q=K[7];K=K[9];end;else local u=B==61;if u then c[w[s]]=y[V[s]][l[s]];else S=c[V[s]];end;end;else local u=B<58;if u then local u=B==57;if u then local u;local mU,jU,kU,lU,VU=j[s],n,E;if mU then local IU=#mU/3;if IU>0 then u,lU,VU={},jU,kU;for PU=1,IU,1 do local IU=(PU-1)*3;local SU,KU=mU[IU+1],mU[IU+3];if SU==3 then lU=if not lU then{}else lU;local WU=lU[KU];if not WU then WU={[6]=KU,[4]=c};lU[KU]=WU;else end;u[PU]=WU;else if SU==1 then u[PU]=c[KU];else if SU==2 then u[PU]=y[KU];else if SU==0 then VU=if not VU then{}else VU;local SU=VU[KU];if not SU then SU={[6]=KU,[4]=c,[5]=mU[IU+2]};VU[KU]=SU;else end;u[PU]=SU;else end;end;end;end;end;else lU,VU=jU,kU;end;else lU,VU=jU,kU;end;n,E=lU,VU;i=k[s](nil,u);wU(i,b);c[F[s]]=i;g=u;else c[w[s]]=c[F[s]]+V[s];end;else local u=B==59;if u then c[F[s]]=c[w[s]]~=k[s];else local u,mU,jU=V[s],F[s],c[w[s]];local kU,lU=Z(mU,4294967295),Z(jU,4294967295);local jU,VU,IU,PU=Z(kU,65535),J(kU,16),Z(lU,65535),J(lU,16);mU=Z(jU*IU+e(Z(jU*PU+VU*IU,65535),16),4294967295);IU=nil;repeat kU=mU%4294967296;if kU~=kU then IU=0;break;end;IU=kU-kU%1;until true;c[u]=IU;end;end;end;end;else local u=B>=40;if u then local u=B<44;if u then local u=B>=42;if u then local u=B==43;if u then c[V[s]]={};else local u,mU,jU=F[s],k[s],c[w[s]];local kU,lU=Z(mU,4294967295),Z(jU,4294967295);local VU,IU,PU,SU=Z(kU,65535),J(kU,16),Z(lU,65535),J(lU,16);jU=Z(VU*PU+e(Z(VU*SU+IU*PU,65535),16),4294967295);mU=nil;repeat PU=jU%4294967296;if PU~=PU then mU=0;break;end;mU=PU-PU%1;until true;c[u]=mU;end;else local u=B~=41;if u then c[V[s]]=c[w[s]]~=c[F[s]];else local u,mU=n,V[s];if u then local jU=u[mU];if jU then jU[4]=jU;jU[5]=c[mU];jU[6]=5;u[mU]=nil;end;end;end;end;else local u=B<46;if u then local u=B~=45;if u then c[V[s]]=m[F[s]];c[V[s+1]]=F[s+1];s+=1;else local u=c[V[s]]~=l[s];if u then s=w[s];end;end;else local u=B~=47;if u then K={[5]=z,[9]=K,[7]=Q,[8]=H};g,i=w[s],FU(qU);i(m,c[g],c[g+1],c[g+2]);H=i;s=F[s];else local u,mU,jU=w[s],c[V[s]];repeat local kU=mU%4294967296;if kU~=kU then jU=0;break;end;jU=kU-kU%1;until true;c[u]=jU;end;end;end;else local u=B<36;if u then local u=B<34;if u then local u=B==33;if u then c[V[s]]=c[w[s]]+l[s];else g=V[s];local u,mU,jU=H();if u then c[g+1]=mU;c[g+2]=jU;s=F[s];end;i,C,f=u,mU,jU;end;else local u=B==35;if u then c[F[s]]=c[w[s]][k[s]];else local u,mU,jU=V[s],Y(w[s],(Z(Y(p,(Z(J(p,29),7))),536870911))),v[5];local kU=Y(jU[u],418689291);jU[u]=kU;jU,u=v[4],kU+1;kU=TU(jU,u);local lU,VU;if kU<128 then lU,VU=kU,u+1;else local IU=TU(jU,u+1);if IU<128 then lU,VU=(kU-128)*128+IU,u+2;else local PU=TU(jU,u+2);if PU<128 then lU,VU=(kU-128)*128+(IU-128)*16384+PU,u+3;else local SU=TU(jU,u+3);lU,VU=kU-128+(IU-128)*16384+(PU-128)*128+SU%128*2097152+(SU-SU%128)*2097152,u+4;end;end;end;kU,u=mU*16843009,VU+lU;local IU=u-lU%4;for lU=VU,IU-1,4 do vU(jU,lU,(Y(rU(jU,lU),kU)));end;for kU=IU,u-1,1 do OU(jU,kU,(Y(TU(jU,kU),mU)));end;IU,jU,VU=s,s,s;V[s]=228;w[IU]=139;F[jU]=123;T[VU]=55;end;end;else local u=B<38;if u then local u=B~=37;if u then s=if c[F[s]]then V[s]else w[s];else c[F[s]]=W;end;else local u=B~=39;if u then c[w[s]]=l[s];else c[w[s]]=c[F[s]](c[V[s]]);end;end;end;end;end;end;s+=1;end;else end;D=R==49;if D then while true do local u=w[s];local B=u<27;if B then local B=u>=13;if B then local B=u<20;if B then local B=u>=16;if B then local B=u>=18;if B then local B=u==19;if B then c[F[s]]=c[V[s]]~=O[s];else g=T[s];i,C,f=c[g],c[g+1],c[g+2];c[g]=i(C,f);end;else local B=u==17;if B then c[V[s]]=O[s];else local B,mU,jU=T[s],k[s],c[F[s]];local kU,lU=Z(mU,4294967295),Z(jU,4294967295);local VU,IU,PU,SU=Z(kU,65535),J(kU,16),Z(lU,65535),J(lU,16);mU=Z(VU*PU+e(Z(VU*SU+IU*PU,65535),16),4294967295);SU=nil;repeat jU=mU%4294967296;if jU~=jU then SU=0;break;end;SU=jU-jU%1;until true;c[B]=SU;end;end;else local B=u<14;if B then c[V[s]]=c[T[s]]==c[F[s]];else local B=u==15;if B then R=T[s];s=F[s]+1;break;else K={[5]=z,[9]=K,[7]=Q,[8]=H};g=F[s];Q=c[g+2]+0;z=c[g+1]+0;H=c[g]-Q;s=V[s];end;end;end;else local B=u<23;if B then local B=u>=21;if B then local B=u==22;if B then c[V[s]]=h(c[T[s]](c[F[s]]));else c[F[s]](c[T[s]]);end;else g,i=V[s],c[T[s]];c[g+1]=i;c[g]=i[l[s]];end;else local B=u>=25;if B then local B=u==26;if B then g,i=T[s]+1,Y(F[s],(Z(Y(p,(Z(J(p,29),7))),536870911)));local B=s;for mU=1,V[B],1 do i=Z(Y(i,(e(i,13))),536870911);i=Y(i,(J(i,13)));i=Z(Y(i,(e(i,14))),536870911);T[g]=Y(T[g],(Z(J(i,0),127)));F[g]=Y(F[g],(Z(J(i,7),127)));V[g]=Y(V[g],(Z(J(i,14),127)));w[g]=Y(w[g],(Z(J(i,21),127)));g=g+1;end;w[s]=32;else s=V[s];end;else local B=u==24;if B then c[T[s]]=y[F[s]];else local B;local mU,jU,kU,lU,VU=l[s],n,E;if mU then local IU=#mU/3;if IU>0 then B,lU,VU={},jU,kU;for PU=1,IU,1 do local IU=(PU-1)*3;local SU,KU=mU[IU+1],mU[IU+3];if SU==3 then lU=if not lU then{}else lU;local WU=lU[KU];if not WU then WU={[6]=KU,[4]=c};lU[KU]=WU;else end;B[PU]=WU;else if SU==1 then B[PU]=c[KU];else if SU==2 then B[PU]=y[KU];else if SU==0 then VU=if not VU then{}else VU;local SU=VU[KU];if not SU then SU={[6]=KU,[4]=c,[5]=mU[IU+2]};VU[KU]=SU;else end;B[PU]=SU;else end;end;end;end;end;else lU,VU=jU,kU;end;else lU,VU=jU,kU;end;n,E=lU,VU;i=k[s](nil,B);wU(i,b);c[T[s]]=i;g=B;end;end;end;end;else local B=u>=6;if B then local B=u<9;if B then local B=u<7;if B then K={[5]=z,[9]=K,[7]=Q,[8]=H};g,i=F[s],FU(qU);i(m,c[g],c[g+1],c[g+2]);H=i;s=V[s];else local B=u~=8;if B then c[T[s]]=#c[V[s]];else c[F[s]]=c[V[s]][O[s]];end;end;else local B=u<11;if B then local B=u~=10;if B then H=K[8];z=K[5];Q=K[7];K=K[9];else local B,mU,jU=F[s],c[V[s]];repeat local kU=mU%4294967296;if kU~=kU then jU=0;break;end;jU=kU-kU%1;until true;c[B]=jU;end;else local B=u==12;if B then c[V[s]]=O[s];c[V[s+1]]=O[s+1];c[V[s+2]]=O[s+2];s+=2;else g,i=V[s]+1,T[s];local B=s;for mU=1,F[B],1 do i=Z(Y(i,(e(i,13))),536870911);i=Y(i,(J(i,13)));i=Z(Y(i,(e(i,14))),536870911);T[g]=Y(T[g],(Z(J(i,0),127)));F[g]=Y(F[g],(Z(J(i,7),127)));V[g]=Y(V[g],(Z(J(i,14),127)));w[g]=Y(w[g],(Z(J(i,21),127)));g=g+1;end;w[s]=32;end;end;end;else local B=u>=3;if B then local B=u<4;if B then c[F[s]]=T[s];else local B=u~=5;if B then c[V[s]]=W;else g=y[V[s]];c[T[s]]=g[4][g[6]];end;end;else local B=u<1;if B then c[F[s]]={};else local B,mU,jU,kU=u==2;if B then g,mU,jU,kU=F[s],H();if mU then c[g+1]=jU;c[g+2]=kU;s=V[s];end;else local B,lU=n,E;if B then for VU in q,B,nil do if B then local IU=B[VU];if IU then IU[4]=IU;IU[5]=c[VU];IU[6]=5;B[VU]=nil;end;end;end;end;if lU then for VU,IU in q,lU,nil do B=IU[5];if lU then local IU=lU[VU];if IU then local PU,SU=VU+B,o(B);L(c,VU,PU-1,1,SU);IU[4]=SU;IU[6]=1;lU[VU]=nil;end;end;end;end;B=O[s];return false,true,h(B);end;i,C,f=mU,jU,kU;end;end;end;end;else local B=u<40;if B then local B=u<33;if B then local B=u>=30;if B then local B=u<31;if B then c[V[s]]=y[T[s]][l[s]];else local B=u~=32;if B then g,i,C=T[s],V[s],F[s];f,M,d=g+C-1,g+i,h(c[g](r(c,g+1,g+i)));L(d,1,C,g,c);else end;end;else local B=u>=28;if B then local B=u==29;if B then g,i=T[s]+1,Y(F[s],(Z(Y(W,(Z(J(W,29),7))),536870911)));local B=s;for mU=1,V[B],1 do i=Z(Y(i,(e(i,13))),536870911);i=Y(i,(J(i,13)));i=Z(Y(i,(e(i,14))),536870911);T[g]=Y(T[g],(Z(J(i,0),127)));F[g]=Y(F[g],(Z(J(i,7),127)));V[g]=Y(V[g],(Z(J(i,14),127)));w[g]=Y(w[g],(Z(J(i,21),127)));g=g+1;end;w[s]=32;else g,i,C=F[s],T[s],V[s];f=c[g];L(c,g+1,g+i,C+1,f);end;else c[V[s]]=O[s];c[V[s+1]]=O[s+1];s+=1;end;end;else local B=u<36;if B then local B=u>=34;if B then local B=u==35;if B then c[V[s]]=c[F[s]]+c[T[s]];else c[V[s]]=b[l[s]];end;else c[V[s]]=c[F[s]]==O[s];end;else local B=u<38;if B then local B=u==37;if B then c[V[s]]=c[F[s]][c[T[s]]];else c[V[s]][O[s]]=c[F[s]];end;else local B=u~=39;if B then W=c[T[s]];else y[T[s]][k[s]]=c[F[s]];end;end;end;end;else local B=u<47;if B then local B=u<43;if B then local B=u>=41;if B then local B=u==42;if B then c[F[s]]=not c[V[s]];else s=c[V[s]];end;else c[V[s]]=c[T[s]];end;else local B=u>=45;if B then local B=u==46;if B then local B,mU,jU=F[s],T[s],v[5];local kU=Y(jU[B],418689291);jU[B]=kU;jU,B=v[4],kU+1;kU=TU(jU,B);local lU,VU;if kU<128 then lU,VU=kU,B+1;else local IU=TU(jU,B+1);if IU<128 then lU,VU=(kU-128)*128+IU,B+2;else local PU=TU(jU,B+2);if PU<128 then lU,VU=(kU-128)*128+(IU-128)*16384+PU,B+3;else local SU=TU(jU,B+3);lU,VU=kU-128+(IU-128)*16384+(PU-128)*128+SU%128*2097152+(SU-SU%128)*2097152,B+4;end;end;end;B,kU=mU*16843009,VU+lU;local IU=kU-lU%4;for PU=VU,IU-1,4 do vU(jU,PU,(Y(rU(jU,PU),B)));end;for B=IU,kU-1,1 do OU(jU,B,(Y(TU(jU,B),mU)));end;kU,jU,lU=s,s,s;F[s]=166;T[kU]=43;V[jU]=136;w[lU]=32;else g,i,C,f=Y(W,Z(J(W,14),262143),(Z(J(W,28),15))),F[s],T[s],V[s];M=C<16384 and 7 or(C<2097152 and 14 or 21);d,A=J(C,M),Z(C,e(1,M)-1);local B=s;V[B]=Y(f,12,(Z(J(g,14),127)));B=s;w[B]=Y(d,51,(Z(J(g,21),127)));B=s;T[B]=Y(A,62,(Z(g,127)));B=s;F[B]=Y(i,126,(Z(J(g,7),127)));s-=1;end;else local B=u~=44;if B then g,i,C=V[s],F[s],T[s];f,M=g+C-1,g+i;d=c[M];A=d.n;X=i+A-1;d.n=X;L(d,1,A,i,d);L(c,g+1,M-1,1,d);x=h(c[g](r(d,1,d.n)));L(x,1,C,g,c);else p=c[F[s]];end;end;end;else local B=u<50;if B then local B=u<48;if B then s=if c[T[s]]then F[s]else V[s];else local B=u~=49;if B then c[T[s]]=p;else c[V[s]]=m[F[s]];end;end;else local B=u<52;if B then local B=u==51;if B then c[V[s]]=c[F[s]]+T[s];else local B,mU,jU=V[s],l[s],O[s];local l,kU=Z(mU,4294967295),Z(jU,4294967295);local jU,lU,VU,IU=Z(l,65535),J(l,16),Z(kU,65535),J(kU,16);mU=Z(jU*VU+e(Z(jU*IU+lU*VU,65535),16),4294967295);lU=nil;repeat VU=mU%4294967296;if VU~=VU then lU=0;break;end;lU=VU-VU%1;until true;c[B]=lU;end;else local l=u~=53;if l then c[V[s]]=c[F[s]](c[T[s]]);else c[F[s]][c[V[s]]]=c[T[s]];end;end;end;end;end;end;s+=1;end;else end;X=R==90;if X then while true do x=F[s];D=x>=31;if D then local l=x<46;if l then local l=x>=38;if l then local l=x<42;if l then local l=x>=40;if l then local l=x==41;if l then g,i=V[s]+1,w[s];local l=s;for u=1,T[l],1 do i=Z(Y(i,(e(i,13))),536870911);i=Y(i,(J(i,13)));i=Z(Y(i,(e(i,14))),536870911);w[g]=Y(w[g],(Z(J(i,0),127)));V[g]=Y(V[g],(Z(J(i,7),127)));T[g]=Y(T[g],(Z(J(i,14),127)));F[g]=Y(F[g],(Z(J(i,21),127)));g=g+1;end;F[s]=54;else s=if c[V[s]]then T[s]else w[s];end;else local l=x==39;if l then g,i=w[s]+1,Y(V[s],(Z(Y(p,(Z(J(p,29),7))),536870911)));local l=s;for u=1,T[l],1 do i=Z(Y(i,(e(i,13))),536870911);i=Y(i,(J(i,13)));i=Z(Y(i,(e(i,14))),536870911);w[g]=Y(w[g],(Z(J(i,0),127)));V[g]=Y(V[g],(Z(J(i,7),127)));T[g]=Y(T[g],(Z(J(i,14),127)));F[g]=Y(F[g],(Z(J(i,21),127)));g=g+1;end;F[s]=54;else s=c[V[s]];end;end;else local l=x>=44;if l then local l=x~=45;if l then c[w[s]]=S;else local l=c[w[s]]==c[T[s]];if l then s=V[s];end;end;else local l=x~=43;if l then g=T[s];local l,u,B=H();if l then c[g+1]=u;c[g+2]=B;s=w[s];end;i,C,f=l,u,B;else g,i,C=w[s],T[s],V[s];f,M,d=g+C-1,g+i,h(c[g](r(c,g+1,g+i)));L(d,1,C,g,c);end;end;end;else local l=x>=34;if l then local l=x<36;if l then local l=x==35;if l then p=c[V[s]];else c[T[s]]=W;end;else local l=x==37;if l then local l,u=n,T[s];if l then local B=l[u];if B then B[4]=B;B[5]=c[u];B[6]=5;l[u]=nil;end;end;else local l,u,B=V[s],O[s];repeat local mU=u%4294967296;if mU~=mU then B=0;break;end;B=mU-mU%1;until true;c[l]=B;end;end;else local l=x<32;if l then c[T[s]]=c[V[s]]==j[s];else local l=x~=33;if l then c[V[s]]=c[T[s]](r(c[w[s]],1,c[w[s]].n));else c[V[s]](c[w[s]]);end;end;end;end;else local l=x<54;if l then local l=x>=50;if l then local l=x<52;if l then local l=x==51;if l then local l,u=n,E;if l then for B in q,l,nil do if l then local mU=l[B];if mU then mU[4]=mU;mU[5]=c[B];mU[6]=5;l[B]=nil;end;end;end;end;if u then for B,mU in q,u,nil do l=mU[5];if u then local mU=u[B];if mU then local jU,kU=B+l-1,o(l);L(c,B,jU,1,kU);mU[4]=kU;mU[6]=1;u[B]=nil;end;end;end;end;return false,false;else c[T[s]]=c[V[s]][c[w[s]]];end;else local l=x==53;if l then c[V[s]]=#c[w[s]];else c[V[s]]=c[w[s]]+c[T[s]];end;end;else local l=x>=48;if l then local l=x==49;if l then c[V[s]]=not c[w[s]];else c[V[s]][c[w[s]]]=c[T[s]];end;else local l=x~=47;if l then c[w[s]]=p;else S=c[w[s]];end;end;end;else local l=x<58;if l then local l=x<56;if l then local l=x~=55;if not(l)then local l,S,u=V[s],T[s],c[w[s]];local B,mU=Z(S,4294967295),Z(u,4294967295);local u,jU,kU,lU=Z(B,65535),J(B,16),Z(mU,65535),J(mU,16);S=Z(u*kU+e(Z(u*lU+jU*kU,65535),16),4294967295);B=nil;repeat kU=S%4294967296;if kU~=kU then B=0;break;end;B=kU-kU%1;until true;c[l]=B;end;else local l=x~=57;if l then c[V[s]]=c[w[s]]+O[s];else c[T[s]]=k[s];c[T[s+1]]=k[s+1];c[T[s+2]]=k[s+2];s+=2;end;end;else local l=x<60;if l then local l=x~=59;if l then c[w[s]]=c[V[s]]-c[T[s]];else c[V[s]][O[s]]=c[w[s]];end;else local l=x==61;if l then c[T[s]]=k[s];c[T[s+1]]=k[s+1];s+=1;else local l,S,u=w[s],V[s],v[5];local B=Y(u[l],418689291);u[l]=B;u,l=v[4],B+1;B=TU(u,l);local mU,jU;if B<128 then mU,jU=B,l+1;else local kU=TU(u,l+1);if kU<128 then mU,jU=(B-128)*128+kU,l+2;else local lU=TU(u,l+2);if lU<128 then mU,jU=(B-128)*128+(kU-128)*16384+lU,l+3;else local VU=TU(u,l+3);mU,jU=B-128+(kU-128)*16384+(lU-128)*128+VU%128*2097152+(VU-VU%128)*2097152,l+4;end;end;end;B,l=S*16843009,jU+mU;local kU=l-mU%4;for lU=jU,kU-1,4 do vU(u,lU,(Y(rU(u,lU),B)));end;for B=kU,l-1,1 do OU(u,B,(Y(TU(u,B),S)));end;S,u,mU=s,s,s;w[s]=185;V[S]=203;T[u]=250;F[mU]=54;end;end;end;end;end;else local l=x<15;if l then local l=x<7;if l then local l=x<3;if l then local l=x<1;if l then c[T[s]]=c[w[s]]//c[V[s]];else local l=x~=2;if l then c[T[s]]=m[V[s]];else g,i=w[s],c[T[s]];c[g+1]=i;c[g]=i[k[s]];end;end;else local l=x>=5;if l then local l=x==6;if l then g,i=w[s]+1,Y(V[s],(Z(Y(W,(Z(J(W,29),7))),536870911)));local l=s;for S=1,T[l],1 do i=Z(Y(i,(e(i,13))),536870911);i=Y(i,(J(i,13)));i=Z(Y(i,(e(i,14))),536870911);w[g]=Y(w[g],(Z(J(i,0),127)));V[g]=Y(V[g],(Z(J(i,7),127)));T[g]=Y(T[g],(Z(J(i,14),127)));F[g]=Y(F[g],(Z(J(i,21),127)));g=g+1;end;F[s]=54;else local l,S,u=V[s],c[T[s]];repeat local B=S%4294967296;if B~=B then u=0;break;end;u=B-B%1;until true;c[l]=u;end;else local l=x~=4;if l then R=T[s];s=w[s]+1;break;else H=K[8];z=K[5];Q=K[7];K=K[9];end;end;end;else local l=x<11;if l then local l=x<9;if l then local l=x==8;if l then c[V[s]]=c[T[s]]>w[s];else g=T[s];i,C,f=c[g],c[g+1],c[g+2];c[g]=i(C,f);end;else local l=x==10;if l then c[V[s]]=c[T[s]][j[s]];else c[w[s]]=T[s];end;end;else local l=x>=13;if l then local l=x~=14;if l then c[w[s]]=c[T[s]]-V[s];else c[T[s]]=k[s];end;else local l=x~=12;if l then g,i,C,f=w[s],Y(p,Z(J(p,14),262143),(Z(J(p,28),15))),V[s],T[s];M=g<16384 and 7 or(g<2097152 and 14 or 21);d,A=Z(g,e(1,M)-1),J(g,M);local l=s;F[l]=Y(A,85,(Z(J(i,21),127)));l=s;w[l]=Y(d,44,(Z(i,127)));l=s;V[l]=Y(C,87,(Z(J(i,7),127)));l=s;T[l]=Y(f,0,(Z(J(i,14),127)));s-=1;else H+=Q;g=if Q<=0 then H>=z else H<=z;if g then c[T[s]]=H;s=V[s];end;end;end;end;end;else local l=x>=23;if l then local l=x>=27;if l then local l=x>=29;if l then local l=x~=30;if l then c[V[s]]={};else c[V[s]]=c[w[s]](c[T[s]]);end;else local l=x==28;if l then c[V[s]]=y[w[s]];else c[w[s]]=c[T[s]];end;end;else local l=x<25;if l then local l=x~=24;if l then g,i,C=w[s],T[s],V[s];f=g+i;c[g]=h(c[g](r(c,g+1,f)));else c[T[s]]=c[V[s]]%c[w[s]];end;else local l=x~=26;if l then g,i,C=V[s],T[s],w[s];f=c[g];L(c,g+1,g+i,C+1,f);else s=w[s];end;end;end;else local l=x>=19;if l then local l=x>=21;if l then local l=x==22;if l then local l,S,u=V[s],j[s],c[T[s]];local B,mU=Z(S,4294967295),Z(u,4294967295);local S,jU,kU,lU=Z(B,65535),J(B,16),Z(mU,65535),J(mU,16);mU=Z(S*kU+e(Z(S*lU+jU*kU,65535),16),4294967295);u=nil;repeat kU=mU%4294967296;if kU~=kU then u=0;break;end;u=kU-kU%1;until true;c[l]=u;else W=c[w[s]];end;else local l=x~=20;if l then c[T[s]]=b[j[s]];else K={[5]=z,[9]=K,[7]=Q,[8]=H};g,i=T[s],FU(qU);i(m,c[g],c[g+1],c[g+2]);H=i;s=V[s];end;end;else local l=x>=17;if l then local l,S=x~=18;if l then S=nil;local l,u,B,mU,jU=O[s],n,E;if l then local kU=#l/3;if kU>0 then S,mU,jU={},u,B;for lU=1,kU,1 do local kU=(lU-1)*3;local VU,IU=l[kU+1],l[kU+3];if VU==3 then mU=if not mU then{}else mU;local PU=mU[IU];if not PU then PU={[6]=IU,[4]=c};mU[IU]=PU;else end;S[lU]=PU;else if VU==1 then S[lU]=c[IU];else if VU==2 then S[lU]=y[IU];else if VU==0 then jU=if not jU then{}else jU;local VU=jU[IU];if not VU then VU={[6]=IU,[4]=c,[5]=l[kU+2]};jU[IU]=VU;else end;S[lU]=VU;else end;end;end;end;end;else mU,jU=u,B;end;else mU,jU=u,B;end;n,E=mU,jU;i=k[s](nil,S);wU(i,b);c[w[s]]=i;else local l,u=n,E;if l then for B in q,l,nil do if l then local mU=l[B];if mU then mU[4]=mU;mU[5]=c[B];mU[6]=5;l[B]=nil;end;end;end;end;if u then for B,mU in q,u,nil do l=mU[5];if u then local mU=u[B];if mU then local jU,kU=B+l,o(l);L(c,B,jU-1,1,kU);mU[4]=kU;mU[6]=1;u[B]=nil;end;end;end;end;u=j[s];return false,true,h(u);end;g=S;else local l=x==16;if l then c[w[s]][k[s]]=O[s];else c[T[s]]=c[V[s]]+w[s];end;end;end;end;end;end;s+=1;end;else end;X=R==179;if X then while true do D=F[s];x=D>=26;if x then local l=D>=39;if l then local l=D<46;if l then local l=D>=42;if l then local l=D<44;if l then local l=D~=43;if l then W=c[T[s]];else g=T[s];i,C,f=c[g],c[g+1],c[g+2];c[g]=i(C,f);end;else local l=D~=45;if l then c[V[s]][T[s]]=c[w[s]];else c[T[s]]=c[w[s]][V[s]];end;end;else local l=D<40;if l then local l,S,R=w[s],T[s],v[5];local u=Y(R[l],418689291);R[l]=u;R,l=v[4],u+1;u=TU(R,l);local v,x;if u<128 then v,x=u,l+1;else local X=TU(R,l+1);if X<128 then v,x=(u-128)*128+X,l+2;else local B=TU(R,l+2);if B<128 then v,x=(u-128)*128+(X-128)*16384+B,l+3;else local mU=TU(R,l+3);v,x=u-128+(X-128)*16384+(B-128)*128+mU%128*2097152+(mU-mU%128)*2097152,l+4;end;end;end;l,u=S*16843009,x+v;local X=u-v%4;for B=x,X-1,4 do vU(R,B,(Y(rU(R,B),l)));end;for l=X,u-1,1 do OU(R,l,(Y(TU(R,l),S)));end;v,x,S=s,s,s;w[s]=60;T[v]=77;V[x]=249;F[S]=35;else local v=D==41;if v then local v,l=n,T[s];if v then local S=v[l];if S then S[4]=S;S[5]=c[l];S[6]=5;v[l]=nil;end;end;else c[T[s]]=c[w[s]][k[s]];end;end;end;else local v=D<49;if v then local v=D>=47;if v then local v=D~=48;if v then c[V[s]]=T[s];else c[V[s]]=b[O[s]];end;else c[w[s]]=m[T[s]];end;else local v=D>=51;if v then local v=D==52;if v then c[w[s]]=c[V[s]](c[T[s]]);else s=c[T[s]];end;else local v=D~=50;if v then H=K[8];z=K[5];Q=K[7];K=K[9];else c[T[s]]=p;end;end;end;end;else local v=D<32;if v then local v=D<29;if v then local v=D>=27;if v then local v=D~=28;if v then s=if c[V[s]]then T[s]else w[s];else local v,l=n,E;if v then for S in q,v,nil do if v then local R=v[S];if R then R[4]=R;R[5]=c[S];R[6]=5;v[S]=nil;end;end;end;end;if l then for S,R in q,l,nil do v=R[5];if l then local R=l[S];if R then local u,x=S+v,o(v);L(c,S,u-1,1,x);R[4]=x;R[6]=1;l[S]=nil;end;end;end;end;return false,false;end;else local v,l=n,E;if v then for S in q,v,nil do if v then local R=v[S];if R then R[4]=R;R[5]=c[S];R[6]=5;v[S]=nil;end;end;end;end;if l then for S,R in q,l,nil do v=R[5];if l then local R=l[S];if R then local u=o(v);L(c,S,S+v-1,1,u);R[4]=u;R[6]=1;l[S]=nil;end;end;end;end;l=c[T[s]];return false,true,h(l);end;else local v=D<30;if v then local v,l,S=V[s],c[w[s]];repeat local R=l%4294967296;if R~=R then S=0;break;end;S=R-R%1;until true;c[v]=S;else local v=D~=31;if v then g=w[s];local v,l,S=H();if v then c[g+1]=l;c[g+2]=S;s=T[s];end;i,C,f=v,l,S;else c[V[s]]=c[w[s]]();end;end;end;else local v=D<35;if v then local v=D<33;if v then K={[5]=z,[9]=K,[7]=Q,[8]=H};g,i=w[s],FU(qU);i(m,c[g],c[g+1],c[g+2]);H=i;s=T[s];else local v=D==34;if v then c[w[s]]();else c[T[s]]=c[V[s]]-c[w[s]];end;end;else local v=D<37;if v then local v=D~=36;if not(v)then c[T[s]]=c[V[s]]<w[s];end;else local v=D==38;if v then c[V[s]]=c[T[s]]-j[s];else c[T[s]]={};end;end;end;end;end;else local v=D>=13;if v then local v=D>=19;if v then local v=D>=22;if v then local v=D>=24;if v then local v=D~=25;if v then c[T[s]]=y[V[s]];else g=y[V[s]];c[T[s]]=g[4][g[6]];end;else local v=D~=23;if v then c[V[s]][j[s]]=c[T[s]];else local v,l=n,E;if v then for S in q,v,nil do if v then local K=v[S];if K then K[4]=K;K[5]=c[S];K[6]=5;v[S]=nil;end;end;end;end;if l then for S,K in q,l,nil do v=K[5];if l then local K=l[S];if K then local H=o(v);L(c,S,S+v-1,1,H);K[4]=H;K[6]=1;l[S]=nil;end;end;end;end;v=k[s];return false,true,h(v);end;end;else local v=D>=20;if v then local v=D==21;if v then c[V[s]]=not c[w[s]];else s=T[s];end;else g,i=T[s]+1,w[s];local v=s;for l=1,V[v],1 do i=Z(Y(i,(e(i,13))),536870911);i=Y(i,(J(i,13)));i=Z(Y(i,(e(i,14))),536870911);T[g]=Y(T[g],(Z(J(i,0),127)));w[g]=Y(w[g],(Z(J(i,7),127)));V[g]=Y(V[g],(Z(J(i,14),127)));F[g]=Y(F[g],(Z(J(i,21),127)));g=g+1;end;F[s]=35;end;end;else local v=D<16;if v then local v=D>=14;if v then local v=D==15;if v then c[V[s]]=W;else c[V[s]](c[T[s]]);end;else c[V[s]]=j[s];end;else local v=D>=17;if v then local v=D~=18;if v then c[T[s]]=c[V[s]]+j[s];else g,i=T[s]+1,Y(w[s],(Z(Y(W,(Z(J(W,29),7))),536870911)));local v=s;for l=1,V[v],1 do i=Z(Y(i,(e(i,13))),536870911);i=Y(i,(J(i,13)));i=Z(Y(i,(e(i,14))),536870911);T[g]=Y(T[g],(Z(J(i,0),127)));w[g]=Y(w[g],(Z(J(i,7),127)));V[g]=Y(V[g],(Z(J(i,14),127)));F[g]=Y(F[g],(Z(J(i,21),127)));g=g+1;end;F[s]=35;end;else g,i=T[s],c[V[s]];c[g+1]=i;c[g]=i[j[s]];end;end;end;else local j=D<6;if j then local j=D<3;if j then local j=D>=1;if j then local j=D==2;if j then local j=c[V[s]]==T[s];if j then s=w[s];end;else p=c[w[s]];end;else c[T[s]]=c[w[s]]+V[s];end;else local j=D<4;if j then g,i,C,f=Y(W,Z(J(W,14),262143),(Z(J(W,28),15))),T[s],V[s],w[s];M=f<16384 and 7 or(f<2097152 and 14 or 21);d,A=J(f,M),Z(f,e(1,M)-1);local j=s;T[j]=Y(i,49,(Z(g,127)));j=s;V[j]=Y(C,124,(Z(J(g,14),127)));j=s;w[j]=Y(A,99,(Z(J(g,7),127)));j=s;F[j]=Y(d,15,(Z(J(g,21),127)));s-=1;else local j=D==5;if j then y[T[s]][c[w[s]]]=c[V[s]];else g=y[V[s]];g[4][g[6]]=c[T[s]];end;end;end;else local j=D>=9;if j then local j=D<11;if j then local j=D==10;if j then c[V[s]]=c[T[s]]<c[w[s]];else local j;local v,l,S,K,W=k[s],n,E;if v then local k=#v/3;if k>0 then j,K,W={},l,S;for H=1,k,1 do local k=(H-1)*3;local z,Q=v[k+1],v[k+3];if z==3 then K=if not K then{}else K;local R=K[Q];if not R then R={[6]=Q,[4]=c};K[Q]=R;else end;j[H]=R;else if z==1 then j[H]=c[Q];else if z==2 then j[H]=y[Q];else if z==0 then W=if not W then{}else W;local z=W[Q];if not z then z={[6]=Q,[4]=c,[5]=v[k+2]};W[Q]=z;else end;j[H]=z;else end;end;end;end;end;else K,W=l,S;end;else K,W=l,S;end;n,E=K,W;i=O[s](nil,j);wU(i,b);c[w[s]]=i;g=j;end;else local j=D~=12;if j then g,i=T[s]+1,Y(w[s],(Z(Y(p,(Z(J(p,29),7))),536870911)));local j=s;for b=1,V[j],1 do i=Z(Y(i,(e(i,13))),536870911);i=Y(i,(J(i,13)));i=Z(Y(i,(e(i,14))),536870911);T[g]=Y(T[g],(Z(J(i,0),127)));w[g]=Y(w[g],(Z(J(i,7),127)));V[g]=Y(V[g],(Z(J(i,14),127)));F[g]=Y(F[g],(Z(J(i,21),127)));g=g+1;end;F[s]=35;else local j,b=n,E;if j then for v in q,j,nil do if j then local O=j[v];if O then O[4]=O;O[5]=c[v];O[6]=5;j[v]=nil;end;end;end;end;if b then for v,O in q,b,nil do j=O[5];if b then local O=b[v];if O then local F=o(j);L(c,v,v+j-1,1,F);O[4]=F;O[6]=1;b[v]=nil;end;end;end;end;j,b=T[s],c[V[s]];return true,true,j,h(b);end;end;else local j=D<7;if j then c[T[s]]=#c[w[s]];else local j=D~=8;if j then g,i,C=w[s],V[s],T[s];f,M,d=g+C-1,g+i,h(c[g](r(c,g+1,g+i)));L(d,1,C,g,c);else c[w[s]]=c[V[s]];end;end;end;end;end;end;s+=1;end;end;end,...);if _ then if G then if t then return c[a](r(U,1,U.n));else return c[a](r(c,a+1,U));end;elseif a then if t then return r(a,1,a.n);else return r(c,a,U);end;end;else local j,b,T=n,E,c;if j then for v in q,j,nil do if j then local r=j[v];if r then r[4]=r;r[5]=T[v];r[6]=5;j[v]=nil;end;end;end;end;if b then for v,r in q,b,nil do j=r[5];if b then local r=b[v];if r then local O,w=v+j,o(j);L(T,v,O-1,1,w);r[4]=w;r[6]=1;b[v]=nil;end;end;end;end;bU(m,G,s,I);end;end;return P;end
```


## `O`  (2,239027 - 2,239314)

参数: m, j, b, T, v, r, O, w, F  长度: 287

```lua
function(m,j,b,T,v,r,O,w,F)if O<=41 then if O<=40 then return 63,j+1,r,w;else local j=(r-128)*128+v;return 19,b+2,j,w;end;elseif O<=42 then local j=m[27](T,2+b);return not(j>=128)and 69 or 37,b,r,j;elseif O<=43 then local m=128*(w-128)+F;return 57,b+2,r,m;else return 138,1+b,r,w;end;end
```


## `Q`  (2,260328 - 2,260526)

参数: m, j, b, T, v, r, O, w  长度: 198

```lua
function(m,j,b,T,v,r,O,w)if O<=157 then local F=(j-128)*128+r;return 52,v,b,T+2,F;elseif O<=158 then return 124,v[5],b,T,j;else local b=m[27](w,0);return not not(b>=128)and 28 or 6,v,nil,b,j;end;end
```


## `R`  (2,225468 - 2,225503)

参数: m  长度: 35

```lua
function(m,...)return(...)[...];end
```


## `S`  (2,225965 - 2,226383)

参数: m, j, b, T, v, r, O, w, F, q  长度: 418

```lua
function(m,j,b,T,v,r,O,w,F,q)if q<=11 then if q<=10 then return 1,123,m[27](b,O),T,O,j,w;else local k=m[27](b,T);return 1,not not(128<=k)and 96 or 18,r,T,O,k,w;end;elseif q<=12 then local k=m[27](b,T+1);return 1,not(k>=128)and 125 or 149,r,T,O,j,k;elseif q<=13 then local q,k,l=m[27](b,T+3),O-128,(F-128)*16384;local m=(v-128)*128+(2097152*(q%128)+2097152*(q-q%128))+(k+l);return 1,67,r,4+T,m,j,w;else return 2;end;end
```


## `T`  (2,238911 - 2,238943)

参数: m  长度: 32

```lua
function(m,...)return(...)();end
```


## `U`  (2,1027 - 2,1434)

参数: m, j, b, T, v, r, O, w, F, q, k, l, V  长度: 407

```lua
function(m,j,b,T,v,r,O,w,F,q,k,l,V)if q<=16 then if q<=15 then local I,P=128*(k-128),(T-128)*16384;local T=I+b+P;return 38,r,3+V,j,T,O,w;else local b=m[27](v,V);return b<128 and 72 or 154,r,V,b,k,O,w;end;elseif q<=17 then local b=O-73306;local T,v,I=m[118](b),m[118](b),1+0;local m=1-I;return 160,{nil,I,b+0,m,r},V,j,k,T,v;elseif q<=18 then return 148,r,1+V,j,k,O,w;else l[F]=j;return 82,r,V,j,k,O,w;end;end
```


## `V`  (2,714 - 2,1019)

参数: m, j, b, T, v, r, O, w, F, q  长度: 305

```lua
function(m,j,b,T,v,r,O,w,F,q)if b<=1 then if b<=0 then local k=m[27](F,v+1);return 128>k and 157 or 101,w,v,T,k;else return 52,w,v+1,T,r;end;elseif b<=2 then local m=O+128*(T-128);return 38,w,v+2,m,r;elseif b<=3 then local m=(w-128)*128;return 63,16384*(v-128)+q+m,j+3,T,r;else return 29,w,v+1,T,r;end;end
```


## `W`  (2,259366 - 2,259671)

参数: m, j, b, T, v, r, O, w, F, q  长度: 305

```lua
function(m,j,b,T,v,r,O,w,F,q)if T<=116 then local k=m[27](b,3+O);local m,b,l,V=r-128,(F-128)*16384,(q-128)*128,2097152*(k%128);local F=(k-k%128)*2097152+m+(l+(V+b));return 57,O+4,j,F;elseif T<=117 then local m=w+128*(j-128);return 119,2+O,m,r;elseif O==2 then return 105,O,j,r;else return 14,v,j,r;end;end
```


## `X`  (2,236934 - 2,237185)

参数: m, j, b, T, v, r, O, w, F  长度: 251

```lua
function(m,j,b,T,v,r,O,w,F)if j<=75 then local q=m[27](F,v+1);return not(q>=128)and 100 or 70,q,O,b;elseif j<=76 then local j=128*(b-128);local v=r+(16384*(T-128)+j);return 103,3+w,O,v;else local j=m[27](F,2+w);return j<128 and 142 or 80,w,j,b;end;end
```


## `Y`  (2,1779 - 2,2087)

参数: m, j, b, T, v, r, O, w  长度: 308

```lua
function(m,j,b,T,v,r,O,w)if O<=83 then local F=m[27](T,v+3);local q,k,l,V=r-128,16384*(j-128),128*(b-128),F%128*2097152;local b=(F-F%128)*2097152+k+(q+(l+V));return 17,v+4,w,b;elseif O<=84 then local b=m[27](T,v);return not not(b>=128)and 141 or 112,v,b,r;else local m=(r-128)*128+j;return 17,v+2,w,m;end;end
```


## `Z`  (2,3953 - 2,4371)

参数: m, j, b, T, v, r, O, w, F, q  长度: 418

```lua
function(m,j,b,T,v,r,O,w,F,q)if j<=123 then if j<=122 then local k=m[27](b,3+F);local l,V,I,P,S=w-128,16384*(O-128),(r-128)*128,2097152*(k%128),k%128;local r=(k-S)*2097152;k=P+(l+V)+r+I;return 103,F+4,k,q;else return not not(128<=v)and 81 or 94,F,w,q;end;elseif j<=124 then local v=m[27](b,F);return not(v>=128)and 1 or 0,F,v,q;elseif j<=125 then local m=T+(q-128)*128;return 138,2+F,w,m;else return 17,F+1,w,q;end;end
```


## `a`  (2,4724 - 2,5138)

参数: m, j, b, T, v, r, O, w, F, q, k, l, V, I, P, S, K, W, H, z  长度: 414

```lua
function(m,j,b,T,v,r,O,w,F,q,k,l,V,I,P,S,K,W,H,z)if w<=113 then local Q=m[27](F,3+I);local o=W-128+((K-128)*16384+(128*(P-128)+(2097152*(Q%128)+(Q-Q%128)*2097152)));return 148,k,I+4,q,o,l;elseif w<=114 then V[0]=k;l[0]=T;v[0]=j;K[0]=W;m[19](V,H);m[19](l,H);m[19](v,H);m[19](K,H);return 14,q,I,m[O](m,V,S,T,b,P,l,k,W,r,v,K,nil,j,nil,z),W,l;else local j=m[27](F,I+2);return not(j>=128)and 15 or 127,k,I,q,W,j;end;end
```


## `b`  (2,296050 - 2,296164)

参数: m  长度: 114

```lua
function(m)return true,159,nil,nil,nil,nil,nil,nil,nil,nil,nil,nil,nil,nil,nil,nil,nil,nil,nil,nil,nil,nil,nil;end
```


## `c`  (2,227052 - 2,227381)

参数: m, j, b, T, v, r, O, w, F  长度: 329

```lua
function(m,j,b,T,v,r,O,w,F)if r<=86 then local r=m[27](T,3+v);local q,k,l,V,I=j-128,(b-128)*16384,128*(O-128),2097152*(r%128),r%128;local b=2097152*(r-I);r=V+(k+l+(q+b));return 11,F,4+v,r;else local b=m[27](T,w+3);local m,T,r,O,q=F-128,(v-128)*16384,(j-128)*128,b%128*2097152,2097152*(b-b%128);return 45,O+(T+r+m+q),w+4,j;end;end
```


## `d`  (2,328735 - 2,329147)

参数: m, j, b, T, v, r, O, w, F  长度: 412

```lua
function(m,j,b,T,v,r,O,w,F)if O<=51 then if O<=50 then local q=m[27](j,b+1);return not not(128<=q)and 60 or 147,b,q,T,w;else local q,k=m[67](j,b),b+4;local l=q/2;if not(q%2~=0)then return 74,k,F,T,l;else return 34,k,F,l,w;end;end;elseif O<=52 then local q=m[27](j,b);return q<128 and 126 or 121,b,F,T,q;elseif O<=53 then return 103,1+b,F,T,w;else local m=v+(128*(w-128)+16384*(r-128));return 17,3+b,F,T,m;end;end
```


## `e`  (2,5845 - 2,6210)

参数: m, j, b, T, v, r, O, w, F, q, k, l, V  长度: 365

```lua
function(m,j,b,T,v,r,O,w,F,q,k,l,V)if v<=46 then if v<=45 then local I=m[27](F,k);return not not(128<=I)and 35 or 78,b,k,I,w,r;else V[q]=w;return 110,b,k,l,w,r;end;elseif v<=47 then return 22,b[3],T,l,k,r;elseif v<=48 then local T=128*(r-128);local v=16384*(O-128)+(T+j);return 138,b,3+k,l,w,v;else local j=m[27](F,k);return not(j<128)and 97 or 53,b,k,l,j,r;end;end
```


## `f`  (2,263143 - 2,263371)

参数: m, j, b, T, v, r, O, w  长度: 228

```lua
function(m,j,b,T,v,r,O,w)if b<=129 then local F=m[27](w,2+j);return not not(F>=128)and 86 or 130,v,j,T,F;elseif b<=130 then local m,b=128*(T-128),(r-128)*16384;local r=O+m+b;return 11,v,j+3,r,O;else return 114,v[5],j,T,O;end;end
```


## `g`  (2,2641 - 2,3095)

参数: m, j, b, T, v, r, O, w, F, q  长度: 454

```lua
function(m,j,b,T,v,r,O,w,F,q)if v<=61 then if v<=60 then local k=m[27](O,2+w);return not(k>=128)and 65 or 91,r,F,w,j,T,b,k;else local k,l,V=m[118](T),m[118](T),1+0;local I=1-V;return 134,{nil,T+0,V,r,I},F,w,j,k,l,q;end;elseif v<=62 then local k=m[27](O,1+w);return not(128<=k)and 137 or 161,r,F,w,j,T,k,q;elseif v<=63 then local v=F-73306;local O,k,l=m[118](v),m[118](v),1+0;return 82,{l,nil,r,1-l,v+0},O,w,k,T,b,q;else return 119,r,F,w+1,j,T,b,q;end;end
```


## `h`  (2,259707 - 2,259864)

参数: m, j, b, T, v, r  长度: 157

```lua
function(m,j,b,T,v,r)if b<=132 then local b=m[27](r,1+j);return b<128 and 95 or 120,T,b;else local b=m[27](r,j+1);return not(b<128)and 129 or 153,b,v;end;end
```


## `j`  (2,296625 - 2,296881)

参数: m, j, b, T, v, r, O  长度: 256

```lua
function(m,j,b,T,v,r,O)if v<=25 then local v,w=(b-128)*128,16384*(j-128);local F=O+v+w;return 52,3+r,F;else local v=m[27](T,3+r);local m,T,w,F,q=b-128,(j-128)*16384,128*(O-128),v%128*2097152,v%128;local j=(v-q)*2097152;v=m+w+F+(j+T);return 52,4+r,v;end;end
```


## `k`  (2,230636 - 2,231118)

参数: m, j, b, T, v, r, O, w, F, q, k, l, V, I  长度: 482

```lua
function(m,j,b,T,v,r,O,w,F,q,k,l,V,I)if l<=102 then if l<=101 then local P=m[27](I,2+w);return not(P>=128)and 25 or 26,k,w,O,q,P;else local P=m[27](I,3+w);local S,K,W,H=q-128,16384*(b-128),128*(r-128),P%128*2097152;local r=K+((P-P%128)*2097152+S)+(W+H);return 29,k,w+4,O,r,j;end;elseif l<=103 then T[q]=b;return 89,k,w,O,q,j;elseif l<=104 then local b=128*(O-128);local T=(v-128)*16384+(b+V);return 148,k,w+3,T,q,j;else local b=m[27](I,F);return b<128 and 40 or 75,b,w,O,q,j;end;end
```


## `l`  (2,227982 - 2,228415)

参数: m, j, b, T, v, r, O, w, F, q, k  长度: 433

```lua
function(m,j,b,T,v,r,O,w,F,q,k)if b<=97 then if b<=96 then local l=m[27](j,1+F);return not(128>l)and 68 or 71,w,F,l,r,v;else local l=m[27](j,F+1);return not(l<128)and 5 or 55,w,F,q,l,v;end;elseif b<=98 then local l=m[27](j,F+3);local m,j,V,I=v-128,(k-128)*16384,(O-128)*128,l%128*2097152;local O=(l-l%128)*2097152+V+(I+m)+j;return 138,w,F+4,q,r,O;elseif b<=99 then return 88,w,F+1,q,r,v;else return 63,F+(w-128)*128,2+T,q,r,v;end;end
```


## `m`  (2,295655 - 2,296009)

参数: m, j, b, T, v, r, O, w, F, q, k, l, V, I  长度: 354

```lua
function(m,j,b,T,v,r,O,w,F,q,k,l,V,I)if l<=143 then if l<=142 then local P=v+((j-128)*128+16384*(V-128));return 19,q,3+r,k,P,T;else b[0]=k;m[19](b,I);return 14,w,r,m[q](m,b),j,T;end;elseif l<=144 then k[j]=V;return 134,q,r,k,j,T;elseif l<=145 then return 106,q,r,k,j,O+(T-128)*128;else local b=m[27](F,w+2);return not(b>=128)and 9 or 87,q,r,b,j,T;end;end
```


## `n`  (2,6233 - 2,6562)

参数: m, j, b, T, v, r, O, w, F  长度: 329

```lua
function(m,j,b,T,v,r,O,w,F)if b<=127 then local b=m[27](w,j+3);local q,k,l,V,I=T-128,(v-128)*16384,128*(r-128),b%128*2097152,b%128;local v=(b-I)*2097152;b=k+(V+(q+l+v));return 38,4+j,O,b;else local b=m[27](w,3);local m,v,r,w,q=j-128,16384*(O-128),128*(F-128),2097152*(b%128),(b-b%128)*2097152;return 108,m+r+(v+(q+w)),4,T;end;end
```


## `o`  (2,236247 - 2,236636)

参数: m, j, b, T, v, r, O, w, F  长度: 389

```lua
function(m,j,b,T,v,r,O,w,F)if O<=66 then if O<=65 then local q=128*(T-128);local k=16384*(v-128)+(F+q);return 144,3+w,b,k,v;else return 11,w+1,b,T,v;end;elseif O<=67 then local q=m[27](r,w);return not(128>q)and 62 or 150,w,q,T,v;elseif O<=68 then local O=m[27](r,2+w);return not(128>O)and 113 or 104,w,b,T,O;else local m=(v-128)*128;local v=(F-128)*16384+(j+m);return 119,3+w,b,T,v;end;end
```


## `p`  (2,238467 - 2,238908)

参数: m, j, b, T, v, r, O, w, F, q, k  长度: 441

```lua
function(m,j,b,T,v,r,O,w,F,q,k)if b<=92 then if b<=91 then local l=m[27](k,r+3);local V,I,P,S=F-128,16384*(v-128),128*(w-128),l%128*2097152;local v=I+((l-l%128)*2097152+V)+P+S;return 144,4+r,v,T,q;else local v=m[27](k,r+1);return not not(128<=v)and 93 or 43,r,F,v,q;end;elseif b<=93 then local v=m[27](k,2+r);return not(v<128)and 116 or 155,r,F,T,v;elseif b<=94 then return 45,O+1,F,T,q;else local m=128*(q-128)+j;return 29,r+2,F,T,m;end;end
```


## `q`  (2,235576 - 2,236022)

参数: m, j, b, T, v, r, O, w, F, q  长度: 446

```lua
function(m,j,b,T,v,r,O,w,F,q)if r<=6 then if r<=5 then local k=m[27](q,F+2);return not(k<128)and 122 or 76,v,F,O,b,k;else return 108,v,F,1,b,j;end;elseif r<=7 then local k=m[27](q,F+3);local m,q,l,V=b-128,16384*(w-128),(T-128)*128,2097152*(k%128);local T=m+(q+2097152*(k-k%128)+(V+l));return 61,v,4+F,O,T,j;elseif r<=8 then local m=128*(O-128)+(16384*(b-128)+w);return 67,v,3+F,m,b,j;else return 45,(v-128)*128+((F-128)*16384+b),O+3,O,b,j;end;end
```


## `r`  (2,2147 - 2,2638)

参数: m, j, b, T, v, r, O, w, F, q, k  长度: 491

```lua
function(m,j,b,T,v,r,O,w,F,q,k)if q<=56 then if q<=55 then local l=(r-128)*128+O;return 103,T,v+2,k,w,b,F,l;else return 144,T,1+v,k,w,b,F,r;end;elseif q<=57 then local O=b-73306;local l,V,I=m[118](O),m[118](O),1+0;return 89,{T,I,nil,1-I,O+0},v,k,w,l,V,r;elseif q<=58 then local m,O,q=T[3],T[2],T[5];local l,V=m+O,O<=0;m,O=l>=q,l<=q;q=V and m or not V and O;T[3]=l;if q then return 84,T,v,k,l,b,F,r;else return 39,T,v,k,w,b,F,r;end;else local m=(k-128)*128+j;return 67,T,v+2,m,w,b,F,r;end;end
```


## `s`  (2,226386 - 2,226753)

参数: m, j, b, T, v, r, O, w, F, q, k  长度: 367

```lua
function(m,j,b,T,v,r,O,w,F,q,k)if j<=21 then if j<=20 then return 108,w,128*(T-128)+((r-128)*16384+v),3,F,q,O;else return 45,128*(w-128)+T,2+r,r,F,q,O;end;elseif j<=22 then return 136,w,T,r,F,q,O+1;elseif j<=23 then local j=(q-128)*128;local v=(O-128)*16384+b+j;return 29,w,3+T,r,F,v,O;else local j=m[27](k,1+T);return not not(128<=j)and 42 or 117,w,T,r,j,q,O;end;end
```


## `t`  (2,298036 - 2,298391)

参数: m, m, j, b, T, v, r, O, w  长度: 355

```lua
function(m,m,j,b,T,v,r,O,w)if O<=108 then local F;local q=r[6];if not(0~=v)then return 10,q,v,w,b,T,m;else return 118,r,v,w,F,q,m;end;elseif O<=109 then return 108,r,128*(v-128)+w,2,b,T,m;else local O,F,q=j[1],j[5],j[2];local k,l=O+F,F<=0;O,F=k>=q,k<=q;q=l and O or not l and F;j[1]=k;if q then return 46,r,v,w,b,T,k;else return 47,r,v,w,b,T,m;end;end;end
```


## `u`  (2,225523 - 2,225865)

参数: m, j, b, T, v, r, O, w  长度: 342

```lua
function(m,j,b,T,v,r,O,w)if T<=31 then if T<=30 then return 57,w,v+1,O,j,r;else return 152,w[1],v,O,j,r;end;elseif T<=32 then return 143,w[4],v,O,j,r;elseif T<=33 then local T=m[27](b,v);return not(T>=128)and 66 or 133,w,v,T,j,r;else local T,r=m[67](b,v),v+4;local v,F,q,k=m[67](b,r),r+4,j-j%1,1+0;return 110,{q-k,T+0,w,nil,k},T,O,v,F;end;end
```


## `v`  (2,236639 - 2,236931)

参数: m, j, b, T, v, r, O, w  长度: 292

```lua
function(m,j,b,T,v,r,O,w)if v<=78 then return 67,1+O,T,b;elseif v<=79 then local v=m[27](w,O);return not not(128<=v)and 12 or 44,O,T,v;else local v=m[27](w,O+3);local m,w,F,q,k=T-128,16384*(j-128),128*(r-128),v%128*2097152,v%128;local j=2097152*(v-k);v=F+q+(m+(j+w));return 19,4+O,v,b;end;end
```


## `w`  (2,264055 - 2,264236)

参数: m, j, b, T, v, r, O  长度: 181

```lua
function(m,j,b,T,v,r,O)if v<=106 then return 88,T,j+2;else local v,w,F,q=m[27](b,O+3),T-128,16384*(j-128),(r-128)*128;return 63,v%128*2097152+((v-v%128)*2097152+(q+w))+F,O+4;end;end
```


## `x`  (2,235354 - 2,235477)

参数: m, j, b, T, v  长度: 123

```lua
function(m,j,b,T,v)if j<=111 then local j=m[27](v,T+1);return not not(128<=j)and 90 or 145,T,j;else return 38,1+T,b;end;end
```


## `y`  (2,228418 - 2,228659)

参数: m, j, b, T, v, r, O  长度: 241

```lua
function(m,j,b,T,v,r,O)if v<=119 then local w=m[27](r,b);return not(128<=w)and 99 or 111,w,j,O;elseif v<=120 then local v=m[27](r,b+2);return not(128>v)and 102 or 23,T,v,O;else local v=m[27](r,b+1);return not(v<128)and 36 or 85,T,j,v;end;end
```


## `z`  (2,1458 - 2,1702)

参数: m, j, b, T, v, r, O  长度: 244

```lua
function(m,j,b,T,v,r,O)if j<=81 then local j=m[27](v,T+1);return not(j<128)and 146 or 21,j,r;else local m,j,T=b[4],b[1],b[5];local v,w=m+j,j<=0;j,m=v>=T,v<=T;T=w and j or not w and m;b[4]=v;if T then return 16,O,v;else return 73,O,r;end;end;end
```


## `D6`  (2,259868 - 2,259926)

参数: m, m, j, b  长度: 58

```lua
function(m,m,j,b)local T=b+128*(m-128);return 15,2+j,T;end
```


## `G6`  (2,265231 - 2,265607)

参数: m, j, b, T, v, r  长度: 376

```lua
function(m,j,b,T,v,r)if T<=11 then if T<=10 then local O=(v*j+r)%256;local w=(r+O*j)%256;local F=(r+w*j)%256;local q=(r+F*j)%256;local k,l,V,I=m.P6,256*w,65536*F,q*16777216;k[v]=l+O+(V+I);m.M6[v]=q;return 6,r,b;else return 28,r+1,b;end;elseif T<=12 then return 20,r+1,b;elseif T<=13 then local T=m[27](j,1+r);return not not(T>=128)and 19 or 33,r,T;else return 42,r+1,b;end;end
```


## `H6`  (2,295126 - 2,295588)

参数: m, j, b, T, v, r, O, w, F, q  长度: 462

```lua
function(m,j,b,T,v,r,O,w,F,q)if b<=33 then if b<=32 then local k=m[27](v,3+w);local l,V,I,P=j-128,(r-128)*16384,(F-128)*128,k%128*2097152;local S=l+2097152*(k-k%128)+(P+(I+V));return 37,v,w+4,T,S,r;else local k=j+(T-128)*128;return 42,v,w+2,k,j,r;end;elseif b<=34 then local k=128*(r-128)+((F-128)*16384+q);return 20,v,3+w,T,j,k;elseif b<=35 then m[83](O,v,T);return 41,v+4,w,T,j,r;else local m=128*(j-128);local j=16384*(r-128)+F+m;return 37,v,w+3,T,j,r;end;end
```


## `K6`  (2,263752 - 2,263983)

参数: m, m, j, b, T, v, r  长度: 231

```lua
function(m,m,j,b,T,v,r)if v<=5 then local v=(m-128)*128+b;return 37,T+2,j,v;else local b,v,O=r[2],r[4],r[3];local w,F=b+v,v<=0;v,b=w>=O,w<=O;O=F and v or not F and b;r[2]=w;if O then return 10,T,w,m;else return 25,T,j,m;end;end;end
```


## `L6`  (2,239338 - 2,256861)

参数: m, j, b, T  长度: 17523

```lua
function(m,j,b,T)local v;local r,O,w,F,q,k,l,V,I,P,S,K,W,H,z,Q,o,n,E,p,c,s,R,L,Z,J,e,Y=m[27],m[37],m[38],m[83],m.J,m[67],m.P6,m[103],m.M6,m[121],m[47],m[9],m[8],m[59],m[118],m[41],m.L6,m[90],m[116],m[39],m[84],m[49],m[92],m._,m[94],m[71],8;local h;local N,y,u,_,A,G,t,a,U,x,i,d=j,b,T;while true do if e<=17 then if e<=8 then if e<=3 then e,N,y,u,G,t=m:R6(A,G,u,x,e,y,a,_,N,t,U);else e,y,u,_,A,G=m:T6(u,d,G,t,e,_,v,y,x,N,A,U);end;elseif e<=12 then e,A,G=m:i6(G,_,e,U,Y,a,A,t,u);elseif e<=14 then if e<=13 then b=Y[3];v=N;e,Y,y=v[7]and 18 or 20,b,6;else e,A,G=m:D6(G,A,t);end;else e,Y,y,u,t,a,U,x,i,d=m:_6(x,d,a,i,u,y,e,U,Y,G,t);end;elseif e<=26 then if e<=21 then e,u,A,t=m:b6(t,U,v,A,u,e);else e,Y,u,A,G,t,a=m:V6(t,_,a,e,G,Y,U,A,u);end;elseif e<=30 then if e<=28 then if e<=27 then h=v[5];T={__index=function(j,b)local d,X=33;local g,f,C,M,D,B,mU,jU,bU,TU,vU,rU,OU,wU=j,b;while true do local FU,qU,kU,lU,VU;if d<=97 then if d<=48 then if d<=23 then if d<=11 then if d<=5 then if d<=2 then if d<=0 then b=r(mU,1+C);d,D=not(b<128)and 184 or 111,b;elseif d<=1 then d,M,C=140,B+((M-128)*128+16384*(D-128)),3+C;else local b,IU=133,25;FU=(C+8)%256;local PU,SU,KU=w(D),134744072,D-D%4;local WU,HU=KU-1,4+0;j=0-HU;local zU={WU+0,X,nil,HU,j};d,X,C,B,jU,bU,TU,vU,rU,OU=10,zU,FU,8,O,b,IU,PU,SU,KU;end;elseif d<=3 then local j=r(B,1+M);d,mU=j<128 and 164 or 53,j;elseif d<=4 then local j,b,IU=X[3],X[1],X[2];local PU,SU=j+b,b<=0;j,b=PU>=IU,PU<=IU;IU=SU and j or not SU and b;X[3]=PU;if IU then d,jU=83,PU;else d=34;end;else return M;end;elseif d<=8 then if d<=6 then local j=X[3];d,X=88,j;elseif d<=7 then local j;j,d=128*(C-128),112;C,M=16384*(M-128)+(j+D),3;else local j,b,IU=X[3],jU(vU),M+D;local PU=r(mU,IU);d,X,C,M,B=PU<128 and 41 or 186,j,b,IU,PU;end;elseif d<=9 then local j=r(mU,3+M);local b,IU,PU,SU,KU,WU,HU=B-128,(jU-128)*16384,128*(bU-128),j%128*2097152,j%128;WU,HU,d=b+((j-KU)*2097152+IU)+(PU+SU),4+M,129;B=WU;elseif d<=10 then local j,b,IU=X[5],X[4],X[1];local PU,SU=j+b,b<=0;b,j=PU>=IU,PU<=IU;IU=SU and b or not SU and j;X[5]=PU;if IU then d,wU=58,PU;else d=65;end;else d,M=112,1;end;elseif d<=17 then if d<=14 then if d<=12 then local j=r(vU,M+3);local b,IU,PU,SU,KU,WU=B-128,(mU-128)*16384,(jU-128)*128,j%128*2097152,j%128;WU,d,M=(j-KU)*2097152+PU+SU+(IU+b),107,4+M;B=WU;elseif d<=13 then local j,b,IU=M+1,(4+C)%256,0;F(q,0,(V(67372036,k(mU,0+j),l[b])));j=I[b];d,M=88,P(q,B);else local j=r(vU,M+2);d,jU=not(128<=j)and 116 or 12,j;end;elseif d<=15 then local j=r(B,1+M);if not(128<=j)then d,B=185,j;else d,jU=96,j;end;elseif d<=16 then qU=(bU*C+TU)%256;S(vU,D,(V(mU,qU,(r(B,M+D)))));d,C=99,qU;else local j,b,P=M+1,(196+C)%256,0;local P=k(B,j+0);F(q,0,(V(3301229764,l[b],P)));P=I[b];d,M=88,K(q,D);end;elseif d<=20 then if d<=18 then bU(TU,jU,(OU(rU,vU,M)));local j,b=I[D],8;F(q,b,(V(k(mU,C+b),l[j],M)));local b,b=I[j],W(K(q,B),K(q,4),(K(q,8)));d,M=88,b;elseif d<=19 then local j=r(B,2+M);d,jU=not(j<128)and 192 or 36,j;else local j=r(B,M+1);d,mU=j<128 and 187 or 19,j;end;elseif d<=21 then d,C=115,C+1;elseif d<=22 then local j;B,d,j=(mU-128)*128+(B+16384*(jU-128)),45,3+M;else local j,b,b=r(mU,C),C+1,w(M);H(b,0,j);d,M=88,b;end;elseif d<=35 then if d<=29 then if d<=26 then if d<=24 then d=not(51<mU)and 174 or 145;elseif d<=25 then local j=r(mU,M+3);local b,P,W,H,IU=D-128,(B-128)*16384,128*(jU-128),j%128*2097152,j-j%128;local j,PU,SU=2097152*IU+b,H+W;SU,d,M=P+(j+PU),114,M+4;D=SU;else local j=r(B,3+M);local b,P,W,H,IU=mU-128,16384*(jU-128),128*(bU-128),2097152*(j%128),j%128;local PU,SU,KU=(j-IU)*2097152,b+W;KU,d,M=SU+(P+PU+H),63,4+M;mU=KU;end;elseif d<=27 then d,B,D=149,128*(B-128)+mU,D+2;elseif d<=28 then d=not(76>=mU)and 190 or 78;else local j,b=D-1,1+0;local P=OU-b;local W={j+0,b,X,nil,P};d,X=60,W;end;elseif d<=32 then if d<=30 then local j,b=z(B),1+0;local P=1-b;local W={b,B+0,P,nil,X};d,X,mU=4,W,j;elseif d<=31 then local j=r(mU,2+M);d,jU=j<128 and 38 or 173,j;else local j,b=mU-1,1+0;local P={OU-b,X,j+0,nil,b};d,X=43,P;end;elseif d<=33 then local j=g[0][f];local b,P,W=h[j],v,0;local H=P[4];local h,IU=r(H,b),b+1;if h>94 then d,C,M,D,B,mU,jU=93,j,b,P,W,H,h;else d,C,M,D,B,mU=24,j,b,W,H,h;end;elseif d<=34 then local j=X[5];M[D]=mU;d,X=42,j;else d,D,M=2,(D-128)*128+B,M+2;end;elseif d<=41 then if d<=38 then if d<=36 then local j,b,P=128*(D-128),16384*(mU-128);P,d,M=jU+j+b,37,3+M;D=P;elseif d<=37 then local j,b=133,25;qU=(8+C)%256;local P,W,H=w(D),134744072,D-D%4;local h,IU=H-1,4+0;local PU={0-IU,nil,X,h+0,IU};d,X,C,mU,jU,bU,TU,vU,rU,OU=182,PU,qU,8,O,j,b,P,W,H;else local j,b,P=(D-128)*128,16384*(B-128);P,d,M=b+j+jU,2,3+M;D=P;end;elseif d<=39 then d=not not(181==jU)and 72 or 121;elseif d<=40 then local j=X[3];d,X=160,j;else local j,j=M+1;do j=true;end;d=j and 129 or 139;end;elseif d<=44 then if d<=42 then local j,b,P=X[2],X[4],X[3];local W,H=j+b,b<=0;b,j=W>=P,W<=P;P=H and b or not H and j;X[2]=W;if P then d,D=30,W;else d=89;end;elseif d<=43 then local j,b,P=X[1],X[5],X[3];local W,H=j+b,b<=0;b,j=W>=P,W<=P;P=H and b or not H and j;X[1]=W;if P then d,mU=177,W;else d=47;end;else d,M,C=140,D+128*(M-128),C+2;end;elseif d<=46 then if d<=45 then local j,b=z(D),1+0;local P={nil,1-b,D+0,b,X};d,X,M=42,P,j;else local j=M+1;local b=r(B,j);d,M,D=128>b and 176 or 20,j,b;end;elseif d<=47 then local j,b=X[2],r(vU,D);d,X,C=b<128 and 11 or 85,j,b;else vU(rU,bU,(wU(M,OU,TU)));local j=1;S(q,j,(V((jU+TU*mU)%256,r(B,j+C),M)));d,M=88,Q(q,D);end;elseif d<=72 then if d<=60 then if d<=54 then if d<=51 then if d<=49 then local j,b,P=(B-128)*128,(jU-128)*16384;P,d,D=j+mU+b,149,3+D;B=P;elseif d<=50 then local j=r(mU,2+C);d,B=not not(128<=j)and 166 or 1,j;else d=not(181>=jU)and 130 or 179;end;elseif d<=52 then d,C=140,1+C;elseif d<=53 then local j=r(B,M+2);d,jU=not(j>=128)and 123 or 54,j;else local j=r(B,M+3);local b,P,W,H,Q,h=D-128,16384*(mU-128),128*(jU-128),2097152*(j%128),j%128;h,d,M=P+(W+(j-Q)*2097152)+(H+b),170,M+4;D=h;end;elseif d<=57 then if d<=55 then local j,b,P,W=1+M,(C+176)%256,2964369584,0;F(q,W,(V(P,k(mU,W+j),l[b])));local H=I[b];W=4;d,C,M,D,jU,bU,TU,vU,rU,OU=18,j,P,H,W,F,q,k(mU,W+j),l[H],V;elseif d<=56 then local j,b=3*(D-1),r(vU,M);d,D,B=not(b<128)and 193 or 131,j,b;else d=not(jU>144)and 103 or 138;end;elseif d<=58 then F(vU,wU,(V(rU,k(mU,M+wU),l[C])));FU=I[C];d,C=10,FU;elseif d<=59 then local j=o(m,D,C,169);d,M=88,j;else local j,b,P=X[5],X[2],X[1];local W,H=j+b,b<=0;b,j=W>=P,W<=P;P=H and b or not H and j;X[5]=W;if P then d,rU=74,W;else d=8;end;end;elseif d<=66 then if d<=63 then if d<=61 then local j,b,P=1+M,133,25;local W,H=0,(P+(179+C)%256*b)%256;d,C,M,mU,jU,bU,TU,vU,rU,OU,wU=48,j,179,b,P,W,H,S,q,r(B,j+W),V;elseif d<=62 then local j=r(mU,D+2);if not(128>j)then d,bU=189,j;else d,mU=49,j;end;else local j,b=133,25;kU=(C+173)%256;local P,W,H=w(mU),2913840557,mU-mU%4;local Q,o=H-1,4+0;local h=0-o;local IU={Q+0,X,nil,h,o};d,X,C,jU,bU,TU,vU,rU,OU=194,IU,kU,173,j,b,P,W,H;end;elseif d<=64 then local j,b,P=X[3],jU(vU),D+M;local W=r(mU,P);d,X,C,M,D,B=not(W<128)and 95 or 154,j,b,n,P,W;elseif d<=65 then local j=X[2];d,X=68,j;else d,D,M=114,128*(D-128)+B,M+2;end;elseif d<=69 then if d<=67 then local j=1+M;local b=r(B,j);d,M,mU=not not(128<=b)and 101 or 196,j,b;elseif d<=68 then local j,b=D-1,1+0;local P={b,nil,X,OU-b,j+0};d,X=71,P;else local j,b,P=1+M,(C+12)%256,0;local P=k(mU,j+0);F(q,0,(V(l[b],202116108,P)));P=I[b];d,M=88,k(q,B);end;elseif d<=70 then local j=1+M;local b=r(B,j);d,C,M=128>b and 21 or 82,j,b;elseif d<=71 then local j,b,P=X[4],X[1],X[5];local W,H=j+b,b<=0;b,j=W>=P,W<=P;P=H and b or not H and j;X[4]=W;if P then d,rU=163,W;else d=64;end;else local j=1+M;local b=r(mU,j);d,M,D=b<128 and 150 or 80,j,b;end;elseif d<=84 then if d<=78 then if d<=75 then if d<=73 then vU(rU,bU,(wU(OU,TU,M)));local j,b=1,(jU+TU*D)%256;S(q,j,(V(M,r(mU,C+j),b)));d,M=88,E(q,B);elseif d<=74 then lU=(TU+C*bU)%256;S(vU,rU,(V(B,lU,(r(mU,rU+M)))));d,C=60,lU;else local j=r(mU,M+1);d,B=128>j and 66 or 143,j;end;elseif d<=76 then d=not(mU>59)and 17 or 161;elseif d<=77 then local j,b,P=X[4],X[2],X[3];local W,H=j+b,b<=0;j,b=W>=P,W<=P;P=H and j or not H and b;X[4]=W;if P then d,D=56,W;else d=171;end;else local j,b,P,W=1+M,(32+C)%256,538976288,0;F(q,W,(V(k(B,W+j),l[b],P)));local H=I[b];W=4;d,C,M,mU,jU,bU=141,j,P,H,W,F;end;elseif d<=81 then if d<=79 then d=not not(138>=jU)and 106 or 57;elseif d<=80 then local j=r(mU,M+1);d,B=not(j<128)and 31 or 35,j;else local j=r(B,2+M);d,bU=not(j<128)and 26 or 195,j;end;elseif d<=82 then local j=r(B,C+1);d,D=not not(128<=j)and 100 or 178,j;elseif d<=83 then mU[jU]=V(C,jU*D);d=4;else d,C,M=112,128*(C-128)+M,2;end;elseif d<=90 then if d<=87 then if d<=85 then local j=r(vU,1);d,M=128>j and 84 or 109,j;elseif d<=86 then d,M=88,4294967296*M+C;else local j,b,b=M+1,0,(25+(64+C)%256*133)%256;S(q,0,(V(r(mU,0+j),b,64)));j=-r(q,B);d,M=88,j;end;elseif d<=88 then g[f]=M;d=5;elseif d<=89 then local j=X[5];d,X=88,j;else local j,b,P=p(C,mU%D+1,mU%D+2),1+mU,1+0;local W=b-P;b={B+0,nil,X,W,P};d,X,mU=126,b,j;end;elseif d<=93 then if d<=91 then local j,b,P=X[2],X[5],X[4];local W,H=j+b,b<=0;j,b=W>=P,W<=P;P=H and j or not H and b;X[2]=W;if P then d,mU=90,W;else d=6;end;elseif d<=92 then local j,b=I[M],4;local P=k(B,C+b);F(q,b,(V(l[j],mU,P)));P=I[j];d,M=88,c(q,D);else d=not not(156<jU)and 51 or 79;end;elseif d<=95 then if d<=94 then local j,b,b=M+1,0,(133*((227+C)%256)+25)%256;S(q,0,(V(r(B,j+0),b,227)));j=r(q,D)~=202;d,M=88,j;else local j=r(mU,1+D);if not(j<128)then d,jU=62,j;else d,mU=27,j;end;end;elseif d<=96 then local j=r(B,2+M);if 128>j then d,B=22,j;else d,bU=136,j;end;else local j,b=z(3*C),1+0;local P=1-b;local W={X,b,C+0,P,nil};d,X,C=77,W,j;end;elseif d<=146 then if d<=121 then if d<=109 then if d<=103 then if d<=100 then if d<=98 then local j=jU+1;d,jU=110,j;elseif d<=99 then local j,b,P=X[1],X[5],X[2];local W,H=j+b,b<=0;b,j=W>=P,W<=P;P=H and b or not H and j;X[1]=W;if P then d,D=16,W;else d=148;end;else local j=r(B,C+2);d,mU=not(j<128)and 144 or 172,j;end;elseif d<=101 then local j=r(B,M+1);d,jU=not(128<=j)and 175 or 81,j;elseif d<=102 then d=not(66<mU)and 167 or 28;else local j=M+1;local b=r(mU,j);d,C,M=not not(128<=b)and 0 or 147,j,b;end;elseif d<=106 then if d<=104 then local j;B,d,j=(B-128)*128+mU,129,M+2;elseif d<=105 then local j=M+1;local b=r(mU,j);d,M,D=128>b and 132 or 75,j,b;else d=not not(97<jU)and 13 or 69;end;elseif d<=107 then local j,b,P=s(3,B),R(B,2),1325;if not not(0~=j)then d,B,mU,jU=110,j,b,P;else d,B,mU=191,j,b;end;elseif d<=108 then local j=r(vU,3+M);local b,P,W,H,Q=jU-128,(bU-128)*16384,128*(TU-128),j%128*2097152,j%128;local o,n,E=(j-Q)*2097152,H+b+P;E,d,M=W+(n+o),98,4+M;jU=E;else local j=r(vU,2);d,D=not(j>=128)and 7 or 113,j;end;elseif d<=115 then if d<=112 then if d<=110 then C[2+D]=jU;C[1+D]=B;C[3+D]=mU;d=77;elseif d<=111 then d,M,C=23,128*(M-128)+D,C+2;elseif not(0>=C)then d=97;else d,M=88,L;end;elseif d<=113 then local j=r(vU,3);local b,P,W,H,Q,o=C-128,16384*(M-128),(D-128)*128,2097152*(j%128),j%128;o,d=2097152*(j-Q),112;C,M=b+(W+P)+(H+o),4;elseif d<=114 then local j,b=133,25;lU=(C+8)%256;local P,W,H=w(D),134744072,D-D%4;local Q,o=H-1,4+0;local n=0-o;local E={nil,Q+0,X,n,o};d,X,C,B,jU,bU,TU,vU,rU,OU=146,E,lU,8,O,j,b,P,W,H;else local j=w(M);Z(j,0,B,C,M);local b=C+M;d,M=88,j;end;elseif d<=118 then if d<=116 then d,B,M=107,(B-128)*128+(16384*(mU-128)+jU),M+3;elseif d<=117 then d,M=98,1+M;else local j=r(vU,2+M);d,TU=not(j>=128)and 125 or 108,j;end;elseif d<=119 then F(vU,wU,(V(rU,k(B,M+wU),l[C])));kU=I[C];d,C=194,kU;elseif d<=120 then d=not(37<mU)and 46 or 156;else local j=M+1;local b=r(mU,j);d,C,M=not(b>=128)and 52 or 159,j,b;end;elseif d<=133 then if d<=127 then if d<=124 then if d<=122 then local j=r(mU,M+2);if 128>j then d,mU=169,j;else d,bU=9,j;end;elseif d<=123 then local j,b,O=(D-128)*128,(mU-128)*16384;O,d,M=jU+b+j,170,M+3;D=O;else d=246==jU and 188 or 87;end;elseif d<=125 then local j,b,O=(jU-128)*128,(bU-128)*16384;O,d,M=b+(j+TU),98,M+3;jU=O;elseif d<=126 then local j,b,O=X[4],X[5],X[1];local w,P=j+b,b<=0;j,b=w>=O,w<=O;O=P and j or not P and b;X[4]=w;if O then d,jU=127,w;else d=133;end;else d=not(p(C,1+jU%D,jU%D+2)==mU)and 126 or 162;end;elseif d<=130 then if d<=128 then d=not(mU>23)and 61 or 70;elseif d<=129 then VU=0;local j=1+0;local b={nil,1-j,X,B+0,j};d,X,M=91,b,VU;else d=jU<=185 and 105 or 124;end;elseif d<=131 then d,M=107,1+M;elseif d<=132 then d,M=114,M+1;else local j=X[3];d,X=91,j;end;elseif d<=139 then if d<=136 then if d<=134 then local j=r(mU,3+C);local b,O,w,P,W=M-128,(D-128)*16384,128*(B-128),j%128*2097152,j%128;local H,Q,o=(j-W)*2097152,O+b;o,d,C=Q+(H+P+w),23,4+C;M=o;elseif d<=135 then local j=k(B,M+wU);F(vU,wU,(V(l[C],rU,j)));qU=I[C];d,C=182,qU;else local j=r(B,M+3);local b,O,w,P,W,H,Q=mU-128,16384*(jU-128),128*(bU-128),j%128*2097152,j%128;H,Q,d=b+(O+(w+2097152*(j-W)))+P,M+4,45;B=H;end;elseif d<=137 then local j=X[3];d,X=29,j;elseif d<=138 then d=not(jU<156)and 59 or 151;else local j=k(B,C+jU);F(q,jU,(V(l[mU],j,M)));local j,j=I[mU],J(K(q,D),(K(q,4)));d,M=88,j;end;elseif d<=142 then if d<=140 then local j=z(M,r(mU,C),1+C);d,M=88,j;elseif d<=141 then bU(q,jU,(V(M,k(B,C+jU),l[mU])));local j,j,b=I[mU],k(q,D),k(q,4);if not not(b~=0)then d,C,M=155,j,b;else d,M=88,j;end;else F(vU,wU,(V(k(mU,M+wU),l[C],rU)));lU=I[C];d,C=146,lU;end;elseif d<=144 then if d<=143 then local j=r(mU,2+M);d,jU=not(128>j)and 25 or 181,j;else local j=r(B,3+C);local b,O,w,P,K=M-128,(D-128)*16384,128*(mU-128),j%128*2097152,j%128;local W,H,z,Q=(j-K)*2097152,b+O,w+P;Q,d,C=W+(H+z),115,4+C;M=Q;end;elseif d<=145 then d=not not(mU<=64)and 76 or 102;else local j,b,O=X[4],X[5],X[2];local w,P=j+b,b<=0;b,j=w>=O,w<=O;O=P and b or not P and j;X[4]=w;if O then d,wU=142,w;else d=137;end;end;elseif d<=171 then if d<=158 then if d<=152 then if d<=149 then if d<=147 then d,C=23,C+1;elseif d<=148 then local j=X[3];d,X,M=88,j,jU(vU);else local j=M(C,B,D);d,M=88,j;end;elseif d<=150 then d,M=2,1+M;elseif d<=151 then local j,b,O=1+M,133,25;local w,P=0,(b*((C+153)%256)+O)%256;d,C,M,D,jU,bU,TU,vU,rU,OU,wU=73,j,153,b,O,w,P,S,q,r(mU,j+w),V;else local j=X[2];d,X=32,j;end;elseif d<=155 then if d<=153 then local j,b,O=(M-128)*128,16384*(D-128);O,d,C=b+(B+j),23,3+C;M=O;elseif d<=154 then d,D=149,D+1;else d=not(M>=2147483648)and 86 or 180;end;elseif d<=156 then d=not(46>=mU)and 94 or 67;elseif d<=157 then local j,j=M+1;do j=true;end;d=j and 45 or 9;else d,M=170,1+M;end;elseif d<=164 then if d<=161 then if d<=159 then local j=r(mU,C+1);d,D=j<128 and 44 or 50,j;elseif d<=160 then local j,b=D-1,1+0;local O={OU-b,j+0,X,nil,b};d,X=99,O;else local j,b,O,w=1+M,(C+122)%256,2054847098,0;local P=k(B,j+w);F(q,w,(V(O,l[b],P)));P=I[b];w=4;d,C,M,mU,jU=139,j,O,P,w;end;elseif d<=162 then VU=M+1;d,M=126,VU;elseif d<=163 then FU=(bU*C+TU)%256;S(vU,rU,(V(FU,r(mU,M+rU),B)));d,C=71,FU;else d,D,M=170,128*(D-128)+mU,M+2;end;elseif d<=167 then if d<=165 then d,jU,M=98,bU+(jU-128)*128,M+2;elseif d<=166 then local j=r(mU,3+C);local b,O,w,I,P=M-128,(D-128)*16384,(B-128)*128,j%128*2097152,j-j%128;local j,K,W=2097152*P+w,I+b;W,d,C=j+(O+K),140,C+4;M=W;else local j=M+1;local b,O,O=r(B,j),1+j,M+2;j=r(B,O);d,C,M,D=not(j>=128)and 158 or 3,b,O,j;end;elseif d<=169 then if d<=168 then d,B,M=107,mU+(B-128)*128,M+2;else local j,b,O,w=128*(B-128),16384*(jU-128);O,w,d=b+(j+mU),M+3,129;B=O;end;elseif d<=170 then local j=r(B,M);if not(128<=j)then d,B=157,j;else d,mU=15,j;end;else local j=X[1];d,X,M=88,j,C;end;elseif d<=183 then if d<=177 then if d<=174 then if d<=172 then d,M,C=115,mU+(128*(M-128)+16384*(D-128)),3+C;elseif d<=173 then local j=r(mU,M+3);local b,O,w,I,P=D-128,(B-128)*16384,128*(jU-128),j%128*2097152,j%128;local K,W,H=(j-P)*2097152,b+w;H,d,M=W+(K+O)+I,2,M+4;D=H;else d=not(mU<=36)and 120 or 128;end;elseif d<=175 then d,mU,M=63,(mU-128)*128+jU,M+2;elseif d<=176 then d,M=37,1+M;else kU=(TU+bU*C)%256;S(vU,mU,(V(jU,r(B,M+mU),kU)));d,C=43,kU;end;elseif d<=180 then if d<=178 then d,M,C=115,D+128*(M-128),2+C;elseif d<=179 then d=not(jU<=159)and 39 or 55;else local j=M-4294967296;d,M=86,j;end;elseif d<=181 then local j,b,O=(D-128)*128,(B-128)*16384;O,d,M=jU+b+j,114,M+3;D=O;elseif d<=182 then local j,b,O=X[1],X[5],X[4];local w,I=j+b,b<=0;b,j=w>=O,w<=O;O=I and b or not I and j;X[1]=w;if O then d,wU=135,w;else d=40;end;else local j=r(vU,M+1);d,bU=not(128<=j)and 165 or 118,j;end;elseif d<=189 then if d<=186 then if d<=184 then local j=r(mU,2+C);d,B=128>j and 153 or 134,j;elseif d<=185 then local j;B,d,j=B+(mU-128)*128,45,2+M;else local j=r(mU,M+1);if not(j<128)then d,jU=122,j;else d,mU=104,j;end;end;elseif d<=187 then d,D,M=37,128*(D-128)+mU,2+M;elseif d<=188 then local j,b,b=M+1,0,(25+(105+C)%256*133)%256;S(q,0,(V(r(mU,j+0),105,b)));d,M=88,r(q,B);else local j=r(mU,3+D);local b,O,w,I,P=B-128,16384*(jU-128),(bU-128)*128,j%128*2097152,j%128;local S,K,W=2097152*(j-P),I+(O+w);W,d,D=K+(b+S),149,D+4;B=W;end;elseif d<=192 then if d<=190 then local j,b,O,w=M+1,(77+C)%256,1296911693,0;F(q,w,(V(k(B,j+w),O,l[b])));d,C,M,mU=92,j,b,O;elseif d<=191 then local j=r(vU,M);d,jU=j<128 and 117 or 183,j;else local j=r(B,3+M);local b,O,w,F,q=D-128,16384*(mU-128),128*(jU-128),2097152*(j%128),j-j%128;local j,k,l=w+2097152*q,b+O;l,d,M=j+k+F,37,4+M;D=l;end;elseif d<=194 then if d<=193 then local j=r(vU,1+M);d,mU=not(128<=j)and 168 or 14,j;else local j,b,r=X[4],X[5],X[1];local O,w=j+b,b<=0;j,b=O>=r,O<=r;r=w and j or not w and b;X[4]=O;if r then d,wU=119,O;else d=152;end;end;elseif d<=195 then d,mU,M=63,128*(mU-128)+(16384*(jU-128)+bU),3+M;else d,M=63,1+M;end;end;end};v[6]=T;e,u=11,T;else e,a=m:q6(U,u);end;else e,Y,t=m:S6(G,Y,u,e,i,t,U);end;else local j,b,T,v,r,O=m:U6(x,t,a,A,u,e,_,U);if j==2 then return N,y;elseif j==1 then e,u,t,a,x=b,T,v,r,O;end;end;end;end
```


## `O6`  (2,258589 - 2,259016)

参数: m, j, b, T, v, r, O, w, F, q  长度: 427

```lua
function(m,j,b,T,v,r,O,w,F,q)if b<=15 then local k=m[27](j,3+F);local l,V,I,P,S=v-128,(T-128)*16384,(w-128)*128,k%128*2097152,k%128;local w=(k-S)*2097152;k=P+V+(l+w+I);return 28,4+F,q,r,k;elseif b<=16 then local b,w=128*(q-128),16384*(O-128);local O=b+r+w;return 42,3+F,O,r,v;else local b=m[27](j,3+F);local m,j,O,w=r-128,16384*(v-128),128*(T-128),b%128*2097152;local T=(b-b%128)*2097152+(m+(j+O)+w);return 20,4+F,q,T,v;end;end
```


## `R6`  (2,3099 - 2,3574)

参数: m, j, b, T, v, r, O, w, F, q, k, l  长度: 475

```lua
function(m,j,b,T,v,r,O,w,F,q,k,l)if r<=1 then if r<=0 then local V=(k-128)*128;local I=16384*(w-128)+V+v;return 12,q,O,3+T,b,I;else local v=m[27](l,T+3);local V,I,P,S,K=b-128,16384*(k-128),(w-128)*128,2097152*(v%128),v%128;local W=2097152*(v-K);K=P+I+W+(V+S);return 19,q,O,T+4,K,k;end;elseif r<=2 then q[O]=T;local v,r,V=m:z6(q,l);local I=m[27](l,V);return 128>I and 32 or 29,v,r,V,I,k;else local v=(w+k*O)%256;m[47](l,b,(m[103](T,m[27](F,b+j),v)));return 9,q,v,T,b,k;end;end
```


## `S6`  (2,296923 - 2,297071)

参数: m, j, b, T, v, r, O, w  长度: 148

```lua
function(m,j,b,T,v,r,O,w)if v<=29 then local v=m[27](w,T+1);return v<128 and 7 or 28,b,v;else local m,T=j-1,1+0;return 9,{nil,r-T,b,T,m+0},O;end;end
```


## `T6`  (2,296187 - 2,296622)

参数: m, j, b, T, v, r, O, w, F, q, k, l, V  长度: 435

```lua
function(m,j,b,T,v,r,O,w,F,q,k,l,V)if r<=5 then if r<=4 then local I,P=m[83],m[67](O,b+l);I(V,b,(m[103](q,m.P6[F],P)));return 17,m.M6[F],j,O,l,T;else local b=w[6];if not b then return 27,F,j,O,l,T;else return 11,F,b,O,l,T;end;end;elseif r<=6 then return 12,F,1+j,O,l,T;elseif r<=7 then local b=v+128*(T-128);return 19,F,2+j,O,l,b;else local b,T=k[5][F],k[4];local v=b+1;b=m[27](T,v);return not not(128<=b)and 35 or 21,F,j,T,v,b;end;end
```


## `U6`  (2,237280 - 2,237603)

参数: m, j, b, T, v, r, O, w, F  长度: 323

```lua
function(m,j,b,T,v,r,O,w,F)if O<=32 then if O<=31 then return 2;else return 1,19,r+1,b,T,j;end;elseif O<=33 then local q=m[27](w,v+2);return 1,q<128 and 10 or 24,r,b,q,j;elseif O<=34 then local O=m[27](F,2+r);return 1,not(O>=128)and 0 or 16,r,b,T,O;else local b=m[27](w,v+1);return 1,not(128<=b)and 14 or 33,r,b,T,j;end;end
```


## `V6`  (2,228663 - 2,229110)

参数: m, j, b, T, v, r, O, w, F, q  长度: 447

```lua
function(m,j,b,T,v,r,O,w,F,q)if v<=23 then if v<=22 then local k=m[27](w,1+q);return 128>k and 23 or 34,O,q,F,r,j,k;else local w=T+(j-128)*128;return 12,O,q+2,F,r,w,T;end;elseif v<=24 then local w=m[27](b,F+3);local m,b,k,l=r-128,(j-128)*16384,(T-128)*128,w%128*2097152;local V=(w-w%128)*2097152+(m+k+l)+b;return 15,O,q,4+F,V,j,T;elseif v<=25 then return 30,O[5],q,F,r,j,T;else local m=(r-128)*128+((j-128)*16384+T);return 19,O,3+q,F,m,j,T;end;end
```


## `X6`  (2,264523 - 2,264873)

参数: m, j, b, T, v, r, O, w  长度: 350

```lua
function(m,j,b,T,v,r,O,w)if w<=37 then local F,q,k=v-83470,m[27](T,b),1+b;O[7]=not(q==0);q=m[118](F);O[5]=q;local m=1+0;return 38,{r,1-m,m,nil,F+0},k,q,j;elseif w<=38 then local m,T,O=r[2],r[3],r[5];local w,F=m+T,T<=0;m,T=w>=O,w<=O;O=F and m or not F and T;r[2]=w;if O then return 4,r,b,v,w;else return 39,r,b,v,j;end;else return 2,r[1],b,v,j;end;end
```


## `Y6`  (2,237201 - 2,237276)

参数: m, j, b, T  长度: 75

```lua
function(m,j,b,T)local v=m[108];v();for m,r in j,b,T do v(true,m,r);end;end
```


## `_6`  (2,24 - 2,537)

参数: m, j, b, T, v, r, O, w, F, q, k, l  长度: 513

```lua
function(m,j,b,T,v,r,O,w,F,q,k,l)if w<=15 then local V,I,P,S=(r+O)%256,m[38](k),r*16843009,k-k%4;local k,K=S-1,4+0;return 17,{K,0-K,nil,k+0,q},V,r,133,25,I,P,S,b;elseif w<=16 then local w=m[27](F,r+3);local m,k,V,I,P=l-128,16384*(T-128),(j-128)*128,w%128*2097152,w%128;local S=2097152*(w-P);w=V+m+(I+k)+S;return 12,q,O,4+r,w,T,F,j,v,b;else local m,w,k=q[2],q[1],q[4];local V,I=m+w,w<=0;m,w=V>=k,V<=k;k=I and m or not I and w;q[2]=V;if k then return 4,q,O,r,l,T,F,j,v,V;else return 25,q,O,r,l,T,F,j,v,b;end;end;end
```


## `b6`  (2,227385 - 2,227589)

参数: m, j, b, T, v, r, O  长度: 204

```lua
function(m,j,b,T,v,r,O)if O<=19 then if O<=18 then return 2,m[72](T),v,j;else local T=m[27](b,r);return not not(T>=128)and 22 or 6,r,v,T;end;elseif O<=20 then return 5,r,v,j;else return 15,r,v+1,j;end;end
```


## `c6`  (2,234551 - 2,234970)

参数: m, j, b, T  长度: 419

```lua
function(m,j,b,T)local v,r,O,w,F,q,k,l=m[127],m[112],m[26],7,j,T,b;while true do if w<=3 then if w<=1 then if w<=0 then w=v(F,"%:([%d]+)[%:\13\10]")and 3 or 5;else return;end;elseif w<=2 then q(k..l..": "..F,0);w=1;else j=q[k];if j then w,q,k,l=2,r,"LPH:",j;else w,q,k=4,r,"LPH:";end;end;elseif w<=5 then if w<=4 then w,l=2,"?";else r(F,0);w=1;end;elseif w<=6 then r(F,1);w=1;else w=O(F)=="string"and 0 or 6;end;end;end
```


## `d6`  (2,230487 - 2,230633)

参数: m, j, b, T, v, r, O  长度: 146

```lua
function(m,j,b,T,v,r,O)if v<=21 then local v=m[27](b,2+r);return not(128>v)and 15 or 40,r,O,v;else local m=(O-128)*128+j;return 20,r+2,m,T;end;end
```


## `e6`  (2,5568 - 2,5842)

参数: m, j, b, T, v, r, O, w, F, q  长度: 274

```lua
function(m,j,b,T,v,r,O,w,F,q)if v<=18 then local k=128*(q-128)+F;return 28,b,O+2,T,k;elseif v<=19 then local v=m[27](b,2+O);return not(v>=128)and 16 or 24,b,O,v,q;else local v=m[38](T);m[94](v,0,b,O,T);local b=T+O;r[w]=v;m[2]=b;return 23,m:L6(r,j,169)(nil,m.D),O,T,q;end;end
```


## `g6`  (2,226774 - 2,227014)

参数: m, j, b, T, v, r, O, w, F, q, k  长度: 240

```lua
function(m,j,b,T,v,r,O,w,F,q,k)if j<=26 then local l,V=85*(w-O),(T-39)*614125;local O=7225*(b-39)+((q-39)*1+(l+v))+V;r[k]=O;return 35,O,b;elseif j<=27 then local j=m[27](F,r+1);return j<128 and 18 or 21,w,j;else q[k]=T;return 38,w,b;end;end
```


## `i6`  (2,5156 - 2,5522)

参数: m, j, b, T, v, r, O, w, F, q  长度: 366

```lua
function(m,j,b,T,v,r,O,w,F,q)if T<=10 then if T<=9 then local k,l,V=r[2],r[4],r[5];local I,P=k+l,l<=0;l,k=I>=V,I<=V;V=P and l or not P and k;r[2]=I;if V then return 3,w,I;else return 13,w,j;end;else local r=128*(j-128);local k=(F-128)*16384+(r+O);return 15,3+w,k;end;elseif T<=11 then return 2,w,j;else local T,r=m[27](v,q),q+1;m[59](b,j+w,T,F);return 31,w,j;end;end
```


## `j6`  (2,297568 - 2,298033)

参数: m, j, b, T, v, r, O, w, F, q  长度: 465

```lua
function(m,j,b,T,v,r,O,w,F,q)if T<=1 then if T<=0 then local k=m[27](O,j+2);return not not(128<=k)and 17 or 34,j,w,b,r,F,k;else return 37,j+1,w,b,r,F,q;end;elseif T<=2 then local k=m[27](O,j);return not not(128<=k)and 9 or 12,j,w,4,k,F,q;elseif T<=3 then local T,k=m[67](v,w),m[27](v,4+w);local v=4294967296*k+T;local l=j[v];if not not l then return 35,j,l,b,r,F,q;else return 30,j,T,k,v,F,q;end;else local T=m[27](O,j);return 128>T and 11 or 27,j,w,b,r,T,q;end;end
```


## `k6`  (2,233696 - 2,234547)

参数: m  长度: 851

```lua
function(m,...)local j,b,T,v,r,O,w,F,q,k,l,V,I=m:s6();local P,S,K,W,H,z,Q,o,n,E,p,c=b,T,v,r,O,w,F,q,k,l,V,I;while j do if P<=20 then if P<=9 then if P<=4 then P,W,z,Q,o,n,E=m:j6(W,Q,P,H,o,K,z,n,E);elseif P<=6 then P,W,H,Q=m:K6(Q,H,o,W,P,S);else P,S,K,W,H,z,n=m:u6(S,W,K,n,z,P,H);end;elseif P<=14 then P,W,Q=m:G6(K,Q,P,H,W);elseif P<=17 then P,W,z,o,n=m:O6(K,P,E,n,o,Q,p,W,z);else P,K,W,o,n=m:e6(z,K,o,P,H,W,Q,E,n);end;elseif P<=31 then if P<=25 then if P<=22 then P,W,o,p=m:d6(n,K,p,P,W,o);else b,l,r,T,I,v,V=m:r6(o,z,P,W,K,Q,S,H);if b==1 then return K;elseif b==2 then P,S,K,W,H,z=l,r,T,I,v,V;end;end;elseif P<=28 then P,z,E=m:g6(P,E,n,p,W,c,z,K,Q,o);else P,z,o,n,E,p,c=m:o6(n,z,P,K,p,c,W,o,E);end;elseif P<=36 then P,K,W,z,Q,o=m:H6(Q,P,z,K,o,H,W,n,E);elseif P<=39 then P,S,W,Q,o=m:X6(o,W,K,Q,S,H,P);else P,W,z,Q,n=m:v6(Q,p,z,W,n,S,P,E,K);end;end;end
```


## `o6`  (2,259051 - 2,259363)

参数: m, j, b, T, v, r, O, w, F, q  长度: 312

```lua
function(m,j,b,T,v,r,O,w,F,q)if T<=29 then local k=m[27](v,1+w);return not(k>=128)and 5 or 31,b,k,j,q,r,O;elseif T<=30 then local j=b%256;local T=(b-j)/256;local k=T%256;T=(T-k)/256;local l=T%256;return 26,k,F,l,(T-l)/256,(j-39)*52200625,39;else local j=m[27](v,2+w);return 128>j and 36 or 32,b,F,j,q,r,O;end;end
```


## `q6`  (2,259945 - 2,260020)

参数: m, j, b  长度: 75

```lua
function(m,j,b)local T=m[27](j,2+b);return not not(T>=128)and 1 or 26,T;end
```


## `r6`  (2,3597 - 2,3950)

参数: m, j, b, T, v, r, O, w, F  长度: 353

```lua
function(m,j,b,T,v,r,O,w,F)if T<=23 then return 1;elseif T<=24 then local T=m[27](r,3+v);local q,k,l,V,I=b-128,(O-128)*16384,128*(j-128),2097152*(T%128),T%128;local j=2097152*(T-I);I=k+q+(l+(j+V));return 2,42,w,r,4+v,F,I;else local j,T=w[1],m[104](m[39](m.F6,5),m.p6,m.l6);local v,r,O=m[46](T),#T-1,5+0;T=0-O;return 2,41,{nil,O,r+0,T,j},0,{},v,b;end;end
```


## `s6`  (2,225890 - 2,225962)

参数: m  长度: 72

```lua
function(m)return true,8,nil,nil,nil,nil,nil,nil,nil,nil,nil,nil,nil;end
```


## `u6`  (2,260024 - 2,260313)

参数: m, j, b, T, v, r, O, w  长度: 289

```lua
function(m,j,b,T,v,r,O,w)if O<=7 then local F=j[5];m.P=w;local q,k=m.P,m[2];local l=m[27](q,k);return not(128<=l)and 14 or 13,F,q,k,{},l,v;elseif O<=8 then local O=1+0;return 6,{j,0-O,255+0,O,nil},133,25,w,r,v;else local v=m[27](T,b+1);return not not(v>=128)and 0 or 22,j,T,b,w,r,v;end;end
```


## `v6`  (2,4389 - 2,4721)

参数: m, j, b, T, v, r, O, w, F, q  长度: 332

```lua
function(m,j,b,T,v,r,O,w,F,q)if w<=40 then local k=(r-128)*128+(b+(F-128)*16384);return 28,3+v,T,j,k;elseif w<=41 then local b,w,F=O[4],O[2],O[3];local k,l=b+w,w<=0;w,b=k>=F,k<=F;F=l and w or not l and b;O[4]=k;if F then return 3,v,k,j,r;else return 7,v,T,j,r;end;else local j=m[27](q,v);return not(j<128)and 29 or 1,v,T,j,r;end;end
```


## `z6`  (2,231154 - 2,233692)

参数: m, j, b  长度: 2538

```lua
function(m,j,b)local T,v,r,O,w,F,q,k,l,V,I,P,S,K,W,H,z,Q,o,n,E,p,c=m:b();local s,R,L,Z,J,e,Y,h,N,y,u,_,A,G,t,a,U,x,i,d,X,g,f,C=v,r,b,j,O,w,F,q,k,l,V,I,P,S,K,W,H,z,Q,o,n,E,p,c;while T do if s<=80 then if s<=39 then if s<=19 then if s<=9 then if s<=4 then s,J,e,A,i=m:V(Y,s,A,e,i,G,J,L,h);else s,J,e,Y,h,i=m:q(i,h,y,J,s,Y,N,e,L);end;elseif s<=14 then p,V,r,v,w,F,Q=m:S(y,L,e,N,J,Y,f,h,s);if p==1 then s,J,e,Y,y,f=V,r,v,w,F,Q;elseif p==2 then return h,J,e;end;else s,R,e,y,A,i,d=m:U(y,t,G,L,R,i,d,h,s,A,J,e);end;elseif s<=29 then if s<=24 then s,J,e,Y,A,a,U=m:s(s,x,e,h,Y,U,J,A,a,L);elseif s<=26 then s,e,U=m:j(i,U,L,s,e,d);else s,R,e,Y,h,U,x=m:K(e,y,s,Y,x,R,h,N,U,L);end;elseif s<=34 then s,R,e,h,U,i=m:u(U,L,s,e,i,h,R);else s,R,e,h,_,X=m:G(s,y,R,X,L,A,G,h,_,e);end;elseif s<=59 then if s<=49 then if s<=44 then s,e,y,G=m:O(Y,e,L,u,y,s,G,t);else s,R,e,Y,U,g=m:e(C,R,i,s,g,f,U,L,d,e,Y,x);end;elseif s<=54 then s,e,_,U,i=m:d(L,e,U,X,d,s,i,_);else s,R,e,Y,_,G,t,U=m:r(h,G,R,e,U,x,_,t,s,Y);end;elseif s<=69 then if s<=64 then s,R,J,e,Y,h,N,A=m:g(Y,N,h,s,R,L,e,J,A);else s,e,h,u,_=m:o(G,h,u,_,L,s,e,A);end;elseif s<=74 then s,R,e,h,y=m:H(Y,x,s,R,u,U,i,L,h,y,e);elseif s<=77 then s,e,_,U=m:X(s,U,x,Y,i,_,e,L);else s,e,y,g=m:v(u,g,y,s,_,e,L);end;elseif s<=121 then if s<=100 then if s<=90 then if s<=85 then if s<=82 then s,e,h=m:z(s,R,Y,L,h,e);else s,e,A,i=m:Y(d,X,L,e,i,s,A);end;elseif s<=87 then s,J,e,h=m:c(h,y,L,e,s,u,Y,J);else s,G,t,a=m:F(R,L,e,s,G,a,t);end;elseif s<=95 then s,e,u,t,a=m:p(U,s,t,_,e,Y,A,u,a,L);else s,J,e,u,x,g=m:l(L,s,Y,g,x,C,J,e,u,f);end;elseif s<=110 then if s<=105 then s,J,e,y,a,d=m:k(d,U,G,u,x,y,e,Y,a,J,s,_,L);elseif s<=107 then s,J,e=m:w(e,L,J,s,h,Y);else s,Z,e,Y,h,N,d=m:t(d,R,h,N,e,Z,s,Y);end;elseif s<=115 then if s<=112 then s,e,G=m:x(s,G,e,L);else s,J,e,h,y,t=m:a(i,Z,G,d,a,A,s,L,h,J,t,Y,e,_,U,u,y,N,x);end;elseif s<=118 then s,e,_,G=m:W(_,L,s,Y,G,e,A,t,a);else s,A,x,d=m:y(x,e,A,s,L,d);end;elseif s<=141 then if s<=131 then if s<=126 then s,e,U,g=m:Z(s,L,f,J,i,x,U,e,g);elseif s<=128 then s,e,Y,A=m:n(e,s,A,G,t,Y,L,h);else s,R,e,h,u=m:f(e,s,h,R,y,u,L);end;elseif s<=136 then if s<=133 then s,y,U=m:h(e,s,y,U,L);else s,y,_,i=m:C(i,e,y,s,_,R,L);end;else s,e,h,u,A,G=m:A(L,i,s,N,t,A,g,h,u,G,X,e);end;elseif s<=151 then if s<=146 then s,J,e,h,y,A=m:m(y,N,A,_,e,G,Y,L,J,h,s,u,Z);else s,R,e,h,y,u,C=m:B(C,s,e,L,_,R,h,u,y);end;elseif s<=156 then if s<=153 then s,e,h,a=m:E(s,h,L,e,a,y);else s,e,u,A,G=m:N(e,u,s,A,a,L,t,G);end;elseif s<=159 then s,R,J,e,U=m:Q(U,J,e,R,i,s,L);else s,N,y,X=m:I(y,L,R,s,X,N,e);end;end;end
```


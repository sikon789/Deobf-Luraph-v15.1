# Luraph v15.1 — VM 语义解剖（自动生成）

样本：`8.lua`（329 KB，单行 Luau）

- VM 槽位总数：**180**
- handler 函数：**83**
- 可识别原语：**87**

## 一、VM 原语表（m[N] → 真实 API）

| 槽位 | 原语 |
|---|---|
| `m[1]` | `table.clear` |
| `m[4]` | `coroutine.create` |
| `m[5]` | `coroutine.isyieldable` |
| `m[7]` | `pcall` |
| `m[8]` | `Vector3.new` |
| `m[9]` | `buffer.readf32` |
| `m[10]` | `rawset` |
| `m[11]` | `bit32.bnot` |
| `m[14]` | `string.byte` |
| `m[15]` | `rawget` |
| `m[16]` | `buffer.writei8` |
| `m[19]` | `setmetatable` |
| `m[21]` | `assert` |
| `m[22]` | `setfenv` |
| `m[23]` | `coroutine.status` |
| `m[24]` | `coroutine.resume` |
| `m[25]` | `Rect.new` |
| `m[26]` | `type` |
| `m[27]` | `buffer.readu8` |
| `m[28]` | `bit32.countrz` |
| `m[31]` | `buffer.writestring` |
| `m[32]` | `string.format` |
| `m[34]` | `Color3.new` |
| `m[35]` | `getfenv` |
| `m[36]` | `UDim2.new` |
| `m[37]` | `buffer.tostring` |
| `m[38]` | `buffer.create` |
| `m[39]` | `string.sub` |
| `m[41]` | `buffer.readi16` |
| `m[42]` | `table.pack` |
| `m[43]` | `tostring` |
| `m[44]` | `buffer.writef32` |
| `m[46]` | `buffer.fromstring` |
| `m[47]` | `buffer.writeu8` |
| `m[49]` | `bit32.band` |
| `m[51]` | `UDim.new` |
| `m[53]` | `bit32.lrotate` |
| `m[55]` | `table.insert` |
| `m[56]` | `table.concat` |
| `m[57]` | `buffer.writeu16` |
| `m[58]` | `coroutine.close` |
| `m[59]` | `buffer.fill` |
| `m[61]` | `string.unpack` |
| `m[62]` | `unpack` |
| `m[64]` | `buffer.readstring` |
| `m[65]` | `string.pack` |
| `m[66]` | `buffer.writei16` |
| `m[67]` | `buffer.readu32` |
| `m[68]` | `buffer.writei32` |
| `m[69]` | `pairs` |
| `m[70]` | `xpcall` |
| `m[71]` | `Vector2.new` |
| `m[75]` | `buffer.len` |
| `m[76]` | `string.gmatch` |
| `m[80]` | `getmetatable` |
| `m[81]` | `string.char` |
| `m[82]` | `string.find` |
| `m[83]` | `buffer.writeu32` |
| `m[84]` | `buffer.readf64` |
| `m[86]` | `tonumber` |
| `m[90]` | `string.rep` |
| `m[91]` | `table.move` |
| `m[92]` | `bit32.rshift` |
| `m[93]` | `vector.create` |
| `m[94]` | `buffer.copy` |
| `m[96]` | `ipairs` |
| `m[97]` | `next` |
| `m[103]` | `bit32.bxor` |
| `m[104]` | `string.gsub` |
| `m[106]` | `buffer.writebits` |
| `m[108]` | `coroutine.yield` |
| `m[109]` | `coroutine.running` |
| `m[110]` | `bit32.lshift` |
| `m[111]` | `typeof` |
| `m[112]` | `error` |
| `m[113]` | `bit32.countlz` |
| `m[114]` | `buffer.readi8` |
| `m[116]` | `buffer.readu16` |
| `m[117]` | `bit32.bor` |
| `m[118]` | `table.create` |
| `m[119]` | `buffer.readbits` |
| `m[120]` | `buffer.writef64` |
| `m[121]` | `buffer.readi32` |
| `m[124]` | `coroutine.wrap` |
| `m[125]` | `select` |
| `m[126]` | `bit32.rrotate` |
| `m[127]` | `string.match` |

## 二、handler 分派表

每个 handler 返回的第一个值是「下一个状态码」，据此可重建状态机。

| 槽位 | handler | 参数个数 | 后继状态 |
|---|---|---|---|
| `m[A]` | `A` | 13 | [61, 88, 160] |
| `m[B]` | `B` | 10 | [58, 61, 144] |
| `m[C]` | `C` | 8 | [32, 51, 139, 158] |
| `m[E]` | `E` | 7 | [11] |
| `m[F]` | `F` | 8 | [31, 49] |
| `m[G]` | `G` | 11 | [58, 119, 135] |
| `m[H]` | `H` | 12 | [19, 22, 33, 148] |
| `m[I]` | `I` | 8 | [79, 131] |
| `m[K]` | `K` | 11 | [61, 136] |
| `m[L]` | `L` | 1 | — |
| `m[N]` | `N` | 9 | [57, 88] |
| `m[O]` | `O` | 9 | [19, 57, 63, 138] |
| `m[Q]` | `Q` | 8 | [52, 124] |
| `m[R]` | `R` | 1 | — |
| `m[S]` | `S` | 10 | [1, 2] |
| `m[T]` | `T` | 1 | — |
| `m[U]` | `U` | 13 | [38, 82, 148, 160] |
| `m[V]` | `V` | 10 | [29, 38, 52, 63] |
| `m[W]` | `W` | 10 | [14, 57, 105, 119] |
| `m[X]` | `X` | 9 | [103] |
| `m[Y]` | `Y` | 8 | [17] |
| `m[Z]` | `Z` | 10 | [17, 103, 138] |
| `m[a]` | `a` | 20 | [14, 148] |
| `m[b]` | `b` | 1 | — |
| `m[c]` | `c` | 9 | [11, 45] |
| `m[d]` | `d` | 9 | [17, 34, 74, 103] |
| `m[e]` | `e` | 13 | [22, 110, 138] |
| `m[f]` | `f` | 8 | [11, 114] |
| `m[g]` | `g` | 10 | [82, 119, 134] |
| `m[h]` | `h` | 6 | — |
| `m[j]` | `j` | 7 | [52] |
| `m[k]` | `k` | 14 | [29, 89, 148] |
| `m[l]` | `l` | 11 | [63, 88, 138] |
| `m[m]` | `m` | 14 | [14, 19, 106, 134] |
| `m[n]` | `n` | 9 | [38, 108] |
| `m[o]` | `o` | 9 | [11, 119, 144] |
| `m[p]` | `p` | 11 | [29, 45, 144] |
| `m[q]` | `q` | 10 | [45, 61, 67, 108] |
| `m[r]` | `r` | 11 | [39, 67, 84, 89, 103, 144] |
| `m[s]` | `s` | 11 | [29, 45, 108, 136] |
| `m[t]` | `t` | 9 | [10, 46, 47, 108, 118] |
| `m[u]` | `u` | 8 | [57, 110, 143, 152] |
| `m[v]` | `v` | 8 | [19, 67] |
| `m[w]` | `w` | 7 | [63, 88] |
| `m[x]` | `x` | 5 | [38] |
| `m[y]` | `y` | 7 | — |
| `m[z]` | `z` | 7 | [16, 73] |
| `m[13]` | `13` | 16 | — |
| `m[18]` | `18` | 3 | — |
| `m[20]` | `20` | 2 | — |
| `m[63]` | `63` | 2 | — |
| `m[73]` | `73` | 4 | — |
| `m[99]` | `99` | 4 | — |
| `m[D6]` | `D6` | 4 | [15] |
| `m[G6]` | `G6` | 6 | [6, 20, 28, 42] |
| `m[H6]` | `H6` | 10 | [20, 37, 41, 42] |
| `m[K6]` | `K6` | 7 | [10, 25, 37] |
| `m[L6]` | `L6` | 4 | — |
| `m[O6]` | `O6` | 10 | [20, 28, 42] |
| `m[R6]` | `R6` | 12 | [9, 12, 19] |
| `m[S6]` | `S6` | 8 | [9] |
| `m[T6]` | `T6` | 13 | [11, 12, 17, 19, 27] |
| `m[U6]` | `U6` | 9 | [1, 2] |
| `m[V6]` | `V6` | 10 | [12, 15, 19, 30] |
| `m[X6]` | `X6` | 8 | [2, 4, 38, 39] |
| `m[Y6]` | `Y6` | 4 | — |
| `m[_6]` | `_6` | 12 | [4, 12, 17, 25] |
| `m[b6]` | `b6` | 7 | [2, 5, 15] |
| `m[c6]` | `c6` | 4 | — |
| `m[d6]` | `d6` | 7 | [20] |
| `m[e6]` | `e6` | 10 | [23, 28] |
| `m[g6]` | `g6` | 11 | [35, 38] |
| `m[i6]` | `i6` | 10 | [2, 3, 13, 15, 31] |
| `m[j6]` | `j6` | 10 | [30, 35, 37] |
| `m[k6]` | `k6` | 1 | — |
| `m[o6]` | `o6` | 10 | [26] |
| `m[q6]` | `q6` | 3 | — |
| `m[r6]` | `r6` | 9 | [1, 2] |
| `m[s6]` | `s6` | 1 | — |
| `m[u6]` | `u6` | 8 | [6] |
| `m[v6]` | `v6` | 10 | [3, 7, 28] |
| `m[z6]` | `z6` | 3 | — |
| `m[102]` | `102` | 18 | — |

## 三、主循环结构

```lua
function(m,...)local j,b,T,v,r,O,w,F,q,k,l,V,I=m:s6();local P,S,K,W,H,z,Q,o,n,E,p,c=b,T,v,r,O,w,F,q,k,l,V,I;while j do if P<=20 then if P<=9 then if P<=4 then P,W,z,Q,o,n,E=m:j6(W,Q,P,H,o,K,z,n,E);elseif P<=6 then P,W,H,Q=m:K6(Q,H,o,W,P,S);else P,S,K,W,H,z,n=m:u6(S,W,K,n,z,P,H);end;elseif P<=14 then P,W,Q=m:G6(K,Q,P,H,W);elseif P<=17 then P,W,z,o,n=m:O6(K,P,E,n,o,Q,p,W,z);else P,K,W,o,n=m:e6(z,K,o,P,H,W,Q,E,n);end;elseif P<=31 then if P<=25 then if P<=22 then P,W,o,p=m:d6(n,K,p,P,W,o);else b,l,r,T,I,v,V=m:r6(o,z,P,W,K,Q,S,H);if b==1 then return K;elseif b==2 then P,S,K,W,H,z=l,r,T,I,v,V;end;end;elseif P<=28 then P,z,E=m:g6(P,E,n,p,W,c,z,K,Q,o);else P,z,o,n,E,p,c=m:o6(n,z,P,K,p,c,W,o,E);end;elseif P<=36 then P,K,W,z,Q,o=m:H6(Q,P,z,K,o,H,W,n,E);elseif P<=39 then P,S,W,Q,o=m:X6(o,W,K,Q,S,H,P);else P,W,z,Q,n=m:v6(Q,p,z,W,n,S,P,E,K);end;end;end
```

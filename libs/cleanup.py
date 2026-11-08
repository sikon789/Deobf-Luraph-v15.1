#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Luraph v15.1 Cleanup Module V2
More intelligent framework removal
"""

def has_lua_comments(toks, idx):
    """Check if there's a Lua comment at this index"""
    if idx < 2:
        return False
    t1, v1 = toks[idx-2]
    t2, v2 = toks[idx-1]
    if v1 == '--' and t2 == 'c':
        return True
    return False

def find_matching_end(toks, start_idx):
    """Find the matching 'end' for a function statement"""
    if start_idx >= len(toks):
        return None
    depth = 0
    if toks[start_idx][0] == 'w' and toks[start_idx][1] == 'function':
        depth = 1
        k = start_idx + 1
        while k < len(toks) and depth > 0:
            if toks[k][0] == 'w':
                if toks[k][1] in ('function', 'if', 'do', 'for', 'while'):
                    depth += 1
                elif toks[k][1] == 'end':
                    depth -= 1
            elif toks[k][0] == 'o':
                if toks[k][1] in ('(', '[', '{'):
                    depth += 1
                elif toks[k][1] in (')', ']', '}'):
                    depth -= 1
            if depth == 0:
                return k
            k += 1
    return None

def cleanup_luraph_v2(toks, mode='business', keep_business=True):
    """
    Clean up Luraph framework remnants
    mode: 'full' - remove all framework code
          'business' - keep business logic, remove partial framework
    """
    to_remove = set()
    
    # Pattern 1: Identify and remove handler definitions (like [41] = function)
    for i, (t, v) in enumerate(toks):
        if t == 'o' and v == '=' and i > 0:
            if i > 0 and toks[i-1][0] == 'o' and toks[i-1][1].isdigit() and toks[i-2][0] == 'o' and toks[i-2][1].isdigit():
                j = i + 1
                while j < len(toks) and not (toks[j][0] == 'w' and toks[j][1] == 'function'):
                    j += 1
                if j < len(toks) and toks[j][1] == 'function':
                    end_idx = find_matching_end(toks, j)
                    if end_idx:
                        for x in range(j, end_idx + 1):
                            if not has_lua_comments(toks, x):
                                to_remove.add(x)
    
    # Pattern 2: Remove main dispatcher (like rk = function...)
    for i, (t, v) in enumerate(toks):
        if t == 'w' and v == 'rk':
            j = i + 1
            if j < len(toks) and toks[j][0] == 'o' and toks[j][1] == '=':
                j += 1
            while j < len(toks) and not (toks[j][0] == 'w' and toks[j][1] == 'function'):
                j += 1
            if j < len(toks) and toks[j][1] == 'function':
                end_idx = find_matching_end(toks, j)
                if end_idx:
                    for x in range(j, end_idx + 1):
                        if not has_lua_comments(toks, x):
                            to_remove.add(x)
    
    # Pattern 3: Remove debug dead loops
    i = 0
    while i < len(toks) - 10:
        if (i+2 < len(toks) and 
            toks[i][0] == 'w' and toks[i][1] == 'while' and
            toks[i+1][0] == 'w' and toks[i+1][1] == 'true' and
            toks[i+2][0] == 'w' and toks[i+2][1] == 'do'):
            end_idx = find_matching_end(toks, i + 3)
            if end_idx:
                block_text = ' '.join(v for _,v in toks[i:end_idx+1])
                if 'pcall' in block_text or 'break' in block_text:
                    for x in range(i, end_idx + 1):
                        if not has_lua_comments(toks, x):
                            to_remove.add(x)
                i = end_idx + 1
                continue
        i += 1
    
    cleaned = []
    for i, (t, v) in enumerate(toks):
        if i in to_remove:
            continue
        cleaned.append((t, v))
    
    return cleaned

if __name__ == "__main__":
    print("Cleanup Module V2 Ready")

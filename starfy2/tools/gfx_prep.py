#!/usr/bin/env python3
"""Prepare upstream asm/graphics.asm for merging into the main build (scratch copy only).
usage: gfx_prep.py TREE GFX_BASE [AREA]   (AREA default 0x200000; the 16 MiB build uses 0x80000)
- writes TREE/asm/graphics_merged.asm: .open rom/output.gba (not outputGFX.gba), the 0x09000000 block moved to
  GFX_BASE (0x09000000 is where Atlas puts the uncompressed text), incbin paths case-resolved and quoted.
- checks for overlapping writes between VWF.asm, script.asm and the merged graphics (exit 1 on overlap)."""
import sys, os, re
tree, base = sys.argv[1], int(sys.argv[2], 16); area = int(sys.argv[3], 16) if len(sys.argv) > 3 else 0x200000
def ci(rel):
    cur = tree
    for p in rel.replace('\\', '/').split('/'):
        c = os.path.join(cur, p)
        if not os.path.exists(c) and os.path.isdir(cur):
            m = [e for e in os.listdir(cur) if e.lower() == p.lower()]
            if m: c = os.path.join(cur, m[0])
        cur = c
    return os.path.relpath(cur, tree)
src = open(os.path.join(tree, 'asm/graphics.asm'), encoding='latin-1').read()
src = src.replace('"rom/outputGFX.gba"', '"rom/output.gba"')
src = re.sub(r'(?im)^\.org 0x09000000\s*\n\.area 0x09000004', '.org 0x%08X\n.area 0x%08X' % (base, area), src)
missing = []
def fix(m):
    p = ci(m.group(2).strip('"'))
    if not os.path.exists(os.path.join(tree, p)): missing.append(p)
    return '%s"%s"' % (m.group(1), p)
src = re.sub(r'(?im)^(\s*\.incbin\s+)("[^"]+"|[^\s;]+)', fix, src)
open(os.path.join(tree, 'asm/graphics_merged.asm'), 'w', encoding='latin-1').write(src)
if missing: print('gfx: MISSING incbin files:', missing); sys.exit(1)
# --- overlap check: simulate .org / .align / .incbin / .word / .byte per file (comments stripped, ; and //)
def ranges(path, name):
    pc = None; out = []
    for raw in open(os.path.join(tree, path), encoding='latin-1'):
        l = re.sub(r';.*|//.*', '', raw).strip()
        if not l: continue
        m = re.match(r'(?i)\.org\s+0x([0-9a-f]+)', l)
        if m: pc = int(m.group(1), 16); continue
        m = re.match(r'(?i)\.align\s+(\d+)', l)
        if m and pc is not None: a = int(m.group(1)); pc = (pc + a - 1) // a * a; continue
        m = re.match(r'(?i)\.incbin\s+"?([^"]+)"?', l)
        if m and pc is not None:
            n = os.path.getsize(os.path.join(tree, ci(m.group(1).strip())))
            out.append((pc, pc + n, name + ':' + m.group(1))); pc += n; continue
        m = re.match(r'(?i)\.(word|byte|halfword)\s+(.*)', l)
        if m and pc is not None:
            k = {'word': 4, 'byte': 1, 'halfword': 2}[m.group(1).lower()] * len(m.group(2).split(','))
            out.append((pc, pc + k, name + ':.' + m.group(1))); pc += k
    return out
R = ranges('asm/VWF/VWF.asm', 'VWF') + ranges('asm/script.asm', 'script') + ranges('asm/graphics_merged.asm', 'gfx')
R.sort(); bad = 0
for (a1, b1, n1), (a2, b2, n2) in zip(R, R[1:]):
    if a2 < b1 and not ('gfx' in (n1[:3], n2[:3])):
        print('gfx: note (pre-existing upstream overlap) 0x%08X-0x%08X %s  with  0x%08X-0x%08X %s' % (a1, b1, n1, a2, b2, n2))
    elif a2 < b1:
        print('gfx: OVERLAP 0x%08X-0x%08X %s  with  0x%08X-0x%08X %s' % (a1, b1, n1, a2, b2, n2)); bad += 1
g = [r for r in R if r[2].startswith('gfx')]
print('gfx: %d graphics writes, relocated block 0x%08X-0x%08X, %d overlaps' % (len(g), base, max(b for a, b, n in g if a >= base), bad))
sys.exit(1 if bad else 0)

#!/usr/bin/env python3
"""Edit overlay/asm/bin/graphics/minigamemenu/1minigamemenuOBJ.bin in place (run after bomb_shower.py): the minigame-menu
title 'Don't Drop'em' (OBJ tile rows 4-5) becomes 'Don't Drop 'Em' (S2-D009, decision A: same spelling as the 8-6 goal
text and the get 'em fixes). The apostrophe moves 3 px right (4 px word gap after 'p'), 'e' is replaced by a
hand-drawn capital E in the same 2 px stroke and cap height as the D, and the outline (colour 2) is regenerated as the
radius-2 square dilation of the white mask (same rule as bomb_shower.py) for x=38..95. The closing bracket at x>=96 and
'Don't' are untouched. Idempotent: does nothing if the E is already there."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import lz10
HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
DST = os.path.join(HERE, 'overlay/asm/bin/graphics/minigamemenu/1minigamemenuOBJ.bin')
raw = bytearray(lz10.decompress(open(DST, 'rb').read())); R0, W = 4, 16
g = [[0]*(W*8) for _ in range(16)]
for rr in range(2):
    for c in range(W):
        t = (R0+rr)*32 + c
        for y in range(8):
            for x in range(8):
                b = raw[t*32 + y*4 + x//2]; g[rr*8+y][c*8+x] = (b >> 4) if x & 1 else b & 15
wh = [[v == 1 for v in row] for row in g]
# upstream pixels (white): p 65-70, apostrophe 72-73 (rows 2-5), e 75-80 (rows 7-13), m 82-89; bracket outline from x=96
if wh[3][78] and wh[12][78]: print('dont_drop_em: already applied'); sys.exit(0)
assert wh[3][72] and not wh[3][75] and wh[8][75], 'unexpected source pixels'
apos = [[wh[y][x] for x in range(72, 74)] for y in range(16)]
m = [[wh[y][x] for x in range(82, 90)] for y in range(16)]
E = ["#####", "#####", "##...", "##...", "##...", "####.", "####.", "##...", "##...", "##...", "#####", "#####"]  # rows 2..13 (D's cap height)
for y in range(16):
    for x in range(72, 96): wh[y][x] = False
    for i in range(2): wh[y][75+i] = apos[y][i]              # apostrophe 75-76: 4 px gap after p = word space
    if 2 <= y <= 13:
        for i, ch in enumerate(E[y-2]): wh[y][78+i] = ch == '#'   # E 78-82
    for i in range(8): wh[y][84+i] = m[y][i]                 # m 84-91, outline ends at 93 (bracket outline starts 96)
for y in range(16):
    for x in range(38, 96):
        near = any(wh[yy][xx] for yy in range(max(0, y-2), min(16, y+3)) for xx in range(x-2, x+3))
        g[y][x] = 1 if wh[y][x] else 2 if near else 0
for rr in range(2):
    for c in range(W):
        t = (R0+rr)*32 + c
        for y in range(8):
            for xp in range(0, 8, 2):
                raw[t*32 + y*4 + xp//2] = g[rr*8+y][c*8+xp] | g[rr*8+y][c*8+xp+1] << 4
open(DST, 'wb').write(lz10.compress(bytes(raw)))
print('dont_drop_em: wrote', DST, os.path.getsize(DST), 'bytes')

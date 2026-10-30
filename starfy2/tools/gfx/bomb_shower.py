#!/usr/bin/env python3
"""Generate overlay/asm/bin/graphics/minigamemenu/1minigamemenuOBJ.bin: upstream's minigame-menu OBJ sheet with the
temp title 'FureFureBomber' (tile rows 6-7, 4bpp, 32 tiles/row) redrawn as 'Bomb Shower' (backfill/glossary.csv).
Letters B o m b e r are upstream's own pixels from 'FureFureBomber', h from 'Chu-Chu'; S and w are hand-drawn in the same
2 px stroke style. The outline (colour 2) is regenerated as a radius-2 square dilation of the white (colour 1) mask; this
reproduces upstream's outline of 'FureFureBomber' to within 2 pixels. Brackets 「 」 are kept as upstream drew them."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import lz10
HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
SRC = os.path.join(HERE, 'repo/asm/bin/graphics/minigamemenu/1minigamemenuOBJ.bin')
DST = os.path.join(HERE, 'overlay/asm/bin/graphics/minigamemenu/1minigamemenuOBJ.bin')
raw = bytearray(lz10.decompress(open(SRC, 'rb').read()))
def rowpix(r0):
    g = [[0]*128 for _ in range(16)]
    for rr in range(2):
        for c in range(16):
            t = (r0+rr)*32 + c
            for y in range(8):
                for x in range(8):
                    b = raw[t*32 + y*4 + x//2]; g[rr*8+y][c*8+x] = (b >> 4) if x & 1 else b & 15
    return g
g6, g8 = rowpix(6), rowpix(8)
cut = lambda g, a, b: [[g[y][x] == 1 for x in range(a, b)] for y in range(16)]
def art(rows, top):
    m = [[False]*len(rows[0]) for _ in range(16)]
    for i, r in enumerate(rows):
        for x, c in enumerate(r): m[top+i][x] = c == '#'
    return m
G = {'B': cut(g6, 61, 68), 'o': cut(g6, 69, 74), 'm': cut(g6, 75, 83), 'b': cut(g6, 84, 89), 'e': cut(g6, 90, 96),
     'r': cut(g6, 97, 102), 'h': cut(g8, 12, 18),
     'S': art(["..#####", ".######", "###....", "##.....", "###....", ".#####.", ".#####.", "....###", ".....##", "....###",
               "######.", "#####.."], 2),
     'w': art(["##.##.##"]*5 + ["########", ".######."], 7)}
TEXT, X0 = 'Bomb Shower', 18          # centred between the brackets (text area x=10..102); 5 px word gap like 'Color Matcher'
white = [[False]*128 for _ in range(16)]; x = X0
for ch in TEXT:
    if ch == ' ': x += 4; continue
    for y in range(16):
        for i, c in enumerate(G[ch][y]):
            if c: white[y][x+i] = True
    x += len(G[ch][0]) + 1
assert x - 1 <= 102, 'title runs into the closing bracket'
for y in range(16):
    for xx in range(8, 104):                     # cols <8 = 「, >=104 = 」 (untouched)
        near = any(white[yy][xc] for yy in range(max(0, y-2), min(16, y+3)) for xc in range(xx-2, xx+3))
        g6[y][xx] = 1 if white[y][xx] else 2 if near else 0
for rr in range(2):
    for c in range(16):
        t = (6+rr)*32 + c
        for y in range(8):
            for xp in range(0, 8, 2):
                raw[t*32 + y*4 + xp//2] = g6[rr*8+y][c*8+xp] | g6[rr*8+y][c*8+xp+1] << 4
os.makedirs(os.path.dirname(DST), exist_ok=True)
open(DST, 'wb').write(lz10.compress(bytes(raw)))
print('wrote', DST, os.path.getsize(DST), 'bytes')

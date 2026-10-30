#!/usr/bin/env python3
"""enemy_counter.py OUT.bin  - 1-2 Star Spin training counter 'あと' ('... to go') -> 'LEFT' (reads "LEFT 30").
The counter is drawn from uncompressed OBJ tiles at 0x087D3E58 (DMA'd to OBJ tile 960 by 0x0803BB50, palette 0x087D4418
-> OBJ pal 15): tiles 0-3 = 16x16 and tiles 4-5 = 8x16 make the 24x16 word, tiles 6.. are the pink digits (kept).
New word in the same style as the kana: white body (1), grey bottom shade (d), black outline (2), 2-px strokes.
Pure new pixel art (no ROM data); written over the 6 word tiles in place by overlay/patches/50_enemy_counter.asm."""
import sys
L = ["11..", "11..", "11..", "11..", "11..", "11..", "11..", "11..", "11..", "1111", "1111"]
E = ["1111", "1111", "11..", "11..", "11..", "111.", "11..", "11..", "11..", "1111", "1111"]
F = ["1111", "1111", "11..", "11..", "11..", "111.", "11..", "11..", "11..", "11..", "11.."]
T = ["1111", "1111", ".11.", ".11.", ".11.", ".11.", ".11.", ".11.", ".11.", ".11.", ".11."]
W, H = 24, 16; g = [[0] * W for _ in range(H)]; x0, y0 = 2, 2
for i, ch in enumerate((L, E, F, T)):
    for y, row in enumerate(ch):
        for x, c in enumerate(row):
            if c == '1': g[y0 + y][x0 + i * 5 + x] = 1
for y in range(H):                        # bottom shade
    for x in range(W):
        if g[y][x] == 1 and (y + 1 >= H or g[y + 1][x] == 0): g[y][x] = 0xD
out = [r[:] for r in g]
for y in range(H):
    for x in range(W):
        if g[y][x] == 0 and any(0 <= y + dy < H and 0 <= x + dx < W and g[y + dy][x + dx] for dy in (-1, 0, 1) for dx in (-1, 0, 1)): out[y][x] = 2
def tiles(x0, w):
    b = bytearray()
    for ty in range(2):
        for tx in range(w // 8):
            for y in range(8):
                for x in range(0, 8, 2):
                    px = out[ty * 8 + y]; b.append(px[x0 + tx * 8 + x] | px[x0 + tx * 8 + x + 1] << 4)
    return b
data = tiles(0, 16) + tiles(16, 8)
assert len(data) == 6 * 32
open(sys.argv[1], 'wb').write(data)
for r in out: print(''.join('%x' % v if v else '.' for v in r))

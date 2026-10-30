#!/usr/bin/env python3
"""staff_logo.py BASE.gba OUT.lz [PREVIEW.png]  - the small logo at the start of the staff roll, made English to match the title.
The staff roll draws '伝説のスタフィー2' from OBJ sprites: LZ block 0x086A1B70 (header 01 00 00 00 6a 00 00 00: 106 tiles from
OBJ tile 127; pointers 0x08114838, 0x082C7EB4, 0x082C7F44), OBJ palettes 3 (yellow/orange fill, ROM 0x086A2288) and 4 (blue
outline, white, pinks; 0x086A22A8). Nine sprites, fixed by the game's frame data (screen x, y, w, h, first tile, palette):
the palette-3 fill layer (sprites 0-1) is drawn over the palette-4 outline layer (sprites 2-8).
The English title logo (tools/gfx/title_logo.py compose()) is scaled down to the JP logo's 96x40 box and split into the
two layers by nearest palette colour; fill pixels outside the fill sprites fall back to the outline layer's palette.
Same tiles, same palettes, same sprites. Output ROM-derived -> patches/gen/ (never committed); 60_title_logo.asm repoints."""
import sys, os, struct
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); import lz10, title_logo
SRC, PTRS, T0, NT = 0x086A1B70, (0x08114838, 0x082C7EB4, 0x082C7F44), 127, 106
PAL3, PAL4 = 0x086A2288, 0x086A22A8
SPR = [(12, 60, 64, 32, 127, 3), (76, 76, 8, 16, 159, 3), (81, 62, 16, 32, 161, 4), (97, 62, 8, 32, 169, 4), (8, 56, 64, 32, 173, 4),
       (72, 56, 32, 32, 217, 4), (8, 88, 32, 8, 205, 4), (40, 88, 32, 8, 209, 4), (72, 88, 32, 8, 213, 4)]
BX, BY, BW, BH = 9, 60, 96, 35          # target box: the fill sprites start at y=60, the outline sprites end at y=95
def pal(r, a):
    return [((c & 31) << 3, (c >> 5 & 31) << 3, (c >> 10 & 31) << 3) for c in struct.unpack_from('<16H', r, a - 0x08000000)]
def main(base, out, preview=None):
    r = open(base, 'rb').read()
    for p in PTRS: assert struct.unpack_from('<I', r, p - 0x08000000)[0] == SRC, hex(p)
    d = lz10.decompress(r, SRC - 0x08000000); d = bytearray(d[0] if isinstance(d, tuple) else d)
    assert d[:8] == bytes([1, 0, 0, 0, NT, 0, 0, 0]) and len(d) == 8 + NT * 32
    P3, P4 = pal(r, PAL3), pal(r, PAL4)
    canvas, *_ = title_logo.compose(r); BG = title_logo.bg_palette(r)
    ys, xs = np.nonzero(canvas); canvas = canvas[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    h, w = canvas.shape; s = min(BW / w, BH / h); nw, nh = round(w * s), round(h * s)
    rgba = np.zeros((h, w, 4), np.uint8)
    for y in range(h):
        for x in range(w):
            if canvas[y, x]: rgba[y, x] = BG[canvas[y, x]] + (255,)
    # premultiplied box downscale so transparent pixels don't darken the edges
    im = Image.fromarray(rgba, 'RGBA'); small = np.asarray(im.resize((nw, nh), Image.BOX), float)
    ox, oy = BX + (BW - nw) // 2, BY + (BH - nh) // 2
    lay3 = {}; lay4 = {}
    def near(c, P, rng): return min(rng, key=lambda i: sum((a - b) ** 2 for a, b in zip(c, P[i])))
    def dist(c, P, i): return sum((a - b) ** 2 for a, b in zip(c, P[i]))
    def in_spr(x, y, pn):
        return any(pp == pn and sx <= x < sx + sw and sy <= y < sy + sh for sx, sy, sw, sh, t, pp in SPR)
    for y in range(nh):
        for x in range(nw):
            R, G, B, A = small[y, x]
            if A < 110: continue
            c = (R, G, B); X, Y = ox + x, oy + y
            i4 = near(c, P4, range(1, 16)); i3 = near(c, P3, range(1, 10))
            if in_spr(X, Y, 3) and dist(c, P3, i3) < dist(c, P4, i4): lay3[X, Y] = i3
            lay4[X, Y] = i4
    nd = bytearray(d[:8]) + bytearray(NT * 32)
    def put(t, lx, ly, v):
        o = 8 + (t - T0) * 32 + ly * 4 + lx // 2; nd[o] |= v << (4 * (lx & 1))
    for sx, sy, sw, sh, t0, pn in SPR:
        lay = lay3 if pn == 3 else lay4
        for (X, Y), v in lay.items():
            if sx <= X < sx + sw and sy <= Y < sy + sh:
                lx, ly = X - sx, Y - sy; t = t0 + (ly // 8) * (sw // 8) + lx // 8
                put(t, lx & 7, ly & 7, v)
    miss = [k for k in lay4 if not any(pp == 4 and sx <= k[0] < sx + sw and sy <= k[1] < sy + sh for sx, sy, sw, sh, t, pp in SPR)]
    assert not miss, "pixels outside the outline sprites: %d" % len(miss)
    lz = lz10.compress(bytes(nd)); open(out, 'wb').write(lz)
    print("staff_logo: %dx%d at (%d,%d), %d fill + %d outline px, %d B LZ -> %s" % (nw, nh, ox, oy, len(lay3), len(lay4), len(lz), out))
    if preview:
        img = Image.new('RGB', (128, 64), (16, 64, 160))
        for (X, Y), v in lay4.items(): img.putpixel((X - 0, Y - 48), P4[v])
        for (X, Y), v in lay3.items(): img.putpixel((X - 0, Y - 48), P3[v])
        img.resize((512, 256), Image.NEAREST).save(preview)
if __name__ == '__main__': main(*sys.argv[1:4])

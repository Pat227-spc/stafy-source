#!/usr/bin/env python3
"""goal_banner.py BASE.gba OUT.lz  - 4-3 (Shiver Race) finish banner 'ゴール' -> 'GOAL'.
Source: LZ block 0x087FDFB0 (header 01 00 00 00 63 00 00 00: 99 OBJ tiles from tile 413, palette 6; only pointer 0x082A94C4).
The banner is sprites 32x16 @413, 32x8 @421, 32x16 @425, 32x8 @433 (64x24 px). The red kana are painted out with the
row's cloth shade, then GOAL is drawn in the banner's red (7 body, 8 top edge), split by the cloth crease like the kana.
All 3 flutter frames (tiles 0-32, 33-65, 66-98) are edited; the letters follow each frame's hem offset.
ROM-derived output -> patches/gen/ (never committed)."""
import sys, os, struct
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import lz10
SRC, PTR, T0 = 0x087FDFB0, 0x082A94C4, 413
SPR = [(0, 0, 32, 16, 413), (0, 16, 32, 8, 421), (32, 0, 32, 16, 425), (32, 16, 32, 8, 433)]
G = ["..777777.", ".77777777", "777......", "777......", "777......", "777..7777", "777..7777", "777...777", "777...777", ".77777777", "..777777."]
O = ["..77777..", ".7777777.", "777...777", "777...777", "777...777", "777...777", "777...777", "777...777", "777...777", ".7777777.", "..77777.."]
A = ["...777...", "..77777..", ".777.777.", "777...777", "777...777", "777777777", "777777777", "777...777", "777...777", "777...777", "777...777"]
L = ["777......"] * 9 + ["777777777"] * 2
RED = {7, 8, 9, 10, 11}
def main(base, out):
    r = open(base, 'rb').read()
    assert struct.unpack_from('<I', r, PTR - 0x08000000)[0] == SRC
    d = bytearray(lz10.decompress(r, SRC - 0x08000000)); d = d[0] if isinstance(d, tuple) else d
    assert d[:8] == bytes([1, 0, 0, 0, 0x63, 0, 0, 0]), d[:8].hex()
    def at(f, x, y):
        for sx, sy, w, h, t0 in SPR:
            if sx <= x < sx + w and sy <= y < sy + h:
                lx, ly = x - sx, y - sy; t = f * 33 + t0 - T0 + (ly // 8) * (w // 8) + lx // 8
                return 8 + t * 32 + (ly & 7) * 4 + (lx & 7) // 2, (lx & 1) * 4
    def get(f, x, y): o, s = at(f, x, y); return (d[o] >> s) & 15
    def put(f, x, y, v): o, s = at(f, x, y); d[o] = (d[o] & ~(15 << s) & 255) | (v << s)
    X0, X1, CREASE = 5, 58, range(27, 32)
    def hem(f, x): return max([y for y in range(12, 24) if get(f, x, y) in RED] or [None])
    for f in range(3):                                    # 3 flutter frames of 33 tiles, same sprite layout
        dy = [0] * 64
        for x in range(X0, X1 + 1):
            a, b = hem(0, x), hem(f, x)
            dy[x] = max(-2, min(2, b - a)) if a is not None and b is not None else 0
        orig = [[get(f, x, y) for x in range(64)] for y in range(24)]
        for x in range(X0, X1 + 1):                       # paint out the kana with the local cloth shade
            if x in CREASE: continue
            for y in range(6 + dy[x], 21 + dy[x]):
                if orig[y][x] in RED:
                    near = Counter(orig[y][xx] for xx in range(max(X0, x - 6), min(X1, x + 6) + 1)
                                   if xx not in CREASE and orig[y][xx] not in RED and orig[y][xx] > 1)
                    put(f, x, y, near.most_common(1)[0][0] if near else 2)
        for gl, x0 in ((G, 7), (O, 18), (A, 34), (L, 46)):  # GOAL, following the cloth's wave per column
            for yy, line in enumerate(gl):
                for xx, c in enumerate(line):
                    if c == '7':
                        top = yy == 0 or gl[yy - 1][xx] != '7'
                        put(f, x0 + xx, 9 + yy + dy[x0 + xx], 8 if top else 7)
    lz = lz10.compress(bytes(d)); open(out, 'wb').write(lz)
    print("goal_banner: %d tiles, %d B LZ -> %s" % (d[4], len(lz), out))
if __name__ == '__main__': main(*sys.argv[1:3])

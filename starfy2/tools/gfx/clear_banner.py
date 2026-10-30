#!/usr/bin/env python3
"""clear_banner.py BASE_ROM OUT.lz [PREVIEW.png]
English 'CLEAR!!' for the treasure-chest / stage-clear scene banner (JP 'クリア!!', cutscene index 2/19).
The banner is OBJ tiles in the LZ block at 0x088DBB78 (pointer at 0x08121EB8; 8-byte header + 4bpp tiles, tile k = VRAM
OBJ tile k). The scene lays it out with OAM entries (captured in scratch/clear/oam.bin):
  main  : 32x16 @ (72,4) (104,4) (136,4) tiles 0xD4/0xDC/0xE4; 32x8 @ (80,20) (112,20) 0xEC/0xF0; 16x8 @ (144,20) 0xF4;
          8x8 @ (160,20) 0xF6
  shadow: 32x16 @ (69,9) (101,9) (133,9) 0x13E/0x146/0x14E; 8x16 @ (165,9) 0x156; 32x8 @ (77,25) (109,25) (141,25)
          0x158/0x15C/0x160
The '!!' is kept pixel for pixel. C L E A R are drawn as stroke masks and shaded with the banner's own bevel (outline 2, top
highlight 1/4, body 5/6/7, bottom shade 3/7) and the shadow layer (colour 9) is the main silhouette moved down 5 px and
smeared 0-2 px left (closest fit to the hand-drawn JP shadow). The block is written out whole (it is built from the base ROM at build time, never committed)."""
import sys, os, struct
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import lz10
SRC = 0x088DBB78
MAIN = [(72, 4, 32, 16, 0xD4), (104, 4, 32, 16, 0xDC), (136, 4, 32, 16, 0xE4), (80, 20, 32, 8, 0xEC), (112, 20, 32, 8, 0xF0),
        (144, 20, 16, 8, 0xF4), (160, 20, 8, 8, 0xF6)]
SHAD = [(69, 9, 32, 16, 0x13E), (101, 9, 32, 16, 0x146), (133, 9, 32, 16, 0x14E), (165, 9, 8, 16, 0x156),
        (77, 25, 32, 8, 0x158), (109, 25, 32, 8, 0x15C), (141, 25, 32, 8, 0x160)]
L = {
 'C': ["..#########", ".##########", "###########", "###########"] + ["#####......"]*12 + ["###########", "###########", ".##########", "..#########"],
 'L': ["#####....."]*16 + ["##########"]*4,
 'E': ["##########"]*4 + ["#####....."]*4 + ["#########."]*4 + ["#####....."]*4 + ["##########"]*4,
 'A': ["...######...", "..########..", ".##########.", "############"] + ["#####..#####"]*6 + ["############"]*4 + ["#####..#####"]*6,
 'R': ["#########..", "##########.", "###########", "###########", "#####..####", "#####..####", "###########", "###########",
       "##########.", "#########..", "#####.####.", "#####..###.", "#####..####"] + ["#####..####"]*7,
}
def tile_px(blk, t, x, y):
    b = blk[8 + t*32 + y*4 + x//2]; return b >> 4 if x & 1 else b & 15
def set_px(blk, t, x, y, v):
    o = 8 + t*32 + y*4 + x//2; blk[o] = (blk[o] & 0x0F) | (v << 4) if x & 1 else (blk[o] & 0xF0) | v
def screen(blk, sprites):
    s = {}
    for sx, sy, w, h, t0 in sprites:
        for y in range(h):
            for x in range(w):
                t = t0 + (y//8)*(w//8) + x//8; s[(sx+x, sy+y)] = tile_px(blk, t, x % 8, y % 8)
    return s
def write(blk, sprites, s):
    cov = set()
    for sx, sy, w, h, t0 in sprites:
        for y in range(h):
            for x in range(w):
                t = t0 + (y//8)*(w//8) + x//8; set_px(blk, t, x % 8, y % 8, s.get((sx+x, sy+y), 0)); cov.add((sx+x, sy+y))
    lost = [p for p, v in s.items() if v and p not in cov]
    assert not lost, 'pixels outside the sprites: %s' % lost[:5]
def shade(mask):
    out = {}
    inside = lambda p: p in mask
    for (x, y) in mask:
        du = next(d for d in range(1, 40) if (x, y-d) not in mask); dd = next(d for d in range(1, 40) if (x, y+d) not in mask)
        dl = next(d for d in range(1, 40) if (x-d, y) not in mask); dr = next(d for d in range(1, 40) if (x+d, y) not in mask)
        side = min(dl, dr)
        if du == 1:   v = 2 if side == 1 else 1
        elif dd == 1: v = 2 if side == 1 else 7
        elif dd == 2: v = 7 if side == 1 else 3
        elif du == 2: v = 1 if side == 1 else 4 if side == 2 else 7
        elif du == 3: v = 1 if side == 1 else 7 if side == 2 else 6 if side == 3 else 5
        else:         v = 3 if dl == 1 or dr == 1 else 7 if dl == 2 else 5
        out[(x, y)] = v
    for (x, y) in mask:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                q = (x+dx, y+dy)
                if q not in mask: out[q] = 2
    return out
def main():
    rom = open(sys.argv[1], 'rb').read(); blk = bytearray(lz10.decompress(rom, SRC - 0x08000000))
    m0 = screen(blk, MAIN)
    # shadow: the original is hand-drawn; the closest simple model (fitted against the JP banner) is the main silhouette
    # moved down 5 and smeared 0..2 px to the left
    SHIFTS = [(-2, 5), (-1, 5), (0, 5)]
    KEEP = 149                                     # x >= 149: the '!!' (kept as drawn)
    mask = set(); x = 81; top = 6
    for ch in 'CLEAR':
        rows = L[ch]
        for yy, r in enumerate(rows):
            for xx, c in enumerate(r):
                if c == '#': mask.add((x+xx, top+yy))
        x += len(rows[0]) + 3
    assert x - 3 + 1 < KEEP, 'letters run into the !! (x=%d)' % x
    new = {p: v for p, v in m0.items() if p[0] >= KEEP}
    new.update({p: v for p, v in shade(mask).items() if p[0] < KEEP})
    sil = {p for p, v in new.items() if v}
    shad = {(px+dx, py+dy): 9 for px, py in sil for dx, dy in SHIFTS}
    write(blk, MAIN, new); write(blk, SHAD, shad)
    open(sys.argv[2], 'wb').write(lz10.compress(bytes(blk)))
    print('clear_banner: letters x=81..%d, %d bytes' % (x-4, os.path.getsize(sys.argv[2])))
    if len(sys.argv) > 3:
        from PIL import Image
        P = {0: (0, 90, 0), 1: (240, 240, 240), 2: (8, 8, 8), 3: (248, 248, 0), 4: (248, 168, 80), 5: (248, 64, 32),
             6: (184, 48, 0), 7: (128, 48, 0), 8: (216, 136, 64), 9: (184, 48, 0)}
        im = Image.new('RGB', (120, 40), P[0]); px = im.load()
        for layer in (shad, new):
            for (a, b), v in layer.items():
                if v and 60 <= a < 180 and 0 <= b < 40: px[a-60, b] = P.get(v, (255, 0, 255))
        im.resize((480, 160), Image.NEAREST).save(sys.argv[3])
main()

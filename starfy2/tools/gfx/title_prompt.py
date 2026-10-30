#!/usr/bin/env python3
"""title_prompt.py BASE_ROM OUTDIR [PREVIEW.png]
English 'PRESS START!' for the title screen prompt (JP 'スタートボタンを おしてね!').
The data is at:
- the title OBJ sheet: LZ at 0x0890294C = 0x088F6B3C + 0xBE10. The offset is a literal at 0x080DC924 used by the title loader at 0x080DC7BC.
- 13-sprite animation frames at 0x08957194: 20 frames of 82 bytes = count.h + 13 x (attr0, attr1, attr2) + pad.h.
  Frames 0-9 are the dark letters (wave) and 10-19 the semi-transparent glow, which cycles 4 flicker variants per glyph.
Outputs (OUTDIR, built from the base ROM, never committed):
- title_obj.lz: the sheet with P R E S T A drawn over the kana tile groups. The glow variants are made by fitting each JP variant
  (shift direction/amount, inner colour) and applying the same model to the new letter. '!' and its glow are kept.
- title_frames.bin: the 20 frames re-laid out as "PRESS" / "START!", keeping JP's per-slot wave heights and flicker order.
  The 2 spare sprites point at an emptied tile group."""
import sys, os, struct
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import lz10
SHEET = 0x0890294C; FRAMES = 0x08957194; NF, FSZ = 20, 0x52
MASK = {  # interior (fill) masks, 6 x 7, drawn at cols 3..8 rows 4..10 of the 16x16 cell (outline rows 3..11 like the kana)
 'P': ["#####.", "##..##", "##..##", "#####.", "##....", "##....", "##...."],
 'R': ["#####.", "##..##", "##..##", "#####.", "##.##.", "##..##", "##..##"],
 'E': ["######", "##....", "##....", "#####.", "##....", "##....", "######"],
 'S': [".#####", "##....", "##....", ".####.", "....##", "....##", "#####."],
 'T': ["######", "..##..", "..##..", "..##..", "..##..", "..##..", "..##.."],
 'A': ["..##..", ".####.", "##..##", "##..##", "######", "##..##", "##..##"],
}
# letter -> (main 16x16 tile group, glow pool base) reusing the kana slots' tiles: ス タ ー ト ボ ン
SLOT = {'P': (0x00, 0x40), 'R': (0x04, 0x2E), 'E': (0x08, 0x50), 'S': (0x0C, 0x60), 'T': (0x10, 0x70), 'A': (0x14, 0x80)}
JP_GLOW = [0x40, 0x2E, 0x50, 0x60, 0x70, 0x2E, 0x80, 0x90, 0xA0, 0xB0, 0xC0, 0xD0, 0xE0]   # JP slot -> glow pool base
EMPTY_MAIN, EMPTY_GLOW = 0x18, 0x90          # を: emptied, used by the 2 spare sprites
def get16(sh, t):
    g = [[0]*16 for _ in range(16)]
    for y in range(16):
        for x in range(16):
            tt = t + (y//8)*2 + x//8; b = sh[tt*32 + (y % 8)*4 + (x % 8)//2]; g[y][x] = b >> 4 if x & 1 else b & 15
    return g
def put16(sh, t, g):
    for y in range(16):
        for x in range(0, 16, 2):
            tt = t + (y//8)*2 + x//8; sh[tt*32 + (y % 8)*4 + (x % 8)//2] = g[y][x] | g[y][x+1] << 4
def glyph(ch):
    fill = {(3+x, 4+y) for y, r in enumerate(MASK[ch]) for x, c in enumerate(r) if c == '#'}
    g = [[0]*16 for _ in range(16)]
    for (x, y) in fill:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if (x+dx, y+dy) not in fill: g[y+dy][x+dx] = 2
    for (x, y) in fill: g[y][x] = 3 if y >= 9 else 1
    return g
def glow(g, p):
    d, n, inner, dx = p
    S = {(x, y) for y in range(16) for x in range(16) if g[y][x]}
    out = [[0]*16 for _ in range(16)]
    for k in range(n, -1, -1):
        for (x, y) in S:
            X, Y = x+dx, y+d*k
            if 0 <= X < 16 and 0 <= Y < 16: out[Y][X] = inner if k == 0 else 5 if k == 1 else 6
    return out
def fit(g, v):
    best = None
    for d in (-1, 1):
        for n in (0, 1, 2):
            for inner in (1, 5):
                for dx in (-1, 0, 1):
                    m = glow(g, (d, n, inner, dx)); e = sum(m[y][x] != v[y][x] for y in range(16) for x in range(16))
                    if best is None or e < best[0]: best = (e, (d, n, inner, dx))
    return best
def main():
    rom = open(sys.argv[1], 'rb').read(); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
    sh = bytearray(lz10.decompress(rom, SHEET - 0x08000000))
    fr = rom[FRAMES - 0x08000000: FRAMES - 0x08000000 + NF*FSZ]
    errs = []
    jp_main = {0x40: 0x00, 0x2E: 0x04, 0x50: 0x08, 0x60: 0x0C, 0x70: 0x10, 0x80: 0x14}
    for ch, (mt, gp) in SLOT.items():
        jg = get16(sh, jp_main[gp]); ng = glyph(ch)
        for k in range(4):
            e, p = fit(jg, get16(sh, gp + 4*k)); errs.append(e)
            put16(sh, gp + 4*k, glow(ng, p))
        put16(sh, mt, ng)
    blank = [[0]*16 for _ in range(16)]
    put16(sh, EMPTY_MAIN, blank)
    for k in range(4): put16(sh, EMPTY_GLOW + 4*k, blank)
    # frames
    nfr = bytearray(fr)
    for f in range(NF):
        o = f*FSZ; n = struct.unpack_from('<H', fr, o)[0]; assert n == 13
        E = [list(struct.unpack_from('<HHH', fr, o + 2 + 6*i)) for i in range(13)]
        ys = [((a0 & 255) ^ 128) - 128 for a0, _, _ in E]
        glowf = f >= 10
        def var(slot):
            return ((E[slot][2] & 1023) - JP_GLOW[slot]) // 4 if glowf else 0
        def ent(tmpl, x, y, tile):
            a0, a1, a2 = tmpl
            return [(a0 & 0xFF00) | (y & 255), (a1 & 0xFE00) | (x & 511), (a2 & 0xFC00) | tile]
        new = []
        for j, ch in enumerate('PRESS'):
            mt, gp = SLOT[ch]; new.append(ent(E[0], -24 + 9*j, ys[j], gp + 4*var(j) if glowf else mt))
        for j, ch in enumerate('START'):
            mt, gp = SLOT[ch]; vs = 8 + j if j < 4 else 4
            new.append(ent(E[0], -27 + 9*j, ys[j] + 12, gp + 4*var(vs) if glowf else mt))
        new.append(ent(E[12], -27 + 45 - 1, ys[5] + 12, E[12][2] & 1023))     # '!' sprite (glyph at cols 2-5), JP tiles
        for _ in range(2): new.append(ent(E[0], 0, ys[0], EMPTY_GLOW if glowf else EMPTY_MAIN))
        for i, e in enumerate(new): struct.pack_into('<HHH', nfr, o + 2 + 6*i, *e)
    open(os.path.join(out, 'title_obj.lz'), 'wb').write(lz10.compress(bytes(sh)))
    open(os.path.join(out, 'title_frames.bin'), 'wb').write(bytes(nfr))
    print('title_prompt: glow fit mismatches per variant (of 256 px): %s' % errs)
    if len(sys.argv) > 3:
        from PIL import Image
        P = {0: (40, 100, 160), 1: (255, 255, 255), 2: (40, 40, 40), 3: (120, 120, 200), 5: (200, 200, 255), 6: (150, 150, 220)}
        im = Image.new('RGB', (16*7, 16*5), P[0]); px = im.load()
        for i, ch in enumerate('PRESTA'):
            mt, gp = SLOT[ch]
            for r, t in enumerate([mt] + [gp + 4*k for k in range(4)]):
                g = get16(sh, t)
                for y in range(16):
                    for x in range(16):
                        if g[y][x]: px[i*16+x, r*16+y] = P.get(g[y][x], (255, 0, 255))
        im.resize((im.width*4, im.height*4), Image.NEAREST).save(sys.argv[3])
main()

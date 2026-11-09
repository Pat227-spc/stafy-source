#!/usr/bin/env python3
"""Generate overlay/asm/bin/graphics/MoeHouse/{2MoeHouseBG.bin,3MoeHouseBGTileMap.bin} from upstream's MoeHouse files.
1. Title (BG0, map sbb 28 = 3MoeHouseBGTileMap rows 0-1, cols 4-23 = x 32..191, palette 6): upstream "MOE'S HOUSE" redrawn as
   "MASTER MOE'S HOUSE" (glossary: Master Moe's House, v0.9.7). Same style as upstream's letters: 2 px strokes, 12 px tall
   (rows 2-13), per-row gradient indices taken from upstream's letters (rows 2-3 =15, 4-5 =14 ... 12-13 =10), 2 px black
   (index 2) outline; condensed to 7 px letters (M 10 px, T 6 px, ' 2 px), 2 px letter gaps, 7 px word gaps: strokes x 4..155, outline 2..157 of 160.
   New tiles go to 0x180.. (zero and unreferenced in upstream's sheet; the text box writes 0x221-0x3E7 at run time).
2. Button label 'g' (Minigames, Ending): upstream's g is a cap-height 9-shape with no descender. Every occurrence in the
   button tiles is redrawn as a lowercase g on the x-height (rows 6-9 of the label strip) with a 1 px descender (rows 10-11),
   matching the 4 px letter width of the label font. Pixels are found by pattern match, not by fixed offsets.
3. Button labels (Pat227, 2026-11-02): the text masks in
   tools/gfx/moe_house_labels.txt (rows 2-13 of each 72x16 plate, '#' = ink) replace the text of these strips:
   Ending 1/2/3 and Staff Roll 1/2 normal (blue, SelectionTilemap1 rows 20-29) and selected-normal (pink, SelectionTilemap2
   rows 0-9): V1 fit (1 px letter spacing, 4 px before the number, centred), "Staff Roll" with a space.
   Tall (SelectionTilemap2 rows 10-19): Photos V1 (P/h 1 px shorter, t 2 px), Minigames V2 (11 px M, lowercase g),
   Ending 1-3 (V1 fit, lowercase g, 9-row digits on rows 4-12), Staff Roll 1/2 (space, V1 fit, 9-row digits rows 4-12).
   Only the ink/background indices of each plate interior change. Changed 8x8 cells get new tiles (deduplicated) from
   tiles that are zero and unreferenced in 0x165-0x220; untouched cells keep their tiles. SeaJams/Book/Treasure untouched.
4. Moe's House B-button plate (1MoeHouseOBJ.bin, 32x16 OBJ @0x01, 2D mapping): 'BButton' -> 'PRESS B' (pressb V3), the
   game's 5-row letter style with its 1 px yellow drop shadow (ink 2, shadow 0xA, bg 7), ink cols 3-27 (the left star
   ball covers col 2). The alternating 'Back' frame (@0x05) is untouched."""
import os, sys, struct
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import lz10
HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
SRC = os.path.join(HERE, 'upstream/asm/bin/graphics/MoeHouse'); DST = os.path.join(HERE, 'overlay/asm/bin/graphics/MoeHouse')
dz = lambda f: bytearray(lz10.decompress(open(os.path.join(SRC, f), 'rb').read()))
bg, bmap = dz('2MoeHouseBG.bin'), dz('3MoeHouseBGTileMap.bin')
maps = [bmap, dz('1MoeHouseSelectionTilemap1.bin'), dz('2MoeHouseSelectionTilemap2.bin')]
def gp(t, x, y): b = bg[t*32 + y*4 + x//2]; return (b >> 4) if x & 1 else b & 15
def sp(t, x, y, v):
    i = t*32 + y*4 + x//2; bg[i] = (bg[i] & 0x0F) | (v << 4) if x & 1 else (bg[i] & 0xF0) | v
# ---------- 2. g fix ----------
G9 = [".ccc", "c..c", "c..c", ".ccc", "...c", "c..c", ".cc."]           # upstream glyph, rows 4..10 of a 16-px label strip
GN = ["....", "....", ".ccc", "c..c", "c..c", ".ccc", "...c", "ccc."]   # new glyph, rows 4..11
fixed = set()
for m in maps:
    n = len(m)//2; W = 32
    for ty in range(n//W - 1):
        def px(x, y):                       # pixel of the 2-tile-high strip starting at map row ty (no flips in labels)
            e = struct.unpack_from('<H', m, ((ty + y//8)*W + x//8)*2)[0]
            return (e & 0x3ff, x % 8, y % 8, (e >> 10) & 3)
        for x0 in range(1, W*8 - 5):
            cells = [[px(x0 + i, 4 + j) for i in range(4)] for j in range(8)]
            if any(c[3] for row in cells for c in row): continue
            v = [[gp(*c[:3]) for c in row] for row in cells]
            fg = v[0][1]; bgc = v[0][0]
            if fg == bgc or px(x0 - 1, 4)[3]: continue
            ok = all((v[j][i] == fg) == (G9[j][i] == 'c') and v[j][i] in (fg, bgc) for j in range(7) for i in range(4)) \
                 and all(v[7][i] == bgc for i in range(4)) and all(gp(*px(x0-1, 4+j)[:3]) == bgc for j in range(7))
            if not ok: continue
            key = tuple(cells[0][0][:3])
            if key in fixed: continue
            fixed.add(key)
            for j in range(8):
                for i in range(4): sp(*cells[j][i][:3], fg if GN[j][i] == 'c' else bgc)
            print('g fixed at tiles', sorted({c[0] for row in cells for c in row}), 'fg', fg, 'bg', bgc)
# ---------- 1. title ----------
F = {'M': ["10001", "11011", "10101", "10001", "10001", "10001"], 'A': ["0110", "1001", "1001", "1111", "1001", "1001"],
     'S': ["0111", "1000", "0110", "0001", "0001", "1110"], 'T': ["111", "010", "010", "010", "010", "010"],
     'E': ["1111", "1000", "1110", "1000", "1000", "1111"], 'R': ["1110", "1001", "1001", "1110", "1010", "1001"],
     'O': ["0110", "1001", "1001", "1001", "1001", "0110"], 'H': ["1001", "1001", "1111", "1001", "1001", "1001"],
     'U': ["1001", "1001", "1001", "1001", "1001", "0110"], "'": ["1", "1", "0", "0", "0", "0"]}
TEXT, X0, WCOL, Y0 = "MASTER MOE'S HOUSE", 4, 160, 2      # canvas x 0..159 = map cols 4..23
CW = {5: [2, 2, 2, 2, 2], 4: [2, 1, 2, 2], 3: [2, 2, 2], 1: [2]}  # px per glyph column: 4-col letters are 7 px wide
LGAP, WGAP = 2, 7                                            # letter gap / word gap (px between strokes)
fill = set(); x = X0
for i, ch in enumerate(TEXT):
    if ch == ' ': x += WGAP - LGAP; continue
    g = F[ch]; ws = CW[len(g[0])]; xs = [x + sum(ws[:c]) for c in range(len(ws))]
    for r, row in enumerate(g):
        for c, b in enumerate(row):
            if b == '1':
                for dx in range(ws[c]):
                    for dy in (0, 1): fill.add((xs[c] + dx, Y0 + r*2 + dy))
    x += sum(ws) + LGAP
assert x - 2 + 2 <= WCOL, x
canvas = [[0]*WCOL for _ in range(16)]
for (fx, fy) in fill:
    for dx in range(-2, 3):
        for dy in range(-2, 3):
            if 0 <= fx+dx < WCOL and 0 <= fy+dy < 16: canvas[fy+dy][fx+dx] = 2
GRAD = {2: 15, 3: 15, 4: 14, 5: 14, 6: 13, 7: 13, 8: 12, 9: 12, 10: 11, 11: 11, 12: 10, 13: 10}   # from upstream's letters
for (fx, fy) in fill: canvas[fy][fx] = GRAD[fy]
NEW0 = 0x180; nxt = NEW0; seen = {}
for tr in range(2):
    for tc in range(WCOL//8):
        data = bytearray(32)
        for y in range(8):
            for xx in range(8):
                v = canvas[tr*8+y][tc*8+xx]; data[y*4+xx//2] |= (v << 4) if xx & 1 else v
        data = bytes(data)
        if data == bytes(32): t = 0                              # tile 0 is blank in upstream's sheet
        elif data in seen: t = seen[data]
        else:
            t = seen[data] = nxt; nxt += 1
            assert bg[t*32:t*32+32] == bytes(32) and all(struct.unpack_from('<H', m, i*2)[0] & 0x3ff != t for m in maps for i in range(len(m)//2))
            bg[t*32:t*32+32] = data
        struct.pack_into('<H', bmap, (tr*32 + 4 + tc)*2, 0x6000 | t)
assert bg[0:32] == bytes(32)
print('title: %d new tiles 0x%X-0x%X (budget: 0x165-0x220 free = 188); width %d px' % (nxt-NEW0, NEW0, nxt-1, x-2))

# ---------- 3. button label text ----------
from collections import Counter
m1, m2 = maps[1], maps[2]
LOC = lambda i, st: {'blue': (m1, 20 + (i % 5)*2), 'pink': (m2, (i % 5)*2), 'tall': (m2, 10 + (i % 5)*2)}[st] + (0 if i < 5 else 9,)
NAMES = ['Photos', 'Minigames', 'SeaJams', 'Book', 'Treasure', 'Ending1', 'Ending2', 'Ending3', 'StaffRoll1', 'StaffRoll2']
spec = {}; key = None
for line in open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'moe_house_labels.txt')):
    line = line.rstrip('\n')
    if ' ' in line: key = tuple(line.split()); spec[key] = []
    elif line: spec[key].append(line)
refd = {struct.unpack_from('<H', m, i*2)[0] & 0x3ff for m in maps for i in range(len(m)//2)}
pool = [t for t in range(0x165, 0x221) if t not in refd and bg[t*32:t*32+32] == bytes(32)]
newtiles = {}; used = 0
for (name, st), rows in spec.items():
    m, ty, tx = LOC(NAMES.index(name), st)
    E = [[struct.unpack_from('<H', m, ((ty + r)*32 + tx + c)*2)[0] for c in range(9)] for r in range(2)]
    def cell(e, x, y): return gp(e & 0x3ff, 7 - x if e & 0x400 else x, 7 - y if e & 0x800 else y)
    pix = [[cell(E[y//8][x//8], x % 8, y % 8) for x in range(72)] for y in range(16)]
    bgv = Counter(pix[8]).most_common(1)[0][0]
    ink = Counter(pix[b][a] for a in range(12, 62) for b in range(3, 13) if pix[b][a] != bgv).most_common(1)[0][0]
    if all((pix[2 + j][a] == ink) == (ch == '#') for j, row in enumerate(rows) for a, ch in enumerate(row)):
        continue                                                           # already applied (idempotent)
    for j, row in enumerate(rows):
        for a, ch in enumerate(row):
            y = 2 + j
            if ch == '#': assert pix[y][a] in (bgv, ink), (name, st, a, y); pix[y][a] = ink
            elif pix[y][a] == ink: pix[y][a] = bgv
    for r in range(2):
        for c in range(9):
            e = E[r][c]; data = bytearray(32)
            for y in range(8):
                for x in range(8): data[y*4 + x//2] |= pix[r*8 + y][c*8 + x] << (4 if x & 1 else 0)
            data = bytes(data)
            if all(cell(e, x, y) == pix[r*8 + y][c*8 + x] for y in range(8) for x in range(8)): continue
            if data not in newtiles:
                t = pool[used]; used += 1; newtiles[data] = t; bg[t*32:t*32 + 32] = data
            struct.pack_into('<H', m, ((ty + r)*32 + tx + c)*2, (e & 0xF000) | newtiles[data])   # new tiles are stored unflipped
    print('label %s %s: text replaced' % (name, st))
print('labels: %d new tiles (%d free in 0x165-0x220)' % (used, len(pool)))
# ---------- 4. PRESS B on the B-button plate (OBJ) ----------
obj = dz('1MoeHouseOBJ.bin')
def op(t, x, y): i = (t + (y//8)*32 + x//8)*32 + (y % 8)*4 + (x % 8)//2; return i, x & 1
GL = {'P': ["##.", "#.#", "##.", "#..", "#.."], 'R': ["##.", "#.#", "##.", "#.#", "#.#"], 'E': ["###", "#..", "##.", "#..", "###"],
      'S': [".##", "#..", ".#.", "..#", "##."], 'B': ["###.", "#.##", "###.", "#.##", "###."]}
ink_px = set(); x = 3                                   # 25 px: P R E S S (1 px gaps) + 2 px space + B, cols 3-27
for k, ch in enumerate("PRESS B"):
    if ch == ' ': x += 1; continue
    for j, row in enumerate(GL[ch]):
        for i, c in enumerate(row):
            if c == '#': ink_px.add((x + i, 6 + j))
    x += len(GL[ch][0]) + 1
assert max(a for a, _ in ink_px) == 27, max(a for a, _ in ink_px)
for xx in range(2, 30):
    for yy in range(6, 12):
        v = 2 if (xx, yy) in ink_px else 0xA if (xx - 1, yy - 1) in ink_px else 7
        i, hi = op(0x01, xx, yy); obj[i] = (obj[i] & 0x0F) | (v << 4) if hi else (obj[i] & 0xF0) | v
os.makedirs(DST, exist_ok=True)
open(os.path.join(DST, '2MoeHouseBG.bin'), 'wb').write(lz10.compress(bytes(bg)))
open(os.path.join(DST, '3MoeHouseBGTileMap.bin'), 'wb').write(lz10.compress(bytes(bmap)))
open(os.path.join(DST, '1MoeHouseSelectionTilemap1.bin'), 'wb').write(lz10.compress(bytes(m1)))
open(os.path.join(DST, '2MoeHouseSelectionTilemap2.bin'), 'wb').write(lz10.compress(bytes(m2)))
open(os.path.join(DST, '1MoeHouseOBJ.bin'), 'wb').write(lz10.compress(bytes(obj)))

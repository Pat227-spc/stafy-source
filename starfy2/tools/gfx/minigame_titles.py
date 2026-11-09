#!/usr/bin/env python3
"""Minigame menu titles: remove the Japanese corner brackets 「 」 (Pat227, 2026-11-02) and re-center each title; fix
'TightropeTremble' -> 'Tightrope Tremble' (4 px word gap) with a lowercase g (bowl on the x-height, tail 1 px below the
baseline: the title sprites are only 16 px tall). Edits overlay/asm/bin/graphics/minigamemenu/1minigamemenuOBJ.bin IN PLACE,
after tools/gfx/bomb_shower.py and dont_drop_em.py (same chain). Refuses to run twice.
Layout (OAM read from the running game, OBJ 2D mapping, 32 tiles/row; title band x 112..223, y 5..20):
  game 0 Bomb Shower: 0xC0 at x112 (32,32,32,16 wide)      game 1 Color Matcher: 0x40 at x112
  game 2 Squeak Squeak Panic (was Chu-Chu Panic): 0xCD hflip (8x16) at x112, repointed to 0x10E by
  overlay/patches/47_minigame_title_tiles.asm (stage 2), + 0x100 at x120 (32,32,32,8)
  game 3 Don't Drop 'Em: 0x40 (8x16) at x112 + 0x80 at x120   game 4 Tightrope Tremble: 0x8C hflip at x112 + 0x140 at x120
The 8x16 bracket pieces are borrowed from other titles' tiles (0x40/0xCD/0x8C); with the brackets gone they are blank, and
no title may draw into them. Colours: 1 = white letter, 2 = dark plate/outline, 0 = transparent."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import lz10
HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
DST = os.path.join(HERE, 'overlay/asm/bin/graphics/minigamemenu/1minigamemenuOBJ.bin')
raw = bytearray(lz10.decompress(open(DST, 'rb').read()))
def gp(t, x, y): b = raw[t*32 + y*4 + x//2]; return (b >> 4) if x & 1 else b & 15
def sp(t, x, y, v):
    i = t*32 + y*4 + x//2; raw[i] = (raw[i] & 0x0F) | (v << 4) if x & 1 else (raw[i] & 0xF0) | v
L = {0: [(0, 0xC0, 112, 0)], 1: [(0, 0x40, 112, 0)], 2: [(0, 0xCD, 8, 1), (8, 0x100, 104, 0)],
     3: [(0, 0x40, 8, 0), (8, 0x80, 104, 0)], 4: [(0, 0x8C, 8, 1), (8, 0x140, 104, 0)]}
NAMES = ['Bomb Shower', 'Color Matcher', 'Squeak Squeak Panic', "Don't Drop 'Em", 'Tightrope Tremble']
def where(g, X, y):
    for x0, t, w, hf in L[g]:
        if x0 <= X < x0 + w:
            sx = w - 1 - (X - x0) if hf else X - x0
            return (t + (y//8)*32 + sx//8, sx % 8, y % 8)
def read(g): return [[gp(*where(g, X, y)) for X in range(112)] for y in range(16)]
STAGE1 = gp(*where(0, 2, 2)) == 1 and gp(*where(0, 2, 8)) == 2   # brackets still present -> stage 1 not yet applied
out = {}
for g in (range(5) if STAGE1 else ()):
    W = read(g)
    # text = columns 8..103 (the 「 is the first 8 px, the 」 the last 8 px of every title band)
    cols = [X for X in range(8, 104) if any(W[y][X] == 1 for y in range(16))]
    a, b = cols[0] - 2, cols[-1] + 2                         # include the 2 px outline
    blk = [row[a:b+1] for row in W]
    if g == 4:
        # space between 'Tightrope' and 'Tremble': first plate-only column gap after x-offset 50 of the block
        tb = next(X for X in range(40, len(blk[0])) if blk[2][X] == 1)   # top bar of the 2nd T (it overhangs the 'e')
        blk = [(row[:tb-2] + [0]*4 + row[tb-2:]) if y < 5 else (row[:tb] + [2]*4 + row[tb:]) for y, row in enumerate(blk)]  # 4 px word gap
        # find the g: 3rd letter run of the block
        runs, inrun = [], False
        for X in range(len(blk[0])):
            on = any(blk[y][X] == 1 for y in range(16))
            if on and not inrun: runs.append([X, X]); inrun = True
            elif on: runs[-1][1] = X
            elif inrun: inrun = False
        gx0, gx1 = runs[2]
        for y in range(2, 16):
            for X in range(gx0, gx1 + 1): blk[y][X] = 2
        G = [".1111", "11.11", "11.11", ".1111", "...11", "...11", "...11", "1111."]  # rows 7..14
        for j, row in enumerate(G):
            for i, c in enumerate(row):
                if c == '1': blk[7 + j][gx0 + i] = 1
        for y in range(15, 16): blk[y][gx0:gx0+5] = [2]*5
    w = len(blk[0])
    lo = 8 if g != 0 else 0; hi = 104 if g in (0, 3) else 112
    x0 = max(lo, min(hi - w, 56 - w//2))
    new = [[0]*112 for _ in range(16)]
    for y in range(16):
        for X in range(w): new[y][x0 + X] = blk[y][X]
    out[g] = new
    print('%-18s text %3d px, placed x %d..%d (centre %.1f of 56)' % (NAMES[g], w, 112 + x0, 112 + x0 + w - 1, x0 + w/2))
for g in out:
    for X in range(112):
        for y in range(16): sp(*where(g, X, y), out[g][y][X])
if not STAGE1: print('stage 1 (bracket removal) already applied, skipped')

# ---- Stage 2 (Pat227, 2026-11-02): game 2 'Chu-Chu Panic' -> 'Squeak Squeak Panic' (チューチューパニック, the minigame's mice
# squeak), and the matching 'Tightrope Tremble' redraw. Both lines: capitals/ascenders shortened 2 px (10 px tall, rows 2-11), the
# line lifted 2 px (x-height rows 5-11, baseline row 11), so q, g and p drop 3 px below the baseline (rows 12-14); the outline
# under a descender is 1 px (row 15, the bottom of the 16 px sprite). Squeak Squeak Panic uses lowercase narrowed to 5 px
# (like Tightrope Tremble's). The title is 111 px with outline, so
# game 2's left 8x16 piece can no longer borrow Bomb Shower's blank tile 0xCD: it is repointed to the free tiles 0x10E/0x12E
# (blank, not used by any minigame-menu OAM; checked in mGBA) by overlay/patches/47_minigame_title_tiles.asm.
# Masks are literal (white = '#'); the 2 px outline is regenerated (square dilation, clipped to the 16 px sprite), as
# bomb_shower.py does. Idempotent: it redraws both titles from these masks every run.
SQUEAK = [
    '...........................................................................................................',
    '...........................................................................................................',
    '..#####.........................##........#####.........................##......#####..............##......',
    '###.............................##......###.............................##......##..##.............##......',
    '###.............................##......###.............................##......##..##.....................',
    '.#####...####.##.##..###...####.##.##....#####...####.##.##..###...####.##.##...######..####.####..##..####',
    '.#####..#####.##.##.#####.#####.####.....#####..#####.##.##.#####.#####.####....#####..#####.#####.##.#####',
    '....###.##.##.##.##.##.##.##.##.###.........###.##.##.##.##.##.##.##.##.###.....##.....##.##.##.##.##.##...',
    '.....##.##.##.##.##.#####.##.##.###..........##.##.##.##.##.#####.##.##.###.....##.....##.##.##.##.##.##...',
    '....###.##.##.##.##.##....##.##.####........###.##.##.##.##.##....##.##.####....##.....##.##.##.##.##.##...',
    '######..#####.#####.#####.#####.##.##...######..#####.#####.#####.#####.##.##...##.....#####.##.##.##.#####',
    '#####....####..####..####..####.##.##...#####....####..####..####..####.##.##...##......####.##.##.##..####',
    '...........##......................................##......................................................',
    '...........##......................................##......................................................',
    '...........##......................................##......................................................',
    '...........................................................................................................',
]
TIGHTROPE = [
    '................................................................................................',
    '................................................................................................',
    '######.##.......##......##..............................######....................##...###......',
    '..##...##.......##......##................................##......................##....##......',
    '..##............##....######..............................##......................##....##......',
    '..##...##..####.####..######.##.##..###..####...###.......##.##.##..###..#######..####..##..###.',
    '..##...##.#####.#####...##...#####.#####.#####.#####......##.#####.#####.########.#####.##.#####',
    '..##...##.##.##.##.##...##...###...##.##.##.##.##.##......##.###...##.##.##.##.##.##.##.##.##.##',
    '..##...##.##.##.##.##...##...##....##.##.##.##.#####......##.##....#####.##.##.##.##.##.##.#####',
    '..##...##.##.##.##.##...##...##....##.##.##.##.##.........##.##....##....##.##.##.##.##.##.##...',
    '..##...##.#####.##.##...##...##....#####.#####.#####......##.##....#####.##.##.##.#####.##.#####',
    '..##...##..####.##.##...##...##.....###..####...####......##.##.....####.##.##.##.####..##..####',
    '.............##..........................##.....................................................',
    '.............##..........................##.....................................................',
    '..........####...........................##.....................................................',
    '................................................................................................',
]
L[2] = [(0, 0x10E, 8, 0), (8, 0x100, 104, 0)]
def plate(M):
    h, w = 16, len(M[0]) + 4; P = [[0]*w for _ in range(h)]
    for y in range(h):
        for X in range(w):
            if any(0 <= X-2+dx < w-4 and 0 <= y+dy < h and M[y+dy][X-2+dx] == '#' for dx in range(-2, 3) for dy in range(-2, 3)):
                P[y][X] = 1 if 0 <= X-2 < w-4 and M[y][X-2] == '#' else 2
    return P
for g, M, lo in ((2, SQUEAK, 0), (4, TIGHTROPE, 8)):
    P = plate(M); w = len(P[0]); assert w <= 112 - lo, (NAMES[g], w)
    x0 = max(lo, min(112 - w, 56 - w//2))
    for X in range(112):
        for y in range(16):
            v = P[y][X - x0] if x0 <= X < x0 + w else 0
            sp(*where(g, X, y), v)
    print('%-18s stage 2: %3d px with outline, placed x %d..%d' % (NAMES[g], w, 112 + x0, 112 + x0 + w - 1))
# game 2's old borrowed piece (0xCD/0xED, hflip) belongs to Bomb Shower's x 104..111: keep it blank
for y in range(16):
    for x in range(8): sp(0xCD + (y//8)*32, x, y % 8, 0)
open(DST, 'wb').write(lz10.compress(bytes(raw)))

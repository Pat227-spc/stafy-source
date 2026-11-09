#!/usr/bin/env python3
"""'BButton' -> 'B Button' on the minigame menu B-button tab (Pat227, 2026-11-02).
Only the game's own letter pixels are moved; nothing is redrawn. Idempotent: the label is re-laid out from its letter runs
every time (the first gap is forced, the rest are kept), so a second run changes nothing.
1. Minigame menu tab (overlay/asm/bin/graphics/minigamemenu/1minigamemenuOBJ.bin, edited IN PLACE after minigame_titles.py):
   sprites 32x16 @0x0A + 16x16 @0x0E + 8x16 @0x10 (OBJ 2D, 56 px). Text strip rows 6-10, inside cols 5-50 (46 px, colour 9).
   'B' + 4 blank columns + 'Button', centred: 33 px at cols 11-43. The alternate 'Back' frame and the flip frames use other
   tiles (0x11-0x1C) and are not touched.
2. Master Moe's House plate (upstream/asm/bin/graphics/MoeHouse/1MoeHouseOBJ.bin, 32x16 @0x01): NOT changed. The rolling star
   balls (16x16 @0x09) overlap the plate ends; in mGBA the left ball's outline covers plate col 2, so only cols 3-29 (27 px)
   show. 'BButton' already needs 2-29 (its wide first B loses its stem column under the ball). 'B Button' needs at least
   3 (narrow B) + 2 + 23 = 28 px; tried 2026-11-02: the lone B's stem was hidden and it read as '3'. Needs the balls moved
   outward (their animation/OAM data) first."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import lz10
HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
def sheet(raw):
    def gp(t, x, y):
        b = raw[(t + (y//8)*32 + x//8)*32 + (y % 8)*4 + (x % 8)//2]; return (b >> 4) if x & 1 else b & 15
    def sp(t, x, y, v):
        i = (t + (y//8)*32 + x//8)*32 + (y % 8)*4 + (x % 8)//2; raw[i] = (raw[i] & 0x0F) | (v << 4) if x & 1 else (raw[i] & 0xF0) | v
    return gp, sp
def relayout(raw, t, rows, lo, hi, bg, first_gap, first_glyph=0, centre=True):
    gp, sp = sheet(raw)
    cols = [[gp(t, x, y) for y in rows] for x in range(lo, hi + 1)]
    ink = [i for i, c in enumerate(cols) if any(v != bg for v in c)]
    runs = []
    for i in ink:
        if runs and i == runs[-1][1] + 1: runs[-1][1] = i
        else: runs.append([i, i])
    assert len(runs) == 7, runs   # B B u t t o n
    gl = [cols[a:b+1] for a, b in runs]
    gaps = [runs[k][0] - runs[k-1][1] - 1 for k in range(1, len(runs))]
    out = list(gl[first_glyph]) + [[bg]*len(rows)]*first_gap
    for k in range(1, len(gl)):
        if k > 1: out += [[bg]*len(rows)]*gaps[k-1]
        out += gl[k]
    w = len(out); assert w <= hi - lo + 1, (w, hi - lo + 1)
    x0 = lo + ((hi - lo + 1) - w)//2 if centre else lo
    for x in range(lo, hi + 1):
        for j, y in enumerate(rows): sp(t, x, y, bg)
    for i, c in enumerate(out):
        for j, y in enumerate(rows): sp(t, x0 + i, y, c[j])
    return w, x0
# Idempotency: the minigame file is edited in place, so detect a previous run by the 4-column gap after the first letter.
def already(raw, t, rows, lo, hi, bg, gap):
    gp, _ = sheet(raw)
    ink = [x for x in range(lo, hi + 1) if any(gp(t, x, y) != bg for y in rows)]
    runs = []
    for i in ink:
        if runs and i == runs[-1][1] + 1: runs[-1][1] = i
        else: runs.append([i, i])
    return len(runs) == 7 and runs[1][0] - runs[0][1] - 1 == gap
MG = os.path.join(HERE, 'overlay/asm/bin/graphics/minigamemenu/1minigamemenuOBJ.bin')
raw = bytearray(lz10.decompress(open(MG, 'rb').read()))
if already(raw, 0x0A, range(6, 11), 5, 50, 9, 4): print('minigame tab: already B Button, unchanged')
else:
    w, x0 = relayout(raw, 0x0A, range(6, 11), 5, 50, 9, 4)
    open(MG, 'wb').write(lz10.compress(bytes(raw))); print('minigame tab: B Button %d px at cols %d-%d of 56 (inside 5-50)' % (w, x0, x0 + w - 1))

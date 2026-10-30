#!/usr/bin/env python3
"""shop_sign.py BASE_ROM OUT.lz  - 1-3 Lovely's Shop building banner 'ラブリーのおみせ' -> "LOVELY'S / SHOP".
The shop building is an OBJ sheet: LZ block 0x087DD44C (8-byte header 01 00 00 00 a4 00 00 00 + 164 4bpp tiles, loaded
at OBJ tile 352 in 1-3 room 10; only pointer 0x082A7DE4). The banner uses OBJ palette 6 (1 white, 2 outline,
c/d/e pink text shades). shop_sign_edits.json holds our pixel edits as [vram_tile, byte_in_tile, high_nibble, index]:
the JP text pixels are cleared to white and the new letters drawn in the banner's own pink (e = body, d = drop shade),
a 4x5 caps line "LOVELY'S" over a bold 6x7 "SHOP" (caps in the style of upstream's Lovely's Shop logo).
Mapping screen->tile was taken from the in-game OAM (scratch/gfx3/design.py)."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import lz10
rom = open(sys.argv[1], 'rb').read(); SRC = 0x087DD44C; T0 = 352
d = bytearray(lz10.decompress(rom, SRC & 0x1FFFFFF))
assert d[:8] == bytes([1, 0, 0, 0, 0xA4, 0, 0, 0]) and len(d) == 8 + 164 * 32, 'unexpected shop OBJ block'
ed = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'shop_sign_edits.json')))
for t, bo, nib, val in ed:
    o = 8 + (t - T0) * 32 + bo
    d[o] = (d[o] & 0x0F) | (val << 4) if nib else (d[o] & 0xF0) | val
c = lz10.compress(bytes(d)); open(sys.argv[2], 'wb').write(c)
print('shop_sign: %d pixel edits, %d bytes' % (len(ed), len(c)))

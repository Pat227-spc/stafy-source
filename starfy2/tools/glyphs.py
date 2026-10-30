#!/usr/bin/env python3
"""Apply glyph overrides to VWF font .bin files in the scratch tree (upstream files are untouched).
usage: glyphs.py TREE OVERLAY_GLYPH_DIR
  OVERLAY_GLYPH_DIR/<FontName>/<index>.txt -> patches TREE/asm/VWF/<FontName>.bin glyph <index>
Format: 16x13, 2bpp, 52 bytes/glyph, row-major, 4 bytes per row, pixel x in bits (x%4)*2 (LSB first).
Text rows use '.', '1', '2', '3' per pixel; lines starting with '#' are comments.
Also: glyphs.py --show FONT.bin FIRST LAST  prints glyphs as text."""
import sys, os
def enc(rows):
    out = bytearray(52)
    for y, r in enumerate(rows):
        for x, ch in enumerate(r[:16].ljust(16, '.')):
            v = '.123'.index(ch); out[y*4 + x//4] |= v << ((x % 4) * 2)
    return bytes(out)
if sys.argv[1] == '--show':
    d = open(sys.argv[2], 'rb').read()
    for g in range(int(sys.argv[3]), int(sys.argv[4]) + 1):
        print('#', g)
        for y in range(13): print(''.join('.123'[(d[g*52 + y*4 + x//4] >> ((x % 4) * 2)) & 3] for x in range(16)))
    sys.exit()
tree, gdir = sys.argv[1], sys.argv[2]; n = 0
if os.path.isdir(gdir):
    for font in sorted(os.listdir(gdir)):
        fp = os.path.join(tree, 'asm', 'VWF', font + '.bin')
        if not os.path.exists(fp): print('glyphs: no font', fp); sys.exit(1)
        d = bytearray(open(fp, 'rb').read())
        for f in sorted(os.listdir(os.path.join(gdir, font))):
            if not f.endswith('.txt'): continue
            g = int(f[:-4]); rows = [l.rstrip('\n') for l in open(os.path.join(gdir, font, f)) if not l.startswith('#') and l.strip()]
            assert len(rows) == 13, f'{f}: need 13 rows'
            d[g*52:(g+1)*52] = enc(rows); n += 1
        open(fp, 'wb').write(d)
print('glyphs: %d override(s) applied' % n)

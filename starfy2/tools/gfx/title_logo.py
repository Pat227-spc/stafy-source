#!/usr/bin/env python3
"""title_logo.py BASE.gba OUTDIR [PREVIEW.png]  - English title logo "The Legendary Starfy 2".
Title BG1 (8bpp, char base 0, map sbb 29) is loaded by 0x080DC7A6 from archive 0x088F6B3C + offset literals:
  block 0  (+0       -> 0x06000000, tiles 0-511; JP logo = tiles 0xA2-0x143, 162 tiles, map rows 1-9 cols 4-25)
  block 1  (+0x37CC  -> 0x06008000, tiles 512-639; literal 0x080DC91C)
  BG1 map  (+0x5FDA4 -> 0x0600E800; literal 0x080DC92C)
Block 0 recompresses to exactly its original size, so instead of rewriting it in place the new logo tiles are appended to
block 1 (tiles 640+, VRAM 0x0600A000+, unused on the title) and the map is rewritten to point at them; both are
repointed into the patch area by overlay/patches/60_title_logo.asm (offset literals). The palette is unchanged.
Logo = tools/gfx/title_logo_text.png (our text layer, JP palette indices) + the JP '2' and (R) taken from the base ROM.
Tile budget: at most the JP logo's 162 tiles (asserted). Outputs (ROM-derived, never committed): OUTDIR/title_logo_tiles.lz,
OUTDIR/title_logo_map.lz."""
import sys, os, struct
import numpy as np
from PIL import Image
from scipy import ndimage as nd
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); import lz10
ARC = 0x088F6B3C; B0, B1, MAP = 0, 0x37CC, 0x5FDA4; JP_TILES = 162
CX, CY, CWT, CHT = 3, 0, 25, 11            # canvas = map cols 3..27, rows 0..10 (200 x 88 px)
def lz(r, off):
    d = lz10.decompress(r, ARC - 0x08000000 + off); return bytearray(d[0] if isinstance(d, tuple) else d)
def compose(r):
    """-> (out canvas of palette indices 200x88, map bytes, block0, block1); shared with staff_logo.py"""
    lit = lambda a: struct.unpack_from('<I', r, a - 0x08000000)[0]
    assert (lit(0x080DC910), lit(0x080DC91C), lit(0x080DC92C)) == (ARC, B1, MAP), "unexpected title loader literals"
    b0, b1, m = lz(r, B0), lz(r, B1), lz(r, MAP)
    assert len(b1) == 0x2000 and len(m) == 0x500          # map: 20 rows of 32
    ent = lambda mx, my: struct.unpack_from('<H', m, (my * 32 + mx) * 2)[0]
    jp = np.zeros((CHT * 8, CWT * 8), int); old = set()
    for my in range(CY, CY + CHT):
        for mx in range(CX, CX + CWT):
            e = ent(mx, my)
            if e == 0: continue
            assert e >> 10 == 0 and 0xA2 <= e <= 0x143, hex(e); old.add(e)
            t = np.frombuffer(bytes(b0[e * 64:e * 64 + 64]), np.uint8).reshape(8, 8)
            jp[(my - CY) * 8:(my - CY) * 8 + 8, (mx - CX) * 8:(mx - CX) * 8 + 8] = t
    assert len(old) == JP_TILES, len(old)
    text = np.asarray(Image.open(os.path.join(HERE, 'title_logo_text.png')), int)
    assert text.shape == jp.shape
    pink = (jp >= 1) & (jp <= 19)                                  # the '2' (pink) + its outline
    keep = nd.binary_dilation(pink, iterations=5) & (jp > 0); keep[:, :124] = False
    yy, xx = np.mgrid[0:jp.shape[0], 0:jp.shape[1]]
    keep |= ((yy - 68.5) ** 2 + (xx - 138.5) ** 2 <= 7.5 ** 2) & (jp > 0) & ~((jp >= 79) & (jp <= 124))   # (R) mark
    out = text.copy(); out[keep] = jp[keep]
    return out, m, b0, b1
def bg_palette(r):
    pal = lz10.decompress(r, 0x08956518 - 0x08000000); pal = pal[0] if isinstance(pal, tuple) else pal
    P = [struct.unpack_from('<H', pal, 2 * i)[0] for i in range(256)]
    return [((c & 31) << 3, (c >> 5 & 31) << 3, (c >> 10 & 31) << 3) for c in P]
def main(base, outdir, preview=None):
    r = open(base, 'rb').read()
    out, m, b0, b1 = compose(r)
    # Block 1 also holds the file-select quick-save message tiles (BG, 0x06008000). If the build tree has Luckylodeon98's
    # English version (overlay/asm/bin/graphics/titlescreen/2filemessagebg.bin, LZ77, same 0x2000 bytes), start from it
    # instead of the base ROM's Japanese block so the message stays English; the logo tiles are appended after it as before.
    ovl = os.path.join(outdir, '..', '..', 'asm', 'bin', 'graphics', 'titlescreen', '2filemessagebg.bin')
    if os.path.exists(ovl):
        d = lz10.decompress(open(ovl, 'rb').read(), 0); b1 = bytearray(d[0] if isinstance(d, tuple) else d)
        assert len(b1) == 0x2000, "2filemessagebg.bin: %d bytes, want 0x2000" % len(b1)
        print("title_logo: block1 from %s" % os.path.normpath(ovl))
    tiles, idx = [], {}
    nm = bytearray(m)
    for my in range(CY, CY + CHT):
        for mx in range(CX, CX + CWT):
            t = out[(my - CY) * 8:(my - CY) * 8 + 8, (mx - CX) * 8:(mx - CX) * 8 + 8].astype(np.uint8).tobytes()
            if not any(t): e = 0
            else:
                if t not in idx: idx[t] = 640 + len(tiles); tiles.append(t)
                e = idx[t]
            struct.pack_into('<H', nm, (my * 32 + mx) * 2, e)
    assert len(tiles) <= JP_TILES, "English logo needs %d tiles > JP %d" % (len(tiles), JP_TILES)
    assert 0x8000 + 0x2000 + 64 * len(tiles) <= 0xD800, "tiles would reach the BG0 map (sbb 27)"
    nb1 = bytes(b1) + b''.join(tiles)
    os.makedirs(outdir, exist_ok=True)
    open(os.path.join(outdir, 'title_logo_tiles.lz'), 'wb').write(lz10.compress(nb1))
    open(os.path.join(outdir, 'title_logo_map.lz'), 'wb').write(lz10.compress(bytes(nm)))
    print("title_logo: %d tiles (JP %d), block1 %d B -> %s" % (len(tiles), JP_TILES, len(nb1), outdir))
    if preview:
        P = bg_palette(r)
        im = Image.new('RGB', (out.shape[1], out.shape[0]), (255, 0, 255))
        for y in range(out.shape[0]):
            for x in range(out.shape[1]):
                if out[y, x]: im.putpixel((x, y), P[out[y, x]])
        im.resize((im.width * 3, im.height * 3), Image.NEAREST).save(preview)
if __name__ == '__main__': main(*sys.argv[1:4])

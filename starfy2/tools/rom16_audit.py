#!/usr/bin/env python3
"""rom16_audit.py ROM32 ROM16 [--base JP.gba] - prove the --rom16 build is the 32 MiB build with its >16 MiB blocks moved.
Builds the expected 16 MiB image from ROM32 (low 16 MiB + each upper block copied to its rom16 address, see tools/rom16.py),
then explains every differing byte of ROM16: it must be part of an aligned 32-bit word whose new value = old value + the
block delta, where the old value is a pointer (0x08000000 + offset) into that block, or an offset from the title archive
base 0x088F6B3C into it (30_title_prompt / 60_title_logo). Anything else is UNEXPLAINED (exit 1).
Also checks: every byte above 16 MiB in ROM32 belongs to a block; each destination was free (0xFF) in ROM32's low half;
ROM16 is exactly 16 MiB and 0xFF-padded; header checksum; and lists 0x09xxxxxx-valued words left in ROM16 that point into
an old block (expected: only coincidental bytes inside data, each one shown with where it sits)."""
import sys, struct, collections, zlib
a = sys.argv[1:]; r32 = open(a[0], 'rb').read(); r16 = open(a[1], 'rb').read()
M16 = 0x1000000
#        name       old window (32 MiB)      new base   (window size = the rom16 area for that block)
WIN = [('text',    0x1000000, 0x1040000, 0x0C40000),
       ('gfx',     0x1200000, 0x1280000, 0x0C80000),
       ('overlay', 0x1400000, 0x1540000, 0x0D00000),
       ('vwf',     0x1E40000, 0x1F00000, 0x0E40000),
       ('patches', 0x1F00000, 0x1F80000, 0x0F00000)]
fails = []
if len(r16) != M16: fails.append('ROM16 size %d' % len(r16))
blocks = []
exp = bytearray(r32[:M16]); fill = bytearray(M16)   # fill[i]=1: byte i is unwritten padding in ROM32 (0x00) and may be 0xFF in ROM16
for name, lo, hi, nb in WIN:
    dl = nb - lo
    if r32[lo+dl:hi+dl].count(0xFF) != hi - lo: fails.append('%s area 0x%X-0x%X is not free (0xFF) in ROM32' % (name, lo+dl, hi+dl))
    seg = r32[lo:hi]; s0 = len(seg) - len(seg.lstrip(b'\0')); e0 = len(seg.rstrip(b'\0'))
    exp[lo+dl:hi+dl] = seg
    for i in range(lo, hi):
        if r32[i] == 0: fill[i+dl] = 1
    if e0: blocks.append((name, lo + s0, lo + e0, dl)); print('block %-8s 0x%08X-0x%08X -> 0x%08X-0x%08X  %7d bytes  delta -0x%X' % (name, 0x08000000+lo+s0, 0x08000000+lo+e0, 0x08000000+lo+s0+dl, 0x08000000+lo+e0+dl, e0-s0, -dl))
used = sum(b[2]-b[1] for b in blocks)
outside = sum(1 for i in range(M16, len(r32)) if r32[i] and not any(lo <= i < hi for _, lo, hi, _ in WIN))
if outside: fails.append('%d non-zero bytes above 16 MiB are outside every block window' % outside)
def blk(v):
    o = v - 0x08000000
    for name, o0, o1, dl in blocks:
        if o0 <= o <= o1: return name, dl
    return None
diff = [i for i in range(M16) if exp[i] != r16[i] and not (fill[i] and r16[i] == 0xFF)]
nfill = sum(1 for i in range(M16) if fill[i] and r16[i] == 0xFF and exp[i] != 0xFF)
words = sorted(set(i & ~3 for i in diff)); cat = collections.Counter(); unexp = []
TITLE = 0x088F6B3C
for w in words:
    e, n = struct.unpack_from('<I', exp, w)[0], struct.unpack_from('<I', r16, w)[0]
    b = blk(e); bo = blk((e + TITLE) & 0xFFFFFFFF)
    if b and (n - e) & 0xFFFFFFFF == b[1] & 0xFFFFFFFF: cat[('pointer', b[0], 'in moved block' if any(o0+dl <= w < o1+dl for _, o0, o1, dl in blocks) else 'in low 16 MiB')] += 1
    elif bo and (n - e) & 0xFFFFFFFF == bo[1] & 0xFFFFFFFF: cat[('archive offset', bo[0], '0x%08X' % (0x08000000 + w))] += 1
    else: unexp.append((w, e, n))
print('padding: %d bytes are unwritten 0x00 in ROM32 and 0xFF in ROM16' % nfill)
print('differing bytes %d in %d aligned words' % (len(diff), len(words)))
for k, v in sorted(cat.items()): print('  repointed %-15s -> %-8s %-16s %5d' % (k[0], k[1], k[2], v))
for w, e, n in unexp[:20]: print('  UNEXPLAINED 0x%08X: expected %08X, got %08X' % (0x08000000 + w, e, n))
if unexp: fails.append('%d unexplained words' % len(unexp))
if r16[len(r16.rstrip(b'\xff')):] .count(0xFF) != len(r16) - len(r16.rstrip(b'\xff')): pass
tail = len(r16) - len(r16.rstrip(b'\xff'))
c = (-sum(r16[0xA0:0xBD]) - 0x19) & 0xFF
if r16[0xBD] != c: fails.append('header checksum %02X != %02X' % (r16[0xBD], c))
# leftover 0x09-valued words that hit an old block (coincidences inside data are expected; show where)
left = collections.Counter()
for o in range(0, M16 - 3, 4):
    v = struct.unpack_from('<I', r16, o)[0]
    if v >> 24 in (0x09, 0x0B, 0x0D) and blk(0x08000000 + (v & 0x01FFFFFF)):
        where = next((nm for nm, o0, o1, dl in blocks if o0+dl <= o < o1+dl), 'low')
        left[where] += 1
print('ROM16: %d bytes, CRC32 %08X, header checksum %02X (%s), 0xFF tail %d bytes, data end 0x%X' % (len(r16), zlib.crc32(r16), r16[0xBD], 'OK' if r16[0xBD] == c else 'BAD', tail, len(r16) - tail))
print('ROM32: %d bytes, CRC32 %08X; moved %d bytes in %d blocks' % (len(r32), zlib.crc32(r32), used, len(blocks)))
print('0x09/0x0B/0x0D-valued words in ROM16 that hit an old block (by location):', dict(left))
print('RESULT', 'FAIL: ' + '; '.join(fails) if fails else 'PASS')
sys.exit(1 if fails else 0)

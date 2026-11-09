#!/usr/bin/env python3
"""rom16.py - 16 MiB ("Supercard") build variant for build.sh --rom16. Same content as the 32 MiB build, but every
block the 32 MiB layout puts above 16 MiB is assembled into free 0xFF space of the original 16 MiB image instead:

  block                       32 MiB build             16 MiB build (--rom16)     set by
  uncompressed text (Atlas)   0x09000000-              0x08C40000- (< 0x08C80000)  FIRST.txt #JMP, rewritten here
  graphics (graphics.asm)     0x09200000 (area 2 MiB)  0x08C80000 (area 512 KiB)   build.sh GFX_BASE/GFX_AREA
  overlay scenes              0x09400000-0x09E40000    0x08D00000-0x08E40000       build.sh OVL_BASE/OVL_END
  VWF minifont (VWF.asm)      0x09E5D98C, 0x09E6418C   0x08E5D98C, 0x08E6418C      rewritten here
  overlay/patches area        0x09F00000-0x09F2xxxx    0x08F00000-0x08F2xxxx       rewritten here (.org 0x09Fxxxxx)

Nothing is moved after assembly: labels, Atlas pointers and armips expressions are resolved by the tools themselves.
usage: rom16.py prep TREE                 rewrite scratch copies; fail if any other .org 0x09xxxxxx / #JMP($01xxxxxx) is left
       rom16.py snap ROM SNAPFILE         save the text area after Atlas (to prove nothing later overwrote it)
       rom16.py final BASE ROM SNAPFILE   size == 16 MiB, text area intact, header checksum (pointer proof: rom16_audit.py)"""
import sys, os, re, struct, glob
TEXT_LO, TEXT_HI = 0x00C40000, 0x00C80000
def prep(tree):
    n = 0
    def sub(path, pat, rep, want):
        nonlocal n
        s = open(path, 'rb').read().decode('latin-1'); s2, k = re.subn(pat, rep, s)
        if k != want: sys.exit('rom16: %s: expected %d match(es) of %s, found %d' % (path, want, pat, k))
        open(path, 'wb').write(s2.encode('latin-1')); n += k
    sub(os.path.join(tree, 'asm/bin/text/Uncompressed/Blocks/FIRST/FIRST.txt'), r'#JMP\(\$01000000\)', '#JMP($%08X)' % TEXT_LO, 1)
    sub(os.path.join(tree, 'asm/VWF/VWF.asm'), r'(?im)^\.org 0x09E(5D98C|6418C)\b', r'.org 0x08E\1', 2)
    for p in sorted(glob.glob(os.path.join(tree, 'patches/*.asm'))):
        s = open(p, 'rb').read().decode('latin-1')
        k = len(re.findall(r'(?im)^\s*\.org\s+0x09F[0-9a-f]{5}\b', s))
        if k: sub(p, r'(?im)^(\s*\.org\s+)0x09F([0-9a-f]{5})\b', r'\g<1>0x08F\2', k)
    # anything else that still targets the >16 MiB space is a layout we don't know how to move: stop the build
    left = []
    for p in glob.glob(os.path.join(tree, '**/*.asm'), recursive=True) + glob.glob(os.path.join(tree, 'asm/bin/text/**/*.txt'), recursive=True):
        rel = os.path.relpath(p, tree)
        if rel in ('asm/graphics.asm', 'asm/overlay_scenes.asm') or 'Uncompressed_Text' in rel: continue   # moved by build.sh variables / regenerated
        s = open(p, 'rb').read().decode('latin-1')
        s = '\n'.join(re.sub(r';.*|//.*', '', l) for l in s.splitlines())
        for m in re.finditer(r'(?im)(\.org\s+0x0?9[0-9a-f]{6}\b|#JMP\(\$0?1[0-9a-f]{6}\))', s): left.append('%s: %s' % (rel, m.group(1)))
    if left: sys.exit('rom16: unhandled >16 MiB placements:\n  ' + '\n  '.join(left))
    print('rom16: %d placements rewritten (text 0x%08X, VWF minifont 0x08E5D98C, patches 0x08F00000+)' % (n, 0x08000000 + TEXT_LO))
def snap(rom, out):
    d = open(rom, 'rb').read(); seg = d[TEXT_LO:TEXT_HI]; end = len(seg.rstrip(b'\xff'))
    if end == 0: sys.exit('rom16: no text at 0x%08X' % (0x08000000 + TEXT_LO))
    if end > len(seg) - 0x1000: sys.exit('rom16: uncompressed text too close to the graphics area (0x%X bytes)' % end)
    open(out, 'wb').write(seg[:end]); print('rom16: text 0x%08X-0x%08X (%d bytes)' % (0x08000000 + TEXT_LO, 0x08000000 + TEXT_LO + end, end))
def final(base, rom, snapf):
    b = open(base, 'rb').read(); d = bytearray(open(rom, 'rb').read()); bad = []
    if len(d) != 0x1000000: bad.append('size %d, not 16 MiB (something was written above 0x08FFFFFF)' % len(d))
    s = open(snapf, 'rb').read()
    if d[TEXT_LO:TEXT_LO + len(s)] != s: bad.append('uncompressed text area changed after Atlas (overlap with a later write)')
    # 0x09xxxxxx-shaped words also occur inside LZ/tile/table data, so they are only counted here; the proof that no
    # pointer still targets >16 MiB is tools/rom16_audit.py (diff against the 32 MiB build) plus the emulator read watch.
    new = [o for o in range(0, min(len(d), len(b)) - 3, 4) if d[o+3] == 0x09 and d[o:o+4] != b[o:o+4]]
    print('rom16: note: %d aligned 0x09xxxxxx-shaped words differ from the base (data; see rom16_audit.py)' % len(new))
    c = (-sum(d[0xA0:0xBD]) - 0x19) & 0xFF
    if d[0xBD] != c: print('rom16: header checksum 0x%02X -> 0x%02X' % (d[0xBD], c)); d[0xBD] = c; open(rom, 'wb').write(d)
    if bad: sys.exit('rom16 FAILED: ' + '; '.join(bad))
    print('rom16: OK - 16 MiB, header checksum 0x%02X, data end 0x%X, %d bytes 0xFF after it' % (d[0xBD], len(d.rstrip(b'\xff')), len(d) - len(d.rstrip(b'\xff'))))
if __name__ == '__main__':
    a = sys.argv[1:]
    {'prep': lambda: prep(a[1]), 'snap': lambda: snap(a[1], a[2]), 'final': lambda: final(a[1], a[2], a[3])}[a[0]]()

#!/usr/bin/env python3
"""pause_popin_fix.py BASE_ROM OUT.asm  - armips include that moves upstream's pause-tab pop-in labels one entry earlier.
Upstream's asm/graphics.asm writes the Hints, Stuff and Rides pop-in label OAM at 0x0863D68A, 0x0863D88E and 0x0863DC96.
Each of those is 6 bytes (one 6-byte sprite entry) past the group's first entry (group header '00 00 nn 00' at -4).
So the first JP label sprite survives, and it now points at an unrelated tile, which shows as a stray dark box for one frame
when the tab pops in. The JP sprite after the label is also overwritten. This include writes the same upstream files at the
right address and restores that next JP entry (6 bytes, read from the base ROM at build time)."""
import sys
GROUPS = [(0x0863D684, 'asm/bin/graphics/pausemenu/OAM/1hintoam.bin', 18),
          (0x0863D888, 'asm/bin/graphics/pausemenu/OAM/2stuffoam.bin', 24),
          (0x0863DC90, 'asm/bin/graphics/pausemenu/OAM/4vehiclesignoam.bin', 24)]
rom = open(sys.argv[1], 'rb').read(); out = []
for first, f, n in GROUPS:
    h = rom[first - 4 - 0x08000000: first - 0x08000000]
    assert h[0] == 0 and h[1] == 0 and h[3] == 0, 'no group header before %08X' % first
    nxt = rom[first + n - 0x08000000: first + n + 6 - 0x08000000]
    out.append('.org 0x%08X\n\t.incbin "%s"\n\t.byte %s\t; JP entry restored' % (first, f, ','.join('0x%02X' % b for b in nxt)))
open(sys.argv[2], 'w').write('\n'.join(out) + '\n')
print('pause_popin_fix: %d groups' % len(GROUPS))

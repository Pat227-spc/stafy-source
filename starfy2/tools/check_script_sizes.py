#!/usr/bin/env python3
"""Build check (Starfy 2): fail if any in-level conversation script (pointer table 0x0814E22C, 510 LZ entries)
decompresses to >= LIMIT bytes. The game decompresses them into one heap block allocated at 0x080CDFF4
(stock 0x2000; overlay/patches/80_chat_script_buffer.asm raises it to 0x3000). The check reads the limit from the ROM's own allocation
instruction, so it also stays correct if fix B is applied.
usage: check_script_sizes.py ROM [--margin N]   exit 1 on failure"""
import sys,struct,os
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'gfx')); import lz10 as LZ
a=sys.argv[1:]; rom=open(a[0],'rb').read(); margin=int(a[a.index('--margin')+1],0) if '--margin' in a else 0
op=rom[0xCDFF4:0xCDFF8]   # movs r0,#imm8 ; lsls r0,r0,#6
assert op[1]==0x20 and op[2:4]==bytes([0x80,0x01]), 'unexpected code at 0x080CDFF4: %s'%op.hex()
LIMIT=op[0]<<6
bad=[]; mx=(0,0)
for i in range(510):
    p=struct.unpack_from('<I',rom,0x14E22C+4*i)[0]
    n=len(LZ.decompress(rom,p&0x1FFFFFF)); mx=max(mx,(n,i))
    if n>=LIMIT-margin: bad.append((i,hex(p),n))
print('buffer 0x%X, largest script #%d = %d bytes'%(LIMIT,mx[1],mx[0]))
for b in bad: print('FAIL entry #%d at %s: %d bytes >= 0x%X%s'%(b[0],b[1],b[2],LIMIT,' - margin' if margin else ''))
sys.exit(1 if bad else 0)

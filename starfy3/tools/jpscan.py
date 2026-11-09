"""Leftover-Japanese scan over every live EN BMG file reached through the message table.
Skips only the JP developer test file in slot 13 (by slot index, not address — a relocated
file must not escape the skip). Prints file#msg and a snippet for every message with kana/kanji."""
import sys,os,re,struct
sys.path.insert(0,os.path.dirname(__file__))
from bmg import BMG
from s3text import dec
JP=re.compile(r'[\u3041-\u3096\u30a1-\u30fa\u30fc\u4e00-\u9fff]')
def slots(d):
    """Unique (slot_index, file_addr) pairs in table order (first slot wins)."""
    out=[]; seen=set()
    for k in range(27):
        f=struct.unpack('<I',d[0x192978+4*k:0x192978+4*k+4])[0]-0x08000000
        if f not in seen:
            seen.add(f); out.append((k,f))
    return out
def files(d):
    """Unique file addresses (compat). Prefer slots() when the slot index matters."""
    return [f for _,f in slots(d)]
def scan(d, skip_slots=(13,)):
    out=[]
    for k,f in slots(d):
        if k in skip_slots: continue
        for i,m in enumerate(BMG(d,f).msgs):
            t=dec(m)
            names=''.join(bytes.fromhex(x).decode('cp932','replace') for x in re.findall(r'\{1a..020001..((?:[0-9a-f]{4})+)\}',t))
            body=re.sub(r'\{[0-9a-f]+\}','',t)
            if JP.search(body) or JP.search(names): out.append((k,f,i,(names+' | '+body)[:110]))
    return out
if __name__=='__main__':
    for r in scan(open(sys.argv[1],'rb').read()): print('slot%02d %X#%d %s'%r)

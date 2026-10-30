"""Stafy 1 (Origins cut) script codec + pointer tables. Text table discovered by scan."""
import struct
CH={}
for i in range(10): CH[i]=str(i)
for i in range(26): CH[0x0A+i]=chr(65+i); CH[0x24+i]=chr(97+i)
CH.update({0xFC:' ',0x3F:'!',0x3E:'?',0x42:'.',0x43:',',0x44:"'",0x5A:'…',0x45:'-'})
INV={v:k for k,v in CH.items()}
TEXT_LO,TEXT_HI=0x08700000,0x08770000
TABLES=[(0x2169AC,0x216CCC),(0x23103C,0x231A50),(0x27B0A0,0x27B790)]  # hint/story, dialogue, picture book
def tables(d): return TABLES
def tables_scan(d):
    """contiguous runs (>=8) of words pointing into the script area (used once to find TABLES)"""
    runs=[];o=0x200000
    while o<0x300000:
        if TEXT_LO<=struct.unpack_from('<I',d,o)[0]<TEXT_HI:
            s=o
            while TEXT_LO<=struct.unpack_from('<I',d,o)[0]<TEXT_HI: o+=4
            if (o-s)//4>=8: runs.append((s,o))
        else: o+=4
    return runs
def msg_end(d,p):
    k=p
    while True:
        if d[k]==0xFF:
            c=d[k+1]
            if c==0xFF: return k+2
            k+= 3 if c==0xEC else 2
        else: k+=1
def decode(b):
    """bytes (without final FFFF) -> editable string. colour prefix FF EF -> '\\x01'; other codes -> {FFxx}/{FFECxx}; unknown -> {xx}"""
    out=[];k=0
    while k<len(b):
        x=b[k]
        if x==0xFF:
            c=b[k+1]
            if c==0xEF: out.append('\x01'); k+=2
            elif c==0xFE: out.append('/'); k+=2
            elif c==0xFB: out.append('{FFFB}'); k+=2
            elif c==0xEC: out.append('{FFEC%02X}'%b[k+2]); k+=3
            else: out.append('{FF%02X}'%c); k+=2
        else:
            out.append(CH[x] if x in CH else '{%02X}'%x); k+=1
    return ''.join(out)
def encode(s):
    out=bytearray();k=0
    while k<len(s):
        c=s[k]
        if c=='\x01': out+=b'\xff\xef'; k+=1
        elif c=='/': out+=b'\xff\xfe'; k+=1
        elif c=='{':
            j=s.index('}',k); out+=bytes.fromhex(s[k+1:j]); k=j+1
        else: out.append(INV[c]); k+=1
    return bytes(out)
def messages(d):
    ms={}
    for s,e in tables(d):
        for o in range(s,e,4):
            p=struct.unpack_from('<I',d,o)[0]-0x08000000
            ms.setdefault(p,[]).append(o)
    return ms
def plain(s):
    import re
    return re.sub(r'\{[0-9A-F]+\}','',s.replace('\x01','')).replace('/',' ')

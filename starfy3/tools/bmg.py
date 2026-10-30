"""Minimal Nintendo BMG ("MESGbmg1", big-endian) reader/writer as used by Densetsu no Stafy 3 (INF1 entry size 4,
DAT1 null-terminated strings with 0x1A escapes, MID1 kept verbatim)."""
import struct
def msg_bytes(dat,off):
    k=off
    while True:
        x=dat[k]
        if x==0: return bytes(dat[off:k])
        if x==0x1A: k+=dat[k+1]; continue
        if (0x81<=x<=0x9F) or (0xE0<=x<=0xFC): k+=2; continue
        k+=1
class BMG:
    def __init__(self,d,at):
        self.at=at; assert d[at:at+8]==b'MESGbmg1'
        self.hdr=bytearray(d[at:at+0x20]); n=struct.unpack('>I',d[at+12:at+16])[0]
        self.size=struct.unpack('>I',d[at+8:at+12])[0]
        p=at+0x20; self.secs=[]
        for _ in range(n):
            mg=d[p:p+4]; ss=struct.unpack('>I',d[p+4:p+8])[0]; self.secs.append((bytes(mg),bytes(d[p:p+ss]))); p+=ss
        inf=dict(self.secs)[b'INF1']; dat=dict(self.secs)[b'DAT1']
        self.cnt,self.esz=struct.unpack('>HH',inf[8:12]); assert self.esz==4
        self.inf_hdr=inf[:16]
        offs=[struct.unpack('>I',inf[16+4*i:20+4*i])[0] for i in range(self.cnt)]
        self.dat_raw=dat[8:]
        self.msgs=[msg_bytes(self.dat_raw,o) for o in offs]
        self.offs=offs
    def build(self):
        dat=bytearray(b'\x00'); offs=[]; seen={}
        for m in self.msgs:
            if m==b'': offs.append(0); continue
            offs.append(len(dat)); dat+=m+b'\x00'
        while (len(dat)+8)%0x20: dat.append(0)
        inf=bytearray(self.inf_hdr)+b''.join(struct.pack('>I',o) for o in offs)
        while len(inf)%0x20: inf.append(0)
        struct.pack_into('>I',inf,4,len(inf))
        datsec=bytearray(b'DAT1')+struct.pack('>I',len(dat)+8)+dat
        out=bytearray(self.hdr); secs=[]
        for mg,raw in self.secs:
            secs.append(inf if mg==b'INF1' else datsec if mg==b'DAT1' else raw)
        out+=b''.join(secs); struct.pack_into('>I',out,8,len(out)); return bytes(out)

def build_append(b, changes, keep_pad=False):
    """Rebuild keeping the original DAT1 bytes untouched; changed messages {idx: bytes} are appended to the end of
    DAT1 and only their INF1 offsets change. Section/file sizes are updated, 0x20 alignment kept."""
    raw=bytearray(b.dat_raw)
    while raw and raw[-1]==0: raw.pop()
    raw.append(0)
    # keep_pad (v1.0.2-test on): keep the zero padding that unchanged entries still point into (F70078 #530-#539 and
    # F8DF58 #33 point past the last string = empty messages); otherwise appended messages land under them.
    # Off for --v101/plain builds so v1.0-test / v1.0.1-test still rebuild byte-identical.
    if keep_pad:
        while len(raw)<=max(b.offs): raw.append(0)
    offs=list(b.offs)
    for i,m in sorted(changes.items()):
        offs[i]=len(raw); raw+=m+b'\x00'
    while (len(raw)+8)%0x20: raw.append(0)
    inf=bytearray(b.inf_hdr)+b''.join(struct.pack('>I',o) for o in offs)
    old_inf=dict(b.secs)[b'INF1']
    inf+=old_inf[len(inf):] if len(old_inf)>len(inf) else b''
    while len(inf)%0x20: inf.append(0)
    struct.pack_into('>I',inf,4,len(inf))
    datsec=bytearray(b'DAT1')+struct.pack('>I',len(raw)+8)+raw
    out=bytearray(b.hdr)
    for mg,r in b.secs: out+= inf if mg==b'INF1' else datsec if mg==b'DAT1' else r
    struct.pack_into('>I',out,8,len(out)); return bytes(out)

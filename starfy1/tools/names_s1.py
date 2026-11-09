"""Starfy 1 v1.0.4: cross-game name pass (series names decided 2026-11-03, same names as Starfy 2/3).
Runs on the v1.0.3 ROM (CRC32 44C2017A, the output of build_s1.py --v103) and writes the v1.0.4 ROM.
usage: names_s1.py IN.gba OUT.gba [--log names.tsv]
Every rename is word-bounded and applied to both the plain and the colour-highlighted (per-letter FF EF) forms,
in all three message tables (hint/story, dialogue, Picture Book). Dialogue boxes that now overflow are re-wrapped
with the same 198 px rule as build_s1.py; other tables are only checked (the build fails if a line grows past the
widest line already in that table). Messages that no longer fit in place are moved to free space at 0x784000+."""
import sys,os,re,struct,zlib
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from s1text import *; from s1width import *
import build_s1 as B
IN_CRC='44C2017A'
FREE=0x784000          # build_s1 --v103 uses 0x780000-0x78344A; 0x784000-0x7FFFFF is 0xFF filler
# (old, new). Order matters: longer / more specific forms first.
NAMES=[
 # series names decided 2026-11-03 and official TLS (The Legendary Starfy, DS) names
 ('Pufftop Soldiers','Pufftop Guards'),('Pufftop Soldier','Pufftop Guard'),   # テンカイヘイシ (TLS)
 ('Pearl Keeper','Pearl Sprite'),                                          # パールキーパー (TLS)
 ('Ultra Spin','Ultra Star Spin'),                                         # スピンアタックレベル3 (TLS)
 ('Crab Family','Crawfamily'),('Cradaddy','Crawdaddy'),('Crababy','Crawbaby'),   # カンニンオヤコ / パパ / チビ
 ('Jiilacanth','Papacool'),('Jilacanth','Papacool'),                       # ジイラカンス
 ('Georgiro','Jawbreaker'),('Georgio','Jawbreaker'),                       # ジョージロー
 ('Konbi','Coalbies'),                                                     # コンビー
 ('Woe','Joe'),('Loe','Shmoe'),                                            # ショロスケ / チョロスケ
 ('Resturtle','Chubturtle'),('Gain','CLANGshell'),('Modoki','Mockturtle'),('Rarity','Rarescale'),
 ('Gunn','Pistolfin'),('Hirapa','Mophead'),('Phlat','Phlatzo'),('Sharmin','Skullshark'),('Reacher','Lungeeel'),
 ('Hunn','Cannonfin'),('Bogyo','Jumpyre'),('Blade','Wakazashi'),('Buu','Flappy Oink'),('Gufu','Druul'),
 ('Tobeifish','Jetsetfish'),('Samett','Sharkapult'),('Eelastic','Serprise'),('Ridox','Dumbark'),
 # Picture Book names picked in round 2 (2026-11-03; already in Starfy 2)
 ('Chiku','Jellspike'),('Choki','Clippercrab'),('Sawawa','Hushbrush'),('Potori','Dropzzy'),('Uga','Ooga'),
 ('Lyte','Lampyre'),('Chochin','Lantongue'),('Mayucoin','Browcoin'),('Zuratta','Octofro'),('Komelt','Comelt'),
 ('Lumi The Mirror','Lumi the Mirror'),('Traveller','Traveler'),('Akko','Angloom'),
 # Moe's オレさま boast: "the Great Moe" (capital G); Joe's parody of it follows
 ('the great Moe','the Great Moe'),('The great Moe','The Great Moe'),('the great Joe','the Great Joe'),
]
def pat(a):
    """word-bounded regex matching a in plain or per-letter colour form; a space may also be a line break '/';
    a trailing plural 's' is allowed (kept as is)"""
    body=''.join(('(?:\x01)?'+re.escape(c)) if c!=' ' else '[ /]' for c in a)
    return re.compile(r'(?<![A-Za-z])'+body+r'(?=(?:\x01?s)?(?!\x01?[a-z]))')
def colour_like(src,new):
    seps=re.findall(r'[ /]',src); words=new.split(' ')
    if len(seps)==len(words)-1: new=''.join(w+(seps[i] if i<len(seps) else '') for i,w in enumerate(words))
    return B.col(new).replace('\x01/','/') if '\x01' in src else new
PATS=[(pat(a),a,b) for a,b in NAMES]
def rename(s,counts,where,log):
    for rx,a,b in PATS:
        def f(m):
            counts[a]=counts.get(a,0)+1; log.append(('rename',where,a,b)); return colour_like(m.group(0),b)
        s=rx.sub(f,s)
    return s
def widest(d,tabs,ti):
    w=0
    for o in range(tabs[ti][0],tabs[ti][1],4):
        p=struct.unpack_from('<I',d,o)[0]-0x08000000; e=msg_end(d,p)
        for box in re.split(r'\{FF(?:FB|EA|F9)\}',decode(d[p:e-2])):
            for ln in box.split('/'): w=max(w,line_px(B.W,ln))
    return w
def main(src,dst,logf=None):
    d=bytearray(open(src,'rb').read())
    assert '%08X'%zlib.crc32(d)==IN_CRC, 'input must be Starfy 1 v1.0.3 (44C2017A)'
    B.W=table(d); tabs=tables(d); ms=messages(d)
    cat={}
    for ti,(a,e) in enumerate(tabs):
        for o in range(a,e,4): cat[struct.unpack_from('<I',d,o)[0]-0x08000000]=ti
    lim={0:widest(d,tabs,0),1:B.LIMIT,2:widest(d,tabs,2)}
    counts={}; log=[]; free=FREE
    assert all(x==0xFF for x in d[FREE:0x800000])
    for p in sorted(ms):
        e=msg_end(d,p); old=decode(d[p:e-2]); s=rename(old,counts,hex(p),log)
        if s==old: continue
        if cat[p]==1: s=B.fix_overflow(s,p,log)
        for box in re.split(r'\{FF(?:FB|EA|F9)\}',s):
            for ln in box.split('/'):
                w=line_px(B.W,ln)
                assert w<=lim[cat[p]], ('line too wide',hex(p),cat[p],w,lim[cat[p]],plain(ln))
        assert not any(x[0]=='OVERFLOW-UNFIXED' and x[1]==hex(p) for x in log), hex(p)
        log.append(('text',hex(p),cat[p],plain(old),plain(s)))
        nb=encode(s)+b'\xff\xff'
        if len(nb)<=e-p:
            d[p:p+len(nb)]=nb; d[p+len(nb):e]=b'\xff'*(e-p-len(nb))
        else:
            assert all(x==0xFF for x in d[free:free+len(nb)])
            d[free:free+len(nb)]=nb
            for o in ms[p]: struct.pack_into('<I',d,o,0x08000000+free)
            others=[o for o in range(0,len(d)-3,4) if struct.unpack_from('<I',d,o)[0]==0x08000000+p and o not in ms[p]]
            assert not others,(hex(p),others)
            log.append(('relocated',hex(p),hex(free),len(nb))); free=(free+len(nb)+3)&~3
    open(dst,'wb').write(d)
    if logf:
        with open(logf,'w') as f:
            for x in log: f.write('\t'.join(str(y).replace('\x01','').replace('\n',' ') for y in x)+'\n')
    print('renames',counts,'total',sum(counts.values()),'free used',hex(free-FREE),'CRC %08X'%zlib.crc32(d))
if __name__=='__main__':
    a=sys.argv[1:]; lf=None
    if '--log' in a: i=a.index('--log'); lf=a[i+1]; del a[i:i+2]
    main(a[0],a[1],lf)

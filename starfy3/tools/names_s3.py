"""Starfy 3 v1.0.5: cross-game name pass (series names decided 2026-11-03, same names as Starfy 1/2).
Runs on the v1.0.4 ROM (CRC32 4F31E799, the output of build_s3.py --v104) and writes the v1.0.5 ROM.
usage: names_s3.py IN.gba OUT.gba [--log names.tsv]
- Renames are word-bounded, in dialogue text, Picture Book / item files (fullwidth or ASCII-byte style) and in speaker
  name tags (tag length byte rebuilt; tagfix() from build_s3 keeps the name-plate redraw working).
- Moe's "yours truly" / selected オレさま lines become "the Great Moe" (decisions 2026-11-03 and 2026-11-09).
- Hirara becomes Snarley (decision 2026-11-09).
- Changed BMG files are rebuilt with build_append (original DAT1 bytes kept, edited messages appended), placed in
  free space from FREE and both message-table entries repointed. The JP dev test file (slot 13) is not touched."""
import sys,os,re,struct,zlib
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from bmg import BMG,build_append
from s3text import dec,enc
import build_s3 as B
IN_CRC=0x4F31E799
TABLES=B.TABLES
# free space: 0xE80108-0xEFFFFF is 0xFF filler in both the JP Rev 1 ROM and Dimedime v1.0 (nothing in the JP game can
# point there); 0xFED120-0xFFFFFF is the filler left after build_s3 --v104. First fit, 0x20-aligned.
REGIONS=[[0xE80200,0xF00000],[0xFED140,0x1000000]]
NAMES=[
 # series names decided 2026-11-03 and official TLS (The Legendary Starfy, DS) names
 ('Pufftop Soldiers','Pufftop Guards'),('Pufftop Soldier','Pufftop Guard'),   # テンカイヘイシ (TLS)
 ('Jellato Siblings','Jellato Sisters'),                                   # クリオレたち (TLS)
 ('Jawjiro','Jawbreaker'),('Hirao','Halo'),('Hirarin','Haley'),('Hirara','Snarley'),('Torito','Tweeto'),('Coelagramps','Papacool'),
 ('Resturtle','Chubturtle'),('Gain','CLANGshell'),('Buu','Flappy Oink'),('Modoki','Mockturtle'),('Rarity','Rarescale'),
 ('Gufu','Druul'),('Tobeifish','Jetsetfish'),('Eelastic','Serprise'),('Bogyo','Jumpyre'),('Hirapa','Mophead'),
 ('Sharmin','Skullshark'),('Blade','Wakazashi'),('Samett','Sharkapult'),('Jiappo','Liftwhisp'),('Ridox','Dumbark'),
 # Picture Book names picked in round 2 (2026-11-03; already in Starfy 2)
 ('Chiku','Jellspike'),('Choki','Clippercrab'),('Sawawa','Hushbrush'),('Uga','Ooga'),('Melty','Meltfy'),
 ('Chochin','Lantongue'),('Mayucoin','Browcoin'),('Zuratta','Octofro'),('Komelt','Comelt'),('Bakiross','Bankiross'),
 ('Akko','Angloom'),('Russel','Russell'),('Spark Ball','Sparkball'),
]
# Moe's オレさま -> "the Great Moe" where the English already used the boast form (JP checked line by line)
MOE={(0xF44BF8,5):[("as cool/and dependable as yours truly","as cool/and dependable as the Great Moe")],
     (0xFD11A0,4):[("as cool as/yours truly!","as cool as/the Great Moe!")],
     (0xFD11A0,49):[("then yours truly'll","then the Great Moe'll")],
     (0xFDC9E0,322):[("Like yours truly!","Like the Great Moe!")],
     # Tier A (decision 2026-11-09): 15 more オレさま lines -> the Great Moe
     (0xFC6C80,21):[("Yours truly is on drums!","The Great Moe's on drums!")],
     (0xFDC9E0,407):[("They have fine and cute eyes for/sure. Not as pretty as your's/truly's eyes, though!",
                      "They have pretty cute eyes, I'll/give 'em that. Not as cute as/the Great Moe's, though!")],
     (0xF003B8,1):[("That's my, the cool and reliable Moe's,/job!","That's a job for the cool and reliable/Great Moe!")],
     (0xF003B8,22):[("Looks like you/want me to clobber you again!","Looks like you want/the Great Moe to clobber you again!")],
     (0xF003B8,30):[("You're lucky I rushed down here/to save you...","You're lucky the Great Moe/rushed down here to save you...")],
     (0xF54E78,24):[("Those two really can't do a/thing without me!","Those two really can't/do a thing without the Great Moe!")],
     (0xFDC9E0,313):[("Ya wanna be like me?/Don't think so!","Ya wanna be like the Great Moe?/Don't think so!")],
     (0xFDC9E0,329):[("But I'm certain that my own/shell is far superior!","But the Great Moe's shell/is way cooler, obviously!")],
     (0xFDC9E0,349):[("He's all cool and stern./Not as cool as me, of course!","He's all cool and stern./Not as cool as the Great Moe,/of course!")],
     (0xFDC9E0,355):[("It's an interesting strategy,/but it's not really my style, if/ya catch my drift.",
                      "Not that it matters. They're/still no match for the/Great Moe!")],
     (0xFDC9E0,379):[("By the way, aren't I a cool clam?/Ya know that, right?","By the way, the Great Moe is/one cool clam. Ya knew that,/right?")],
     (0xFDC9E0,458):[("But he sure doesn't have the looks!/I'm handsome, but he's ugly,/right?",
                      "But he sure doesn't have the looks!/The Great Moe is handsome. This/guy? Ugly!")],
     (0xFDC9E0,473):[("They should learn from me about/bein' reliable!","They oughta learn a thing or/two from the Great Moe!")],
     (0xFDC9E0,485):[("Good thing I stepped in to save/the day! Starfy couldn't've/beaten it without my help!",
                      "Good thing the Great Moe/stepped in! Starfy couldn't've/beaten it without me!")],
     (0xFDC9E0,517):[("It'll take more than that to/scare me!","It'll take more than that to/scare the Great Moe!")]}
def tokens(run):
    """split a text run into characters (1 or 2 bytes); norm = one char per token: Latin letters (fullwidth or
    ASCII) as ASCII, the three separators (ASCII space, fullwidth space, newline) as ' ', anything else as '#'"""
    toks=[];k=0
    while k<len(run):
        x=run[k]; n=2 if (0x81<=x<=0x9F) or (0xE0<=x<=0xFC) else 1
        toks.append(bytes(run[k:k+n])); k+=n
    norm=''
    for t in toks:
        if len(t)==1: c=chr(t[0]); norm+= c if c.isascii() and c.isalpha() else ' ' if t in (b' ',b'\n') else "'" if t==b"'" else '#'
        else:
            try: u=t.decode('cp932')
            except UnicodeDecodeError: u='#'
            o=ord(u[0]) if len(u)==1 else 0
            norm+= chr(o-0xFEE0) if 0xFF21<=o<=0xFF5A and chr(o-0xFEE0).isalpha() else ' ' if u=='\u3000' else "'" if u=='’' else '#'
    return toks,norm
def pat(a):
    return re.compile(r'(?<![A-Za-z])'+re.escape(a).replace(r'\ ',' ')+r"(?=s?(?![a-z]))")
PATS=[(pat(a),a,b) for a,b in NAMES]
def enc_like(srctoks,new):
    """encode new in the style of the matched tokens: ASCII-byte letters or fullwidth; keep the separators"""
    ascii_style=any(len(t)==1 and t not in (b' ',b'\n') for t in srctoks)
    seps=[t for t in srctoks if t in (b' ',b'\n',b'\x81\x40')]; words=new.split(' ')
    out=b''
    for i,w in enumerate(words):
        out+= w.encode('ascii') if ascii_style else enc(w)
        if i<len(words)-1: out+= seps[i] if i<len(seps) else b' '
    return out
def rename_run(run,cnt,log,where):
    toks,norm=tokens(run); changed=False
    for rx,a,b in PATS:
        while True:
            m=rx.search(norm)
            if not m: break
            src=toks[m.start():m.end()]; nb=enc_like(src,b)
            toks[m.start():m.end()]=[nb]; norm=norm[:m.start()]+'@'+norm[m.end():]
            cnt[a]=cnt.get(a,0)+1; log.append(('rename',where,a,b)); changed=True
    return b''.join(toks),changed
def rename_text(t,cnt,log,where):   # plain-string version (speaker tags)
    for rx,a,b in PATS:
        def f(m):
            cnt[a]=cnt.get(a,0)+1; log.append(('rename',where,a,b)); return b
        t=rx.sub(f,t)
    return t
TAG=re.compile(rb'\x1a(.)\x02\x00\x01(.)',re.S)
def rename_msg(m,cnt,log,where):
    """split into escapes / text runs; rename text runs (via dec/enc) and speaker-tag names"""
    out=bytearray(); k=0; run=bytearray()
    def flush():
        if run:
            nb,_=rename_run(bytes(run),cnt,log,where); out.extend(nb); run.clear()
    while k<len(m):
        x=m[k]
        if x==0x1A:
            flush(); L=m[k+1]; esc=m[k:k+L]
            if L>6 and esc[2:5]==b'\x02\x00\x01':
                name=esc[6:]; words=name.split(b'\x82\x59'); nt='<8259>'.join(dec(w) for w in words)
                t2=rename_text(nt.replace('<8259>',' ').replace('~',' '),cnt,log,where+' tag')
                if t2!=nt.replace('<8259>',' ').replace('~',' '):
                    nb=b'\x82\x59'.join(enc(w) for w in t2.replace('~',' ').split(' '))
                    esc=bytes([0x1a,6+len(nb)])+esc[2:6]+nb
            out+=esc; k+=L; continue
        if (0x81<=x<=0x9F) or (0xE0<=x<=0xFC): run+=m[k:k+2]; k+=2; continue
        run.append(x); k+=1
    flush(); return bytes(out)
def files(d):
    fs=[]
    for k in range(27):
        f=struct.unpack('<I',d[TABLES[0]+4*k:TABLES[0]+4*k+4])[0]-0x08000000
        if f not in fs: fs.append(f)
    return fs
def main(src,dst,logf=None):
    d=bytearray(open(src,'rb').read()); assert zlib.crc32(d)==IN_CRC, 'input must be Starfy 3 v1.0.4 (4F31E799)'
    cnt={}; log=[]; used=0
    for a,e in REGIONS: assert all(x==0xFF for x in d[a:e])
    for f in files(d):
        if f in (0x5A6B34,0xF68898): continue    # JP developer test file; debug message file (out of scope since v1.0, see RELEASE_NOTES)
        b=BMG(d,f); ch={}
        for i,m in enumerate(b.msgs):
            nm=rename_msg(m,cnt,log,'%X#%d'%(f,i))
            for a,c in MOE.get((f,i),[]):
                ea,ec=enc(a.replace(' ','~')),enc(c.replace(' ','~'))
                assert nm.count(ea)==1, ('MOE target',hex(f),i,a); nm=nm.replace(ea,ec); cnt['yours truly']=cnt.get('yours truly',0)+1
                log.append(('moe','%X#%d'%(f,i),a,c))
            if nm!=m:
                nm2,c=B.tagfix(nm)
                if c: log.append(('tagfix','%X#%d'%(f,i),c))
                ch[i]=nm2; log.append(('text','%X#%d'%(f,i),dec(m),dec(nm2)))
        if not ch: continue
        nb=build_append(b,ch,keep_pad=True)
        r=[r for r in REGIONS if r[0]+len(nb)<=r[1]]; assert r, 'out of free space'
        at=r[0][0]; r[0][0]=(at+len(nb)+0x1F)&~0x1F; used+=len(nb)
        assert all(x==0xFF for x in d[at:at+len(nb)])
        d[at:at+len(nb)]=nb
        for t in TABLES:
            hit=[k for k in range(t,t+0x70,4) if struct.unpack('<I',d[k:k+4])[0]==0x08000000+f]
            assert len(hit)==1,(hex(f),hex(t)); struct.pack_into('<I',d,hit[0],0x08000000+at)
        log.append(('reloc','%X'%f,'%X'%at,len(nb),len(ch)))
    open(dst,'wb').write(d)
    if logf:
        with open(logf,'w') as fo:
            for x in log: fo.write('\t'.join(str(y).replace('\n',' ') for y in x)+'\n')
    print('renames',cnt,'total',sum(cnt.values()),'bytes placed',hex(used),'CRC %08X'%zlib.crc32(d))
if __name__=='__main__':
    a=sys.argv[1:]; lf=None
    if '--log' in a: i=a.index('--log'); lf=a[i+1]; del a[i:i+2]
    main(a[0],a[1],lf)

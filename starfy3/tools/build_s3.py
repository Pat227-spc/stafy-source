"""Stafy 3 (Dimedime v1.0) cleanup builder. base.gba (CRC 850B4137) -> out ROM.
- translates the leftover live Japanese messages (F09F58 #51 #55 #56 #57, F3A758 #40, F8DF58 #8-10 #32)
- typo fixes in place (same length): lackies->lackeys, Ukelele->Ukulele
- changed BMG files are re-emitted (original DAT bytes kept, edited messages appended) into free space at
  0xFB0000+ and both pointer-table entries (0x1929xx) repointed.
Not changed (verified in-game): 'Mr。 Polar' / 'Sgt。 Hawky' - glyph 0x8142 IS the game's '.' (0x8144 renders blank).
usage: build_s3.py base.gba out.gba [--v101|--v102|--v103]   (--v101: held-decision picks S3-001 1, S3-002 1, S3-003 2 + S006;
       --v102: v101 + "Chutah" -> "Chuta" everywhere, series consistency with Stafy 2 S007 / Stafy 1 S1-002 C;
       --v103: v102 + F5DEB8 #7 (FDA020 #7 in the v1.0.2 ROM) "This maybe" -> "This may be" (pause > Abilities, Jump)
       --v104: v103 + F09F58 #51 Baby Brother line in baby talk (2026-10-31, S3-002 option 3))"""
import sys,os,struct,zlib,re
sys.path.insert(0,os.path.dirname(__file__))
from bmg import BMG,build_append
from s3text import enc
BASE_CRC=0x850B4137
TABLES=(0x192978,0x1929E8)
FREE=0xFB0000
V104=False
C1,C0=bytes.fromhex('1a06ff000001'),bytes.fromhex('1a06ff000000')
def tag(name,col):
    nb=b''
    for w_i,w in enumerate(name.split(' ')):
        if w_i: nb+=b'\x82\x59'
        nb+=enc(w)
    return bytes([0x1a,6+len(nb),2,0,1,col])+nb
def E(s):  # dialogue text: '/' newline, '{c}' / '{/c}' colour on/off
    out=b''
    for part in re.split(r'(\{c\}|\{/c\})',s):
        out+= C1 if part=='{c}' else C0 if part=='{/c}' else enc(part)
    return out
def A(s): return s.replace('/','\n').encode('ascii')  # treasure-description file uses plain ASCII
def rebuild_msg(old, pages, keep_head=1):
    """old message: keep the leading control escapes and the trailing control tail; replace the talk pages."""
    m=old
    first_tag=re.search(rb'\x1a.\x02\x00\x01',m).start()
    tail=m.index(b'\n\x1a\x06\x01\x00\x03\x00')  # end-of-talk control sequence
    return m[:first_tag]+b''.join(pages)+m[tail:]
def edits():
    J={}
    # NB the engine only redraws the name plate when the new tag differs from the old one within ~the first 12
    # characters, so "Moe’s Little Brother" -> "Moe’s Little Sister" overprints. Sister tag shortened (decision S3-001).
    LB,LS,BB=tag("Moe’s Little Brother",1),tag("Moe’s Sister",1),tag("Moe’s Baby Brother",1)
    J[(0xF09F58,51)]=[LB+b'\n'+E("I wish Ruby and our big bro/would get married..."),
                     LS+b'\n'+E("But Ruby would have it real rough/with him!!"),
                     BB+b'\n'+(E("Whaddya tawkin' 'bout!?/I'm gonna marry Ruby!/Not him!") if V104 else E("Whaddya talkin' about!?/I'm the one who's gonna marry/Ruby!"))]
    V=tag("Moe’s Voice",8)
    for i,who in ((55,'Starf!'),(56,'Starly!'),(57,'Starf!')):
        if i==57: p2="If he gets away from ya,/try talkin' to this {c}speaker{/c}!"
        else:     p2="If {c}he gets away from ya,/try talkin' to this speaker!{/c}"
        J[(0xF09F58,i)]=[V+b'\n'+E(who+"/Corner that jerk!"), V+b'\n'+E(p2),
                         V+b'\n'+E("I'll tell ya the {c}password{/c}/to open the door over there!")]
    J[(0xF3A758,40)]=[tag("Moe",1)+b'\n'+E("Spin the terrain round and round/and take 'em down!")]
    T={}
    for i in (8,9,10): T[(0xF8DF58,i)]=A("One of Mamaus's/children! Save/all three and/take them back/to Mamaus!")
    T[(0xF8DF58,32)]=A("A Pufftop Child/taken by Evil's/henchmen! Looks/like it has a/crush on Moe!")
    return J,T
# v1.0.1-test decisions (2026-10-25): S3-001 1 and S3-002 1 keep the -test text; S3-003 2 translates the dev
# placeholders; S2 decision S006 (Pufftop Soldier everywhere) applied to the one テンカイヘイシ line rendered "Guards".
JP_DEV='かいはつちゅうです'.encode('cp932')
def edits_v101(d,files):
    R={}
    for i in range(30,50): R[(0xF5DEB8,i)]=lambda m: m.replace(JP_DEV,enc('Under development.'))
    R[(0xF4C7F8,48)]=lambda m: m.replace(enc("Pufftop Guards've"),enc("Pufftop Soldiers've"))
    return R
# v1.0.2-test (2026-10-25): Chutah -> Chuta in every live message, dialogue and name tags alike (tag escape length
# byte adjusted). 'Chuta' is a prefix of 'Chutah', but no 'Chutah' tag is left anywhere, and tagfix() below still
# catches any in-message prefix case.
CHUTAH,CHUTA=enc('Chutah'),enc('Chuta')
def chuta(m):
    out=bytearray(); k=0; n=0
    for x in TAGRE.finditer(m):
        if x.start()<k: continue
        L=m[x.start()+1]; tg=m[x.start():x.start()+L]
        out+=m[k:x.start()].replace(CHUTAH,CHUTA); n+=m[k:x.start()].count(CHUTAH)
        if CHUTAH in tg[6:]:
            nm=tg[6:].replace(CHUTAH,CHUTA); n+=tg[6:].count(CHUTAH); tg=bytes([0x1a,6+len(nm)])+tg[2:6]+nm
        out+=tg; k=x.start()+L
    out+=m[k:].replace(CHUTAH,CHUTA); n+=m[k:].count(CHUTAH)
    return bytes(out),n
TYPOS=[  # (needle, replacement) - every occurrence, same length, in place
    ('ｌａｃｋｉｅｓ'.encode('cp932'),'ｌａｃｋｅｙｓ'.encode('cp932')),
    ('Ｕｋｅｌｅｌｅ'.encode('cp932'),'Ｕｋｕｌｅｌｅ'.encode('cp932')),
    (b'Ukelele',b'Ukulele'),(b'ukelele',b'ukulele'),
    (enc('ya year me'),enc('ya hear me'))]
TAGRE=re.compile(rb'\x1a(.)\x02\x00\x01.',re.S)
def tagfix(m):
    """name-plate redraw fix: if a tag is a prefix of (or shares its first 12 chars with) the previous tag in the same
    message, the engine skips the redraw and the old name stays. Append the narrow blank 0x8259 so they differ early."""
    out=bytearray(m); prev=None; k=0; changed=0
    while True:
        x=TAGRE.search(bytes(out),k)
        if not x: break
        L=out[x.start()+1]; name=bytes(out[x.start()+6:x.start()+L])
        if prev is not None and name!=prev and (prev.startswith(name) or name[:24]==prev[:24]):
            assert prev.startswith(name), 'tag clash needs rewording: %r -> %r'%(prev,name)
            out[x.start()+1]=L+2; out[x.start()+L:x.start()+L]=b'\x82\x59'; changed+=1; name+=b'\x82\x59'; L+=2
        prev=name; k=x.start()+L
    return bytes(out),changed
def build(d, log=None, v101=False, v102=False, v103=False):
    v102=v102 or v103; v101=v101 or v102
    assert zlib.crc32(d)==BASE_CRC, 'wrong base'
    d=bytearray(d); L=log if log is not None else []
    for a,b in TYPOS:
        for m in re.finditer(re.escape(a),bytes(d)):
            assert 0xF00000<=m.start()<0xFA0000
            d[m.start():m.start()+len(a)]=b; L.append(('typo','%X'%m.start(),a.decode('cp932'),b.decode('cp932')))
    # long-vowel bar 'ー' (0x815B) used as a hyphen between Latin letters renders as a wide JP bar -> use '‐' (0x815D)
    LAT=rb'\x82[\x60-\x79\x81-\x9a]'
    for m in re.finditer(rb'(?<=%s)\x81\x5b(?=%s)'%(LAT,LAT),bytes(d)):
        if 0xF00000<=m.start()<0xFA0000 and not 0xF68898<=m.start()<0xF6BFF8:
            d[m.start()+1]=0x5D; L.append(('hyphen','%X'%m.start(),'ー','‐'))
    # stray closing bracket left at the end of a map-tutorial line (F87AB8 #210): terminate the string 2 bytes early
    k=bytes(d).index(enc('ones...')+'」'.encode('cp932')+b'\x00')+len(enc('ones...'))
    assert 0xF87AB8<k<0xF8DB78; d[k:k+2]=b'\x00\x00'; L.append(('stray','%X'%k,'」',''))
    # clipping fix: F80358 #149 line 1 runs off the screen edge (~228 px from x=14) -> move the line break (same length)
    a=enc('Bounce ＆ Trounce')+C0+b'\n'+enc('minigame'); b2=enc('Bounce ＆/Trounce')+C0+b' '+enc('minigame')
    k=bytes(d).index(a); assert 0xF80358<k<0xF851D8; d[k:k+len(a)]=b2; L.append(('rewrap','%X'%k,'F80358#149'))
    J,T=edits(); files={}
    for (f,i),pages in J.items(): files.setdefault(f,{})[i]=pages
    for (f,i),raw in T.items(): files.setdefault(f,{})[i]=raw
    allf=sorted(set(struct.unpack('<I',d[TABLES[0]+4*k:TABLES[0]+4*k+4])[0]-0x08000000 for k in range(27)))
    allf=[f for f in allf if f>=0xF00000]  # slot 13 -> 0x5A6B34 is the JP dev test file (unused)
    assert len(allf)==26, len(allf)
    at=FREE
    for f in allf:
        if f==0xF68898: continue  # debug message file: out of scope
        b=BMG(d,f); ch={}
        for i,v in files.get(f,{}).items():
            ch[i]=rebuild_msg(b.msgs[i],v) if isinstance(v,list) else v
            L.append(('msg','%X#%d'%(f,i),len(b.msgs[i]),len(ch[i])))
        if v101:
            for (ff,i),fn in edits_v101(d,files).items():
                if ff!=f: continue
                nm=fn(ch.get(i,b.msgs[i])); assert nm!=ch.get(i,b.msgs[i]), ('v101 edit had no effect',hex(f),i)
                ch[i]=nm; L.append(('v101','%X#%d'%(f,i),len(b.msgs[i]),len(nm)))
        if v102:
            for i,m in enumerate(b.msgs):
                nm,c=chuta(ch.get(i,m))
                if c: ch[i]=nm; L.append(('chuta','%X#%d'%(f,i),c))
        if v103 and f==0xF5DEB8:  # Abilities file (relocated to 0xFDA020 in v1.0.2)
            m=ch.get(7,b.msgs[7]); a3,b3=enc('This maybe'),enc('This may be')
            assert m.count(a3)==1, 'v103: F5DEB8#7 target not found'; ch[7]=m.replace(a3,b3); L.append(('v103','F5DEB8#7','This maybe','This may be'))
        for i,m in enumerate(b.msgs):
            nm,c=tagfix(ch.get(i,m))
            if c: ch[i]=nm; L.append(('tagfix','%X#%d'%(f,i),c))
        if not ch: continue
        nb=build_append(b,ch,keep_pad=v102); assert all(x==0xFF for x in d[at:at+len(nb)])
        d[at:at+len(nb)]=nb
        for t in TABLES:
            hit=[k for k in range(t,t+0x70,4) if struct.unpack('<I',d[k:k+4])[0]==0x08000000+f]
            assert len(hit)==1, (hex(f),hex(t)); struct.pack_into('<I',d,hit[0],0x08000000+at)
        L.append(('reloc','%X'%f,'%X'%at,len(nb)))
        at=(at+len(nb)+0x1F)&~0x1F
    return bytes(d)
if __name__=='__main__':
    V104='--v104' in sys.argv
    a=[x for x in sys.argv[1:] if x not in ('--v101','--v102','--v103','--v104')]; src,dst=a[:2]; log=[]
    out=build(open(src,'rb').read(),log,v101='--v101' in sys.argv,v102='--v102' in sys.argv,v103='--v103' in sys.argv or V104)
    open(dst,'wb').write(out)
    for x in log: print(*x,sep='\t')
    print('CRC %08X'%zlib.crc32(out))

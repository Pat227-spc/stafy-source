"""Build the Stafy 1 (Origins cut) cleanup ROM from the Origins v1.1 ROM (F7CB8EE3).
Clear-cut fixes only: typos, swapped Fork brother tags, Ogura alternating caps -> normal case, re-wrap of
dialogue lines that overflow the 198 px dialogue box. Usage: build_s1.py BASE.gba OUT.gba [--report r.md] [--v101]
--v101 adds the held-decision picks (S1-001 A, S1-002 C, S1-003 A).
--v102 (implies --v101) adds the v1.0.2 bug-report fixes (FIXES_V102)."""
import sys,struct,re,os,zlib
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from s1text import *; from s1width import *; from ogcase import convert_message, normalize_box, visible, ALT
LIMIT=198          # dialogue box: calibrated (198 ok, 200 wraps onto the first glyph)
FREE=0x780000      # 0x76B58A-0x7FFFFF is 0xFF filler in the Origins ROM
TYPOS=[('whimpy','wimpy'),('transportarion','transportation'),('interupting','interrupting'),('futher','further'),
 ('apparetly','apparently'),('burining','burning'),('acheck','a check'),('suprise','surprise'),('relavites','relatives'),
 ('repeative','repetitive'),('atatck','attack'),('gonnna','gonna'),('aginst','against'),('doppleganger','doppelganger'),
 ('attidude','attitude'),('assitance','assistance'),('messanger','messenger'),('acorss','across'),(' swin ',' swim '),
 ('not ony ','not only '),('guy flys ','guy flies '),("commin'","comin'"),('Thats enough','That\'s enough'),('comming','coming')]
def col(s): return ''.join(c if c==' ' else '\x01'+c for c in s)
NAMEFIX=[(col('Younger Fork Brother'),'@@OLD@@'),(col('Older Fork Brother'),col('Younger Fork Brother')),('@@OLD@@',col('Older Fork Brother'))]
OGURA_UNTAGGED={0x7010BA,0x7012F1,0x701689}
# v1.0.1-test decisions (2026-10-25): S1-001 A (Doppel to normal case), S1-002 C (series regulars renamed to the
# Stafy 2/3 names), S1-003 A (keep "barrely": no change)
CASE_SPEAKERS_V100=('Ogura','???','Mysterious Voice')
CASE_SPEAKERS_V101=CASE_SPEAKERS_V100+('Doppel',)
RENAMES=[  # applied to plain and colour-highlighted forms; order matters (longest first)
 ("Coalby? Who's that?","Coalbies? Who're they?"),  # Moe asks about the group (S1-002 C, plural like Stafy 3)
 ('Coalbys','Coalbies'),('Coalby','Coalbies'),
 ('Old Man Geko','Old Man Croak'),('Tweeto','Torito'),('Lovelin','Loverin')]   # Ogura's lines in the jar / game-over scenes (no name tag)
# v1.0.2 (2026-10-30, old Discord bug reports): clear-cut fixes only
FIXES_V102=[('Right…but Stafy…','Right…but Starfy…'),   # 0x71D1E7, Wozart's last line after first meeting him
            ('be used used to solve','be used to solve')]   # 0x72091C, Old Man Lobber
# stage-intro card level names (message group 0x216C84.., read by the card code at 0x08005DDA): re-pad with leading
# spaces so every name is centred on the 240 px screen (verified in-game: the card draws from x=0; spaces are 4 px).
# The second name set (group 0x216AC4.., 0x7016C4..) is NOT re-padded: no screen reached in testing reads it, so its
# window origin/width is unknown and 240 px centring could push names off-centre or out of a narrower window.
NAME_SETS=(set(range(0x704F6E,0x705006)),)
def center_name(s):
    body=s.strip(' '); w=line_px(W,body)-2
    return ' '*max(0,round((240-w)/2/4))+body
def rewrap(box):
    """box text between FFFB separators; returns new box or None if it cannot be fixed automatically"""
    m=re.match(r'^((?:\{FF(?:FC|FD)\})*/?)((?:\{FFECA9\}.*?\{FFEB\}/)?)(.*)$',box,re.S)
    pre,tag,body=m.groups()
    trail=re.search(r'(/?(?:\{FF(?:FC|FD)\})*/?)$',body).group(1); body=body[:len(body)-len(trail)] if trail else body
    words=body.replace('/',' ').split(' ')
    lines=[''];
    for w in words:
        if not w: continue
        cand=(lines[-1]+' '+w) if lines[-1] else w
        if line_px(W,cand)<=LIMIT: lines[-1]=cand
        else: lines.append(w)
    if len(lines)>3: return None
    return pre+tag+'/'.join(lines)+trail
def fix_overflow(s,p,log):
    parts=re.split(r'(\{FF(?:FB|EA|F9)\})',s)
    for i in range(0,len(parts),2):
        b=parts[i]
        if any(line_px(W,l)>LIMIT for l in b.split('/')):
            nb=rewrap(b)
            if nb is None: log.append(('OVERFLOW-UNFIXED',hex(p),b)); continue
            log.append(('rewrap',hex(p),b,nb)); parts[i]=nb
    return ''.join(parts)
def main(base,out,report=None,v101=False,v102=False):
    global W
    d=bytearray(open(base,'rb').read()); W=table(d)
    assert '%08X'%zlib.crc32(d)=='F7CB8EE3', 'base must be Origins v1.1 (F7CB8EE3)'
    ms=messages(d); tabs=tables(d)
    cat={}
    for ti,(a,e) in enumerate(tabs):
        for o in range(a,e,4): cat[struct.unpack_from('<I',d,o)[0]-0x08000000]=ti
    log=[]; free=FREE; counts={}
    for p in sorted(ms):
        e=msg_end(d,p); old=decode(d[p:e-2]); s=old
        for a,b in TYPOS:
            n=s.count(a)
            if n: counts[a]=counts.get(a,0)+n; s=s.replace(a,b); log.append(('typo',hex(p),a,b,n))
        if v101:
            for a,b in RENAMES:
                for aa,bb in ((col(a),col(b)),(a,b)):
                    n=s.count(aa)
                    if n: counts['rename '+a]=counts.get('rename '+a,0)+n; s=s.replace(aa,bb); log.append(('rename',hex(p),a,b,n))
        if v102:
            for a,b in FIXES_V102:
                n=s.count(a)
                if n: counts['v102 '+a]=counts.get('v102 '+a,0)+n; s=s.replace(a,b); log.append(('v102',hex(p),a,b,n))
        if v102 and any(p in ns for ns in NAME_SETS) and '/' not in s and '{' not in s:
            s2=center_name(s)
            if s2!=s: log.append(('v102-center',hex(p),s,s2)); counts['v102 center']=counts.get('v102 center',0)+1; s=s2
        for a,b in NAMEFIX:
            if a in s and a!='@@OLD@@': log.append(('name',hex(p),a.replace('\x01',''),'swap'))
            s=s.replace(a,b)
        if p in OGURA_UNTAGGED:
            s2='{FFFB}'.join(normalize_box(x) for x in s.split('{FFFB}'))
        else:
            cl=[]; s2=convert_message(s,speakers=CASE_SPEAKERS_V101 if v101 else CASE_SPEAKERS_V100,log=cl)
        if s2!=s: log.append(('ogura-case' if not any(x[0]=='Doppel' for x in cl) else 'doppel-case',hex(p),plain(s)[:80],plain(s2)[:80])); counts['ogura-case']=counts.get('ogura-case',0)+1
        if v101 and any(x[0]=='Doppel' for x in cl):
            # sentence-case rule capitalises after '… '; Doppel's "…I…am…/cooler…!" continues the sentence
            s2=s2.replace('…/Cooler…','…/cooler…')
        s=s2
        if cat[p]==1: s=fix_overflow(s,p,log)
        if s==old: continue
        nb=encode(s)+b'\xff\xff'
        if len(nb)<=e-p:
            d[p:p+len(nb)]=nb; d[p+len(nb):e]=b'\xff'*(e-p-len(nb))
        else:
            assert all(x==0xFF for x in d[free:free+len(nb)])
            d[free:free+len(nb)]=nb
            for o in ms[p]: struct.pack_into('<I',d,o,0x08000000+free)
            # any other aligned word pointing at p (outside the tables)?
            others=[o for o in range(0,len(d)-3,4) if struct.unpack_from('<I',d,o)[0]==0x08000000+p]
            assert not others, (hex(p),others)
            log.append(('relocated',hex(p),hex(free),len(nb)))
            free=(free+len(nb)+3)&~3
    open(out,'wb').write(d)
    if report:
        with open(report,'w') as f:
            for x in log: f.write('\t'.join(str(y).replace('\x01','').replace('\n',' ') for y in x)+'\n')
    print('counts',counts,'log',len(log),'free used',hex(free-FREE))
    return log
if __name__=='__main__':
    a=[x for x in sys.argv[1:] if x not in ('--v101','--v102')]
    v102='--v102' in sys.argv
    main(a[0],a[1],a[3] if len(a)>3 else None,v101=v102 or '--v101' in sys.argv,v102=v102)

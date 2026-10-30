import re
ALT=re.compile(r"(?=[\w']*[a-z][A-Z])(?=[\w']*[A-Z][a-z])[A-Za-z']{3,}")
PROPER={'starfy','pufftop','ogura','kragen','flychu','crabolt','moe','doppel','prophecy'}
TAG=re.compile(r'\{FFECA9\}(.*?)\{FFEB\}')
def speaker_of(tagtext): return tagtext.replace('\x01','')
def visible(s):
    """return list of (index in s, char) for visible chars; '/' kept as newline"""
    out=[];k=0
    while k<len(s):
        c=s[k]
        if c=='\x01': k+=1; continue
        if c=='{': k=s.index('}',k)+1; out.append((None,' ')); continue
        out.append((k,c)); k+=1
    return out
def normalize_box(s):
    v=visible(s); txt=''.join(c for _,c in v)
    want=list(txt)
    for m in re.finditer(r"[A-Za-z']+",txt):
        w=m.group(); lw=w.lower()
        if lw.strip("'") in PROPER: nw=lw[0].upper()+lw[1:]
        elif re.fullmatch(r"i('m|'ve|'ll|'d)?",lw): nw='I'+lw[1:]
        else: nw=lw
        pre=txt[:m.start()].rstrip(' /')
        if pre=='' or pre[-1] in '.!?' or (pre.endswith('…') and m.start()>0 and txt[m.start()-1] in ' /'):
            nw=nw[0].upper()+nw[1:]
        want[m.start():m.end()]=list(nw)
    s=list(s)
    for (k,c),w in zip(v,want):
        if k is not None: s[k]=w
    return ''.join(s)
def convert_message(s, speakers=('Ogura','???','Mysterious Voice'), log=None):
    boxes=s.split('{FFFB}'); cur=None; out=[]
    for b in boxes:
        m=TAG.search(b)
        if m: cur=speaker_of(m.group(1))
        body_start=m.end() if m else 0
        body=b[body_start:]
        vis=''.join(c for _,c in visible(body))
        if cur in speakers and len(ALT.findall(vis))>=1:
            nb=b[:body_start]+normalize_box(body)
            if log is not None: log.append((cur,vis.replace('/',' '),''.join(c for _,c in visible(nb[body_start:])).replace('/',' ')))
            b=nb
        out.append(b)
    return '{FFFB}'.join(out)

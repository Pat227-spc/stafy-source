"""Stafy 3 dialogue clipping check (estimate). Dialogue text starts at x=14; screen edge 240; the page-advance
arrow sits at x=224-230 on the last line. Splits messages into pages on speaker tags and {1a0601000101}.
Reports lines with est width > CLIP (=226-2 margin) and last-of-page lines with est > ARROW (=208)."""
import sys,os,re
sys.path.insert(0,os.path.dirname(__file__))
from bmg import BMG
from s3text import dec
import jpscan,s3width
STORY=(0xF5FD78,)  # narration renderer (x starts at 4) - checked separately
def pages(s):
    SEP=r'(\{1a..020001[0-9a-f]*\}|\{1a0601000101\})'
    parts=re.split(SEP,s)
    out=[]; cur=[]
    for p in parts:
        if re.fullmatch(SEP,p): 
            if cur: out.append(cur)
            cur=[]; continue
        for ln in p.split('/'):
            t=re.sub(r'\{[0-9a-f]+\}','',ln).replace('~',' ').replace('`','')
            if t.strip(): cur.append(t)
    if cur: out.append(cur)
    return out
def check(d,CLIP=224,ARROW=208):
    t=s3width.table(d); res=[]
    for f in jpscan.files(d):
        if f in (0xF68898,0x5A6B34) or f in STORY: continue
        for i,m in enumerate(BMG(d,f).msgs):
            s=dec(m)
            if '{1a' not in s: continue
            for pg in pages(s):
                for j,ln in enumerate(pg):
                    w=s3width.line_px(ln,t,0)
                    if w>CLIP: res.append(('CLIP',w,'%X#%d'%(f,i),ln))
                    elif j==len(pg)-1 and w>ARROW: res.append(('ARROW',w,'%X#%d'%(f,i),ln))
                if len(pg)>3: res.append(('LINES',len(pg),'%X#%d'%(f,i),' / '.join(pg)[:80]))
    return res
if __name__=='__main__':
    for r in check(open(sys.argv[1],'rb').read()): print(*r,sep='\t')

"""Leftover-Japanese scan over every live EN BMG file reached through the message table (skips only the JP dev
test file in slot 13; F68898 is scanned since v1.0.5). Prints file#msg and a snippet for every message containing kana/kanji."""
import sys,os,re,struct
sys.path.insert(0,os.path.dirname(__file__))
from bmg import BMG
from s3text import dec
JP=re.compile(r'[\u3041-\u3096\u30a1-\u30fa\u30fc\u4e00-\u9fff]')
def files(d):
    fs=[]
    for k in range(27):
        f=struct.unpack('<I',d[0x192978+4*k:0x192978+4*k+4])[0]-0x08000000
        if f not in fs: fs.append(f)
    return fs
def scan(d,skip=(0x5A6B34,)):
    out=[]
    for k,f in enumerate(files(d)):
        if f in skip: continue
        for i,m in enumerate(BMG(d,f).msgs):
            t=dec(m); 
            names=''.join(bytes.fromhex(x).decode('cp932','replace') for x in re.findall(r'\{1a..020001..((?:[0-9a-f]{4})+)\}',t))
            body=re.sub(r'\{[0-9a-f]+\}','',t)
            if JP.search(body) or JP.search(names): out.append((k,f,i,(names+' | '+body)[:110]))
    return out
if __name__=='__main__':
    for r in scan(open(sys.argv[1],'rb').read()): print('slot%02d %X#%d %s'%r)

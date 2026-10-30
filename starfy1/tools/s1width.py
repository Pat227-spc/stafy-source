import re
from s1text import encode
def table(d): return d[0x6E0034:0x6E0134]
def line_px(W,line):
    line=re.sub(r'\{FFEC..\}.*?\{FFEB\}','',line)
    b=re.sub(rb'\xff[\x00-\xff]',b'',encode(line))
    return sum(W[x]+(W[x]&1) for x in b)

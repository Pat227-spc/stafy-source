"""Approximate pixel width of Stafy 3 (Dimedime VWF) dialogue text. Width table 0xF00138 (main dialogue font);
glyph index: '0'-'9' 0x55+, 'A'-'Z' 0x110+, 'a'-'z' 0x131+. Punctuation widths calibrated from screenshots (PUNCT)."""
T0=0xF00138
PUNCT={' ':4,'.':3,',':3,"'":2,'-':5,'!':3,'?':6,':':3,'·':3,'_':4,'~':4,'(':4,')':4,'&':7,'#':7,'§':8,'*':8,'☆':12,'★':12,'♪':10,'"':5,'‐':5,'゛':5,'/':0}
def table(d): return d[T0:T0+0x160]
def cw(c,t,sp):
    if '0'<=c<='9': return t[0x55+ord(c)-48]+sp
    if 'A'<=c<='Z': return t[0x110+ord(c)-65]+sp
    if 'a'<=c<='z': return t[0x131+ord(c)-97]+sp
    return PUNCT.get(c,12)+sp
def line_px(s,t,sp=1): return sum(cw(c,t,sp) for c in s)

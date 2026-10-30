"""Stafy 3 (Dimedime) text helpers: BMG message bytes <-> editable text.
Editable form: ASCII for fullwidth Latin/punctuation, '/' newline, {1a..} escapes kept as hex, other SJIS as-is."""
import re
TOASC={'\u3000':'_','。':'.','、':',','’':"'",'‐':'-','！':'!','？':'?','：':':','・':'·'}
def dec(m):
    out=[];k=0
    while k<len(m):
        x=m[k]
        if x==0x1A: ln=m[k+1]; out.append('{'+m[k:k+ln].hex()+'}'); k+=ln; continue
        if (0x81<=x<=0x9F) or (0xE0<=x<=0xFC):
            b=m[k:k+2]
            try: ch=b.decode('cp932')
            except: ch='<%s>'%b.hex()
            o=ord(ch[0])
            if len(ch)==1 and 0xFF01<=o<=0xFF5E and ch not in '！？：': ch=chr(o-0xFEE0)
            elif ch in TOASC: ch=TOASC[ch]
            out.append(ch); k+=2; continue
        out.append('/' if x==0x0A else '~' if x==0x20 else '<%02x>'%x if x<0x20 or x>0x7e else '`'+chr(x)); k+=1
    return ''.join(out)
FROMASC={'_':'\u3000','.':'。',',':'、',"'":'’','-':'‐','!':'！','?':'？',':':'：','·':'・'}
def enc(s):
    """encode editable text: plain ASCII letters/digits -> fullwidth; ' ' and '~' -> ASCII space (game style);
    '`x' -> literal ASCII byte; {..} escape hex; '/' newline"""
    out=bytearray();k=0
    while k<len(s):
        c=s[k]
        if c=='{': j=s.index('}',k); out+=bytes.fromhex(s[k+1:j]); k=j+1; continue
        if c=='`': out.append(ord(s[k+1])); k+=2; continue
        if c=='/': out.append(0x0A)
        elif c in ' ~': out.append(0x20)
        elif c=='<': j=s.index('>',k); out+=bytes.fromhex(s[k+1:j]); k=j+1; continue
        elif c in FROMASC: out+=FROMASC[c].encode('cp932')
        elif c.isascii() and c.isalnum(): out+=chr(ord(c)+0xFEE0).encode('cp932')
        else: out+=c.encode('cp932')
        k+=1
    return bytes(out)

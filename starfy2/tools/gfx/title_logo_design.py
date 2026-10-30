#!/usr/bin/env python3
"""title_logo_design.py [key=value ...]  - DESIGN-TIME ONLY (needs the Google fonts on the box; the build does not run it).
Draws the English text layer of the title logo, "The Legendary" (Lilita One 17) over "Starfy" (Titan One 40, x0.84),
in the Japanese logo's own palette indices: yellow->orange fill ramp 79..112, blue outline 46/50/51/53/24 with a 2-px
drop at the bottom, near-black rim 125, cyan top highlights 42/63, small sparkle stars 81/83 (like JP's orange stars).
The result was saved as tools/gfx/title_logo_text.png (8-bit indices, 0 = transparent; our own art, no ROM data) with:
    title_logo_design.py big=40 by=25 small=17 sy=5
tools/gfx/title_logo.py composes it with the JP '2' and (R) mark at build time."""
import json, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage as nd
G='/usr/share/fonts/truetype/sand-box/google/'
FONT_BIG=G+'Titan One/TitanOne-Regular.ttf'
CW,CH=200,88; SS=4
args=dict(a.split('=') for a in sys.argv[1:])
big=int(args.get('big',46)); small=int(args.get('small',15)); bx=int(args.get('bx',10)); by=int(args.get('by',24)); sx=int(args.get('sx',12)); sy=int(args.get('sy',6))
FONT_SMALL=G+args.get('sf','Lilita One/LilitaOne-Regular.ttf'); xs=float(args.get('xs',0.84)); xs2=float(args.get('xs2',1.0))
def mask(text,font,size,x,y,xscale):
    f=ImageFont.truetype(font,size*SS)
    l,t,r,b=f.getbbox(text)
    im=Image.new('L',(r-l+8,b-t+8),0); ImageDraw.Draw(im).text((4-l,4-t),text,font=f,fill=255)
    im=im.resize((max(1,int(im.width*xscale)),im.height),Image.LANCZOS)
    big=Image.new('L',(CW*SS,CH*SS),0); big.paste(im,(x*SS,y*SS))
    a=np.asarray(big.resize((CW,CH),Image.BOX),dtype=float)/255
    return a>float(args.get('th',0.45))
T1=mask(args.get('t1','The Legendary'),FONT_SMALL,small,sx,sy,xs2)
T2=mask('Starfy',FONT_BIG,big,bx,by,xs)
def style(T,ow,drop,fillrows):
    out=np.zeros((CH,CW),int)
    dist=nd.distance_transform_edt(~T)
    O=(dist<=ow)
    Od=np.zeros_like(O); Od[drop:,:]=O[:-drop,:] if drop else O
    O=O|Od
    ring=O & ~nd.binary_erosion(O)
    # outline shades
    below=np.zeros_like(T); below[1:,:]=T[:-1,:]  # pixel directly below letter? (T above)
    for y in range(CH):
        for x in range(CW):
            if not O[y,x] or T[y,x]: continue
            d=dist[y,x]
            if ring[y,x]: out[y,x]=125
            elif d<=1.0: out[y,x]=46 if y<fillrows[0]+ (fillrows[1]-fillrows[0])//2 else 50
            elif d<=2.3: out[y,x]=51
            else: out[y,x]=53 if d<=ow else 24
    # top-facing highlight: outline pixels with letter 2px below and no letter above
    for y in range(1,CH-2):
        for x in range(CW):
            if out[y,x] in (46,51) and not T[y-1,x] and (T[y+1,x] or T[y+2,x]): out[y,x]=42 if out[y,x]==46 else 63
    # fill gradient
    ys=np.where(T.any(axis=1))[0]; y0,y1=ys.min(),ys.max()
    ramp=[79,81,83,86,86,87,87,90,99,98,103,112]
    edge=T & ~nd.binary_erosion(T)
    for y in range(CH):
        for x in range(CW):
            if T[y,x]:
                k=int((y-y0)/(y1-y0+1)*len(ramp)); out[y,x]=ramp[min(k,len(ramp)-1)]
                if edge[y,x] and y>0 and not T[y-1,x] and k<6: out[y,x]=79
    return out
L1=style(T1,2,1,(0,0)); L2=style(T2,4,2,(0,0))
# stars on the big word's lower band
ys=np.where(T2.any(axis=1))[0]; y0,y1=ys.min(),ys.max()
E2=nd.binary_erosion(T2,iterations=2)
rng=np.random.RandomState(3)
for x in range(0,CW,9):
    y=int(y0+(y1-y0)*0.78)+rng.randint(-2,3); x+=rng.randint(-2,3)
    if 0<x<CW-1 and E2[y,x] and E2[y-1,x] and E2[y+1,x] and E2[y,x-1] and E2[y,x+1]:
        L2[y,x]=81; L2[y-1,x]=L2[y+1,x]=L2[y,x-1]=L2[y,x+1]=83
out=L2.copy(); m=L1>0; out[m]=L1[m]
Image.fromarray(out.astype(np.uint8),'L').save(args.get('out','/tmp/title_logo_text.png'))

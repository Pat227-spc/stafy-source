"""oamview.py VRAM PAL OAM OUT.png [first last] [--idx]  - compose OBJ sprites (1D mapping, 4bpp) from dumps.
--idx draws palette indices as greys instead of colours."""
import sys, struct
from PIL import Image
SZ = {(0,0):(8,8),(0,1):(16,16),(0,2):(32,32),(0,3):(64,64),(1,0):(16,8),(1,1):(32,8),(1,2):(32,16),(1,3):(64,32),
      (2,0):(8,16),(2,1):(8,32),(2,2):(16,32),(2,3):(32,64)}
def sprites(oam, a, b):
    for i in range(a, b+1):
        a0, a1, a2 = struct.unpack_from('<HHH', oam, i*8)
        if (a0 >> 8) & 3 == 2: continue
        w, h = SZ[(a0 >> 14, a1 >> 14)]; x = a1 & 511; y = a0 & 255
        if x >= 256: x -= 512
        if y >= 160: y -= 256
        yield i, x, y, w, h, a2 & 1023, a2 >> 12, bool(a1 & 0x1000), bool(a1 & 0x2000)
def compose(vram, pal, oam, a, b, idx=False):
    im = Image.new('RGBA', (240, 160), (0, 0, 0, 0)); px = im.load(); P = []
    for i in range(256):
        c = struct.unpack_from('<H', pal, 512 + 2*i)[0]; P.append(((c & 31) << 3, (c >> 5 & 31) << 3, (c >> 10 & 31) << 3, 255))
    for i, x, y, w, h, t, p, hf, vf in reversed(list(sprites(oam, a, b))):
        for ty in range(h // 8):
            for tx in range(w // 8):
                tile = t + ty * (w // 8) + tx
                for yy in range(8):
                    for xx in range(8):
                        bb = vram[0x10000 + tile*32 + yy*4 + xx//2]; v = bb >> 4 if xx & 1 else bb & 15
                        if not v: continue
                        X = tx*8 + xx; Y = ty*8 + yy
                        if hf: X = w - 1 - X
                        if vf: Y = h - 1 - Y
                        X += x; Y += y
                        if 0 <= X < 240 and 0 <= Y < 160: px[X, Y] = (v*16, v*16, v*16, 255) if idx else P[p*16 + v]
    return im
if __name__ == '__main__':
    a = [x for x in sys.argv[1:] if not x.startswith('--')]
    v, p, o = (open(f, 'rb').read() for f in a[:3])
    first, last = (int(a[4], 0), int(a[5], 0)) if len(a) > 5 else (0, 127)
    compose(v, p, o, first, last, '--idx' in sys.argv).save(a[3])

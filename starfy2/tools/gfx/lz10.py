"""GBA LZ77 (type 0x10) decompress / compress. The compressor never emits displacement 1, so the output is also
safe for the BIOS VRAM decompressor (LZ77UnCompVram, 16-bit writes)."""
def decompress(d, o=0):
    assert d[o] == 0x10, 'not LZ10'
    n = d[o+1] | d[o+2] << 8 | d[o+3] << 16; out = bytearray(); i = o + 4
    while len(out) < n:
        f = d[i]; i += 1
        for b in range(8):
            if len(out) >= n: break
            if f & (0x80 >> b):
                x = d[i] << 8 | d[i+1]; i += 2; l = (x >> 12) + 3; off = (x & 0xFFF) + 1
                for _ in range(l): out.append(out[-off])
            else: out.append(d[i]); i += 1
    return bytes(out)
def compress(src):
    n = len(src); out = bytearray([0x10, n & 255, n >> 8 & 255, n >> 16 & 255]); i = 0
    while i < n:
        flagpos = len(out); out.append(0); flag = 0
        for b in range(8):
            if i >= n: break
            best_l = 0; best_d = 0
            for d in range(2, min(i, 0x1000) + 1):
                l = 0
                while l < 18 and i + l < n and src[i + l - d] == src[i + l]: l += 1
                if l > best_l: best_l, best_d = l, d
                if l == 18: break
            if best_l >= 3:
                flag |= 0x80 >> b; x = (best_l - 3) << 12 | (best_d - 1); out += bytes([x >> 8, x & 255]); i += best_l
            else: out.append(src[i]); i += 1
        out[flagpos] = flag
    while len(out) % 4: out.append(0)
    return bytes(out)

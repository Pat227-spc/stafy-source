.gba
; In-level conversation scripts (table 0x0814E22C) are LZ-decompressed into one heap block that each stage allocates at
; 0x080CDFF4 (movs r0,#0x80 / lsls r0,r0,#6 = 0x2000 bytes). The English 2-1 (9,890 B), 3-4 (8,745 B) and 4-5 (9,584 B)
; scripts overflow it and corrupt the heap (2-1 crashes when Ruby's flashback starts). Raise the block to 0x3000 bytes;
; the heap places later blocks after it, so no pointer changes are needed. tools/check_script_sizes.py enforces the limit.
.open "rom/output.gba",0x08000000
.org 0x080CDFF4
.thumb
.area 2
        mov     r0,#0xC0        ; lsl #6 below -> 0x3000
.endarea
.close

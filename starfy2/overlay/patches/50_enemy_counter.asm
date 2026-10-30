; 1-2 Star Spin training: the 'あと' ('... to go') word of the enemy counter -> 'LEFT' (shows "LEFT 30").
; 6 uncompressed OBJ tiles at 0x087D3E58 (16x16 + 8x16); the digits after them are kept. New pixel art from
; tools/gfx/enemy_counter.py (build time, patches/gen/).
.gba
.open "rom/output.gba",0x08000000
.org 0x087D3E58
.area 6*32
	.incbin "patches/gen/enemy_counter.bin"
.endarea
.close

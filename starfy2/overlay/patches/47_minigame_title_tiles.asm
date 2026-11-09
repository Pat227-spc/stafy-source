; Minigame menu, game 2 title ('Squeak Squeak Panic', tools/gfx/minigame_titles.py stage 2): the title is 111 px, so its
; left 8x16 sprite may no longer borrow Bomb Shower's tile 0xCD (H+V flipped, upstream layout). Repoint it to the free
; tiles 0x10E/0x12E of 1minigamemenuOBJ.bin, unflipped. Frame entry (6 bytes: y, attr0 hi, x lo, attr1 hi, tile) is
; F0 80 C8 31 CD 00 in the base ROM; x stays -56 (screen x 112).
.gba
.open "rom/output.gba",0x08000000
.org 0x0834F38C
	.byte 0xF0,0x80,0xC8,0x01
	.halfword 0x010E
.close

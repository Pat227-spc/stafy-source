.gba
; Pause menu: 'Abilities' tab label (glossary: アクション = Abilities).
; Upstream already drew the label (tiles 0x40-0x48 of asm/bin/graphics/pausemenu/2pausemenuOBJ.bin) and wrote
; OAM/5actionsignoam.bin, but left both .org lines commented out in asm/graphics.asm, so the tab showed nothing.
; Their 30-byte file has every halfword byte-swapped (it reads as invalid shape 3), so the entries are written here in
; the right order instead: 16x8 sprites at x=-36,-20,-4,12 (tiles 0x40,0x42,0x44,0x46) + 8x8 at x=28 (tile 0x48), palette 3.
; Generated from that file by hand-checked byte swap; same layout for the pop-in frame and the steady frame, like upstream's other tabs.
.open "rom/output.gba",0x08000000
.org 0x0863DE94	; pop-in animation (5 sprites)
	.halfword 0x40F4,0x01DC,0x3040
	.halfword 0x40F4,0x01EC,0x3042
	.halfword 0x40F4,0x01FC,0x3044
	.halfword 0x40F4,0x000C,0x3046
	.halfword 0x00F4,0x001C,0x3048
.org 0x0863DF46	; tab graphic (5 sprites)
	.halfword 0x40F4,0x01DC,0x3040
	.halfword 0x40F4,0x01EC,0x3042
	.halfword 0x40F4,0x01FC,0x3044
	.halfword 0x40F4,0x000C,0x3046
	.halfword 0x00F4,0x001C,0x3048
.close

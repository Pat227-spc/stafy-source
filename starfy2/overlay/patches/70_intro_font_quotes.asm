; QA round 2 / v0.9.3-test (S2-D001): VWF widths for the two glyphs added to the intro/bulk-text font (asm/VWF/1IntroFont.bin,
; overrides in overlay/glyphs/1IntroFont/): glyph 259 = ' (3 px), glyph 260 = " (6 px). The type-0 width table at 0x08FF7000
; (asm/VWF/1IntroTable.bin) is indexed by glyph number (e.g. 'I' = glyph 40 -> 3, 'A' = glyph 32 -> 9).
.gba
.open "rom/output.gba",0x08000000
.org 0x08FF7000 + 259
	.byte 3, 6
.close

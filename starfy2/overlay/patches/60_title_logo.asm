.gba
; Title logo '伝説のスタフィー2' -> "The Legendary Starfy 2" (skip with ./build.sh --no-logo).
; tools/gfx/title_logo.py (build time, ROM-derived -> patches/gen/, never committed) appends the new logo tiles to title
; BG block 1 and rewrites the BG1 map; the title loader (0x080DC7A6) reads both as offsets from archive 0x088F6B3C, so the
; two offset literals are pointed at the copies here. Same palette, 161 tiles (JP logo: 162).
; The staff roll's small OBJ logo (LZ 0x086A1B70, 3 pointers) is replaced by tools/gfx/staff_logo.py's scaled-down English logo
; (same 106 tiles, OBJ palettes 3/4 and sprite layout).
.open "rom/output.gba",0x08000000
.org 0x080DC91C
	.word TitleLogoTiles - 0x088F6B3C
.org 0x080DC92C
	.word TitleLogoMap - 0x088F6B3C
.org 0x08114838
	.word StaffLogo
.org 0x082C7EB4
	.word StaffLogo
.org 0x082C7F44
	.word StaffLogo
.org 0x09F26000
.area 0x6000
.align 4
TitleLogoTiles:
	.incbin "patches/gen/title_logo_tiles.lz"
.align 4
TitleLogoMap:
	.incbin "patches/gen/title_logo_map.lz"
.align 4
StaffLogo:
	.incbin "patches/gen/staff_logo.lz"
.endarea
.close

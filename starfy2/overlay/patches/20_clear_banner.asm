.gba
; Treasure-chest / stage-clear scene: 'クリア!!' banner -> 'CLEAR!!'.
; The banner tiles live in the LZ OBJ block at 0x088DBB78 (only pointer: 0x08121EB8). build.sh regenerates the block from
; the base ROM with tools/gfx/clear_banner.py into patches/gen/ (ROM-derived, so it is never committed) and this patch
; repoints the loader at the new copy in the patch area (0x09F00000+, checked empty by build.sh).
.open "rom/output.gba",0x08000000
.org 0x08121EB8
	.word ClearBannerEN
.org 0x09F00000
.area 0x8000
.align 4
ClearBannerEN:
	.incbin "patches/gen/clear_banner.lz"
.endarea
.close

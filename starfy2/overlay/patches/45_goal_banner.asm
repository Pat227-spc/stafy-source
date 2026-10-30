; 4-3 Shiver Race finish banner 'ゴール' -> 'GOAL'. Generated at build time by tools/gfx/goal_banner.py into
; patches/gen/ (ROM-derived, never committed) and repointed into the patch area after the shop sign.
.gba
.open "rom/output.gba",0x08000000
.org 0x082A94C4
	.word GoalBannerEN
.org 0x09F24000
.area 0x2000
.align 4
GoalBannerEN:
	.incbin "patches/gen/goal_banner.lz"
.endarea
.close

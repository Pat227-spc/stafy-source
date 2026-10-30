; 1-3 Lovely's Shop: the building's banner 'ラブリーのおみせ' -> "LOVELY'S SHOP" (two lines).
; OBJ sheet LZ block 0x087DD44C (only pointer 0x082A7DE4) is regenerated from the base ROM at build time by
; tools/gfx/shop_sign.py into patches/gen/ (ROM-derived, never committed) and repointed into the patch area.
.gba
.open "rom/output.gba",0x08000000
.org 0x082A7DE4
	.word ShopSignEN
.org 0x09F20000
.area 0x4000
.align 4
ShopSignEN:
	.incbin "patches/gen/shop_sign.lz"
.endarea
.close

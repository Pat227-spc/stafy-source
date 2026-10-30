.gba
; Title screen prompt 'スタートボタンを おしてね!' -> 'PRESS START!' (see tools/gfx/title_prompt.py).
; Inputs are generated from the base ROM at build time into patches/gen/ (never committed).
.open "rom/output.gba",0x08000000
.org 0x080DC924	; title loader literal: OBJ sheet offset from the title archive base 0x088F6B3C (was 0xBE10)
	.word TitleObjEN - 0x088F6B3C
.org 0x08957194	; prompt animation: 20 frames x 82 bytes, same size as the original, rewritten in place
	.incbin "patches/gen/title_frames.bin"
.org 0x09F10000
.area 0x10000
.align 4
TitleObjEN:
	.incbin "patches/gen/title_obj.lz"
.endarea
.close

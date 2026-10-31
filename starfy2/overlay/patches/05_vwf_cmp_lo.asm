.gba
; VWF width lookup (VWF.bps code at 0x08FF6F38): the bounds check at 0x08FF6F72 is encoded as 0x4501, i.e. the
; hi-register CMP form (THUMB format 5) with H1=H2=0. ARMv7TDMI docs call that UNPREDICTABLE; VBA-M swaps the
; operands there, the width lookup then always fails (fixed 13 px text, overflow, heap corruption, World 3/4 hang).
; Re-encode the same instruction in the low-register form (format 4): cmp r1,r0 = 0x4281. Identical flags/semantics.
; (Found by the second-emulator pass, QA round 2.) Audit: no other format-5 ADD/CMP/MOV with H1=H2=0 in code we add.
.open "rom/output.gba",0x08000000
.if readu16("rom/output.gba", 0xFF6F72) != 0x4501
  .error "unexpected bytes at 0x08FF6F72 (expected 0x4501 from VWF.bps)"
.endif
.org 0x08FF6F72
	cmp r1,r0		; armips emits the low-register form 0x4281
.close

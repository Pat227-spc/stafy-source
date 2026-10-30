.gba
; Pause menu tab pop-in: put upstream's Hints/Stuff/Rides pop-in labels at the first sprite of each group, not one entry late
; (removes a one-frame stray box left of the label). The include is generated from the base ROM at build time by
; tools/gfx/pause_popin_fix.py (it restores the JP sprite entry that upstream's write clobbered).
.open "rom/output.gba",0x08000000
.include "patches/gen/pause_popin_fix.asm"
.close

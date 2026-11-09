#!/usr/bin/env bash
# Env: STRICT_ATLAS=1 (default) fail on any Atlas parse/insert error; STRICT_ATLAS=0 = warn and continue like assemble.bat
#      BUILD=dir scratch dir (default ./build), REPO=dir (default ./upstream)
#      OVERLAY_JOBS=N parallel Atlas+lzss for overlay scenes (default: nproc)
# Linux equivalent of upstream/assemble.bat (Densetsu no Stafy 2 EN fan translation).
# usage: ./build.sh [--dummy-ok] [--no-overlay] [--no-gfx] [--no-logo] [--rom16] BASE_ROM.gba [OUT_BPS]
#   --rom16 builds the optional 16 MiB variant (same content, nothing above 0x08FFFFFF, 0xFF padding; see tools/rom16.py)
#   --no-logo keeps the Japanese title logo (skips overlay/patches/60_title_logo.asm)
#   Graphics: upstream asm/graphics.asm (normally a separate outputGFX.gba build) is merged, block moved to 0x09200000.
#   Overlays: backfill/scripts/ (mirrors asm/bin/text/) then overlay/ (mirrors the repo root) are copied over the
#   scratch tree when they exist. New scene .txt files get import.bin reset + Atlas + lzss and are linked via
#   //POINTER: headers or scenes.tsv (see tools/overlay.py). Upstream files are never edited.
#   BASE_ROM must be the clean Japanese ROM (16 MiB, CRC32 EA73EB54). It is only read.
#   Builds in ./build/ (a scratch copy of the repo tree); upstream/ is never modified.
#   Emits out/stafy2_en.bps (default) via native flips.
#   --dummy-ok: allow a non-matching base ROM (tool smoke tests); VWF.bps is then applied
#               with --ignore-checksum and the result is NOT a valid patch.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="${REPO:-$HERE/upstream}"
TOOLS="$HERE/tools"
BUILD="${BUILD:-$HERE/build}"
# optional tools/env.sh: WINE_BIN (wine not on PATH), WINEPREFIX, wine warm-up
# shellcheck source=/dev/null
[[ -f "$TOOLS/env.sh" ]] && source "$TOOLS/env.sh"
STRICT_ATLAS="${STRICT_ATLAS:-1}"
OVERLAY_JOBS="${OVERLAY_JOBS:-$(nproc 2>/dev/null || echo 8)}"
EXPECT_CRC=EA73EB54
DUMMY=0; OVERLAY=1; LOGO=1; ROM16=0; GFX=${GFX:-1}   # graphics merge on by default (--no-gfx to disable)
GFX_BASE=0x09200000   # upstream graphics.asm uses 0x09000000, which collides with the uncompressed text
while [[ "${1:-}" == --* ]]; do case "$1" in
  --dummy-ok) DUMMY=1;; --no-overlay) OVERLAY=0;; --gfx) GFX=1;; --no-gfx) GFX=0;; --no-logo) LOGO=0;; --rom16) ROM16=1;; *) echo "unknown option $1" >&2; exit 1;; esac; shift; done
# Overlays (on by default when the dir exists; later wins): "SRC:DEST-PREFIX-IN-TREE"
OVERLAY_SPECS=("$HERE/backfill/scripts:asm/bin/text" "$HERE/overlay:." ${OVERLAY_EXTRA:-})   # OVERLAY_EXTRA="dir:prefix ..." for experiments
OVL_BASE=0x09400000; OVL_END=0x09E40000   # free expansion space (uncompressed text ends ~0x09019000, VWF minifont at 0x09E5D98C)
GFX_AREA=0x00200000; FREE=0; PATCH_LO=0x1F00000; PATCH_HI=0x2000000   # free space byte: 0x00 (appended padding)
if [[ $ROM16 == 1 ]]; then   # 16 MiB variant: the same blocks in the original image's 0xFF free space (layout table: tools/rom16.py)
  GFX_BASE=0x08C80000; GFX_AREA=0x00080000; OVL_BASE=0x08D00000; OVL_END=0x08E40000; FREE=255; PATCH_LO=0xF00000; PATCH_HI=0xF80000; fi
BASE="${1:?usage: build.sh [--dummy-ok] BASE_ROM [OUT_BPS]}"
OUT="${2:-$HERE/out/stafy2_en.bps}"
# Windows (Git Bash / MSYS2): run the .exe tools natively; elsewhere run Atlas.exe/lzss.exe under wine.
case "$(uname -s)" in MINGW*|MSYS*|CYGWIN*) WINE=(); EXE=.exe;; *) WINE=(wine); EXE=;; esac
export STAFY_WINE="${WINE[*]-}"   # plain string for the parallel overlay workers (arrays are not exported)
ARMIPS="$TOOLS/bin/armips$EXE"; FLIPS="$TOOLS/bin/flips$EXE"
# Third-party tools are not bundled; see tools/README.md. Atlas.exe and lzss.exe run under wine.
for x in "$ARMIPS" "$FLIPS" "$TOOLS/bin/Atlas.exe" "$TOOLS/bin/lzss.exe"; do
  [[ -f "$x" ]] || { echo "missing tool: $x (see tools/README.md)" >&2; exit 1; }; done
export WINEPREFIX="${WINEPREFIX:-$TOOLS/wineprefix}" WINEDEBUG="${WINEDEBUG:--all}" WINEDLLOVERRIDES="${WINEDLLOVERRIDES:-mscoree,mshtml=;winedbg.exe=d}"
LOG="$BUILD/build.log"
step(){ echo "== $*" | tee -a "$LOG"; }
die(){ echo "BUILD FAILED: $*" | tee -a "$LOG" >&2; exit 1; }
crc(){ python3 -c 'import zlib,sys;print("%08X"%(zlib.crc32(open(sys.argv[1],"rb").read())&0xffffffff))' "$1"; }

[[ -f "$BASE" ]] || { echo "base ROM not found: $BASE" >&2; exit 1; }
BASE="$(realpath "$BASE")"; mkdir -p "$(dirname "$OUT")"; OUT="$(realpath -m "$OUT")"; BUILD="$(realpath -m "$BUILD")"; LOG="$BUILD/build.log"
rm -f "$OUT"   # no stale patch if this build FAILs
rm -rf "$BUILD"; mkdir -p "$BUILD" "$(dirname "$OUT")"; : > "$LOG"
step "base ROM check"
SIZE=$(stat -c %s "$BASE"); BCRC=$(crc "$BASE")
echo "base: $BASE size=$SIZE crc32=$BCRC (expected 16777216 / $EXPECT_CRC)" | tee -a "$LOG"
if [[ "$SIZE" != 16777216 || "$BCRC" != "$EXPECT_CRC" ]]; then
  [[ $DUMMY == 1 ]] || die "base ROM does not match VWF.bps source (need clean 'Densetsu no Stafy 2 (Japan)' CRC32 $EXPECT_CRC)"
  echo "WARNING: --dummy-ok, continuing with non-matching base" | tee -a "$LOG"
fi

step "copy repo tree to scratch (no .git, no ROMs/tmp/padding)"
T="$BUILD/tree"; mkdir -p "$T"
tar -C "$REPO" --exclude=.git --exclude='*.gba' --exclude='*.tmp' --exclude='rom/padding.bin' \
    --exclude='*.sav' --exclude='*.ss[0-9]' --exclude='*.sa[0-9]' -cf - . | tar -C "$T" -xf -
cp "$TOOLS/bin/Atlas.exe" "$TOOLS/bin/lzss.exe" "$T/"
if [[ $OVERLAY == 1 ]]; then
  step "overlays"
  specs=(); for sp in "${OVERLAY_SPECS[@]}"; do [[ -d "${sp%:*}" ]] && specs+=("$sp") && echo "  using ${sp%:*}" | tee -a "$LOG"; done
  python3 "$TOOLS/overlay.py" "$T" "$REPO/assemble.bat" "$BUILD/overlay_manifest.tsv" "${specs[@]}" | tee -a "$LOG"
  # glyph overrides (overlay/glyphs/<Font>/<index>.txt) patch the scratch copy of asm/VWF/<Font>.bin
  python3 "$TOOLS/glyphs.py" "$T" "$HERE/overlay/glyphs" | tee -a "$LOG"
else : > "$BUILD/overlay_manifest.tsv"; fi
mkdir -p "$T/rom"
cp "$BASE" "$T/rom/output.gba"; chmod u+w "$T/rom/output.gba"   # = copy input.gba output.gba
cd "$T"

step "normalize TBL/TXT to CRLF (upstream .gitattributes text=auto => Windows checkout is CRLF; Atlas needs CRLF TBLs)"
python3 - <<'PY'
import os
n=0
for root,_,files in os.walk('.'):
    for f in files:
        if f.lower().endswith(('.tbl','.txt')):
            p=os.path.join(root,f); d=open(p,'rb').read()
            c=d.replace(b'\r\n',b'\n').replace(b'\n',b'\r\n')
            if c!=d: open(p,'wb').write(c); n+=1
print(f"{n} files converted")
PY
[[ ${#WINE[@]} == 0 ]] || wineserver -p 120 2>/dev/null || true   # keep one wineserver alive: ~10x faster per-call startup

step "flips --apply asm/VWF/VWF.bps rom/output.gba (native flips)"
IGN=(); [[ $DUMMY == 1 && "$BCRC" != "$EXPECT_CRC" ]] && IGN=(--ignore-checksum)
"$FLIPS" --apply "${IGN[@]}" asm/VWF/VWF.bps rom/output.gba rom/output.vwf.gba 2>&1 | tee -a "$LOG"
[[ -f rom/output.vwf.gba ]] || die "VWF.bps apply failed (needs the clean base ROM)"
mv rom/output.vwf.gba rom/output.gba
echo "after VWF.bps: crc32=$(crc rom/output.gba) (BPS target 2B7B63B8)" | tee -a "$LOG"

if [[ $ROM16 == 1 ]]; then step "rom16: 16 MiB variant, no padding appended"; python3 "$TOOLS/rom16.py" prep "$T" 2>&1 | tee -a "$LOG"; [[ ${PIPESTATUS[0]} == 0 ]] || die "rom16 prep failed"
else
step "append 16 MiB padding (upstream padding.bin is all 0x00) -> 32 MiB"
truncate -s 33554432 rom/output.gba
fi

step "parse assemble.bat"
python3 "$TOOLS/batsteps.py" "$T" "$REPO/assemble.bat" > "$BUILD/steps.pass1.tsv" 2>/dev/null || true
step "copy import.bin over text .bin targets"
n=0; while IFS=$'\t' read -r op a; do [[ $op == import ]] || continue
  mkdir -p "$(dirname "$a")"; cp asm/bin/text/import.bin "$a"; n=$((n+1)); done < "$BUILD/steps.pass1.tsv"
echo "$n files reset from import.bin" | tee -a "$LOG"

step "concatenate uncompressed blocks (copy FIRST\\FIRST.txt+*.txt Uncompressed_Text.txt)"
UB=asm/bin/text/Uncompressed/Blocks
python3 - "$UB" <<'PY'
import os,sys
d=sys.argv[1]
names=sorted([f for f in os.listdir(d) if f.lower().endswith('.txt') and os.path.isfile(os.path.join(d,f)) and f.lower()!='uncompressed_text.txt'],key=str.upper)
with open(os.path.join(d,'..','Uncompressed_Text.txt'),'wb') as o:
    for f in [os.path.join('FIRST','FIRST.txt')]+names:
        o.write(open(os.path.join(d,f),'rb').read())
print(f"FIRST.txt + {len(names)} blocks")
PY
python3 "$TOOLS/batsteps.py" "$T" "$REPO/assemble.bat" > "$BUILD/steps.tsv" 2>>"$LOG"
grep -E 'MISSING|NOFILES|UNHANDLED' "$LOG" && echo "WARNING: see above (assemble.bat refs not found)" || true

step "Atlas (Atlas.exe) - $(grep -c ^atlas "$BUILD/steps.tsv") scripts"
fail=0
while IFS=$'\t' read -r op a b; do [[ $op == atlas ]] || continue
  out=$(timeout 120 "${WINE[@]}" ./Atlas.exe </dev/null "$(echo "$a" | tr / '\\')" "$(echo "$b" | tr / '\\')" 2>&1 | tr -d '\r') || true
  echo "--- Atlas $a $b"$'\n'"$out" >> "$BUILD/atlas.log"
  if ! grep -q "Insertion - 0 error(s)" <<<"$out" || ! grep -q "Parsing - 0 error(s)" <<<"$out"; then
    echo "ATLAS PROBLEM: $a <- $b"; { echo "$out" | grep -a -m5 '^Error\|^Warning\|exception\| [1-9][0-9]* error' || true; }; fi
done < "$BUILD/steps.tsv" | tee -a "$LOG"
fail=$(grep -c '^ATLAS PROBLEM' "$LOG" || true)
echo "Atlas problems: $fail (full output in build/atlas.log)" | tee -a "$LOG"
# Default STRICT_ATLAS=1: any parse/insert failure fails the build (no .bps written).
# STRICT_ATLAS=0 keeps assemble.bat's warn-and-continue behaviour.
[[ $fail == 0 ]] || [[ "$STRICT_ATLAS" != 1 ]] || die "Atlas errors (STRICT_ATLAS=1; $fail problem(s); see build/atlas.log)"
if [[ $ROM16 == 1 ]]; then python3 "$TOOLS/rom16.py" snap rom/output.gba "$BUILD/rom16_text.bin" 2>&1 | tee -a "$LOG"; [[ ${PIPESTATUS[0]} == 0 ]] || die "rom16 text check failed"; fi

step "lzss -ewo (lzss.exe, CUE 2011)"
while IFS=$'\t' read -r op rest; do [[ $op == lzss ]] || continue
  IFS=$'\t' read -r -a files <<<"$rest"
  wpaths=(); for f in "${files[@]}"; do wpaths+=("$(echo "$f" | tr / '\\')"); done
  timeout 300 "${WINE[@]}" ./lzss.exe -ewo "${wpaths[@]}" </dev/null 2>&1 | tr -d '\r' >> "$BUILD/lzss.log" || die "lzss failed on $rest"
done < "$BUILD/steps.tsv"
echo "lzss done: $(grep -c ^lzss "$BUILD/steps.tsv") invocations (build/lzss.log)" | tee -a "$LOG"

step "overlay scenes (new .txt files): import.bin reset, Atlas, lzss, link (parallel x$OVERLAY_JOBS)"
OVL_ASM="$T/asm/overlay_scenes.asm"
{ echo '.gba'; echo '.open "rom/output.gba",0x08000000'; echo ".org $OVL_BASE"; echo ".area $OVL_END-$OVL_BASE"; } > "$OVL_ASM"
# Work list: nsc, rel, src, ptrs (nsc = 1-based scene order for stable labels)
: > "$BUILD/ovl_work.tsv"; nsc=0
while IFS=$'\t' read -r kind rel src ptrs; do [[ $kind == scene ]] || continue
  nsc=$((nsc+1)); printf '%d\t%s\t%s\t%s\n' "$nsc" "$rel" "$src" "$ptrs" >> "$BUILD/ovl_work.tsv"
done < "$BUILD/overlay_manifest.tsv"
mkdir -p "$BUILD/ovl_status"
# One scene = import.bin + Atlas + lzss. Writes status file; safe under xargs -P (distinct bins).
ovl_one() {
  local nsc=$1 rel=$2 src=$3 ptrs=$4
  local bin="${rel%.*}.ovl.bin" st="$BUILD/ovl_status/$nsc.status"
  cp asm/bin/text/import.bin "$bin" || { echo FAIL > "$st"; echo "OVERLAY ATLAS FAIL: $src (import.bin)"; return 0; }
  local out
  out=$(timeout 120 $STAFY_WINE ./Atlas.exe </dev/null "$(echo "$bin" | tr / '\\')" "$(echo "$rel" | tr / '\\')" 2>&1 | tr -d '\r') || true
  { echo "--- Atlas(overlay) $bin $rel"; echo "$out"; } >> "$BUILD/atlas.log.$nsc"
  if ! grep -q "Insertion - 0 error(s)" <<<"$out" || ! grep -q "Parsing - 0 error(s)" <<<"$out"; then
    echo FAIL > "$st"
    echo "OVERLAY ATLAS FAIL: $src"
    echo "$out" | grep -a -m5 '^Error\|^Warning\|exception' || true
    return 0
  fi
  if ! timeout 120 $STAFY_WINE ./lzss.exe -ewo "$(echo "$bin" | tr / '\\')" </dev/null 2>&1 | tr -d '\r' >> "$BUILD/lzss.log.$nsc"; then
    echo FAIL > "$st"; echo "OVERLAY LZSS FAIL: $src"; return 0
  fi
  if [[ -z "$ptrs" ]]; then echo NOPTR > "$st"; echo "OVERLAY NO POINTER (built, not linked): $src"; return 0; fi
  echo OK > "$st"
}
export -f ovl_one
export BUILD
if [[ $nsc -gt 0 ]]; then
  # Parallel workers: each line is nsc<TAB>rel<TAB>src<TAB>ptrs
  xargs -P "$OVERLAY_JOBS" -a "$BUILD/ovl_work.tsv" -d '\n' -I{} bash -c '
    IFS=$'\''\t'\'' read -r nsc rel src ptrs <<<"$1"
    ovl_one "$nsc" "$rel" "$src" "$ptrs"
  ' _ {}
  for i in $(seq 1 "$nsc"); do
    [[ -f "$BUILD/atlas.log.$i" ]] && cat "$BUILD/atlas.log.$i" >> "$BUILD/atlas.log" && rm -f "$BUILD/atlas.log.$i"
    [[ -f "$BUILD/lzss.log.$i" ]] && cat "$BUILD/lzss.log.$i" >> "$BUILD/lzss.log" && rm -f "$BUILD/lzss.log.$i"
  done
fi
# Serial link: emit .incbin labels in scene order, then pointer section
ovl_fail=0; ovl_noptr=0; ovl_ok=0
while IFS=$'\t' read -r i rel src ptrs; do
  st=$(cat "$BUILD/ovl_status/$i.status" 2>/dev/null || echo FAIL)
  bin="${rel%.*}.ovl.bin"
  case "$st" in
    OK)
      ovl_ok=$((ovl_ok+1)); lab="OVL_$i"
      { echo ".align 4"; echo "$lab:"; echo "	.incbin \"$bin\""; } >> "$OVL_ASM"
      ;;
    NOPTR) ovl_noptr=$((ovl_noptr+1)); echo "OVERLAY NO POINTER (built, not linked): $src" | tee -a "$LOG";;
    *) ovl_fail=$((ovl_fail+1)); echo "OVERLAY ATLAS FAIL: $src" | tee -a "$LOG";;
  esac
done < "$BUILD/ovl_work.tsv"
echo ".endarea" >> "$OVL_ASM"
echo "overlay scenes: ok=$ovl_ok fail=$ovl_fail noptr=$ovl_noptr (of $nsc)" | tee -a "$LOG"
[[ $ovl_fail == 0 ]] || [[ "$STRICT_ATLAS" != 1 ]] || die "overlay Atlas/lzss errors (STRICT_ATLAS=1; $ovl_fail fail(s))"
python3 - "$OVL_ASM" "$BUILD/overlay_manifest.tsv" "$LOG" "$BASE" "$T/asm/script.asm" <<'PY'
# write pointer section: map each linked bin to its label; sanity-check every pointer against the base ROM
import sys,re,struct
asm,man,log,base,sasm=sys.argv[1:6]; a=open(asm).read(); lg=open(log,encoding='latin-1').read()
rom=open(base,'rb').read(); upstream=set(int(x,16) for x in re.findall(r'(?im)^\s*\.org\s+0x([0-9a-f]+)',open(sasm,encoding='latin-1').read()))
seen={}
def okptr(p,rel):
    o=p-0x08000000
    if not (0<=o<len(rom)-4) or o%4: print('OVERLAY BAD POINTER %s (%s): outside ROM/unaligned'%(hex(p),rel)); return False
    v=struct.unpack_from('<I',rom,o)[0]
    if not (0x08000000<=v<0x09000000) or rom[v-0x08000000]!=0x10:
        print('OVERLAY BAD POINTER %s (%s): base ROM word there is %08X, not a pointer to an LZ block'%(hex(p),rel,v)); return False
    if p in upstream: print('OVERLAY NOTE: %s (%s) overrides a pointer script.asm already sets'%(hex(p),rel))
    if p in seen: print('OVERLAY DUPLICATE POINTER %s: %s and %s (last wins)'%(hex(p),seen[p],rel))
    seen[p]=rel; return True
lab={m.group(2):m.group(1) for m in re.finditer(r'(OVL_\d+):\n\t\.incbin "([^"]+)"',a)}
out=[]
for l in open(man):
    k,rel,src,ptrs=(l.rstrip('\n').split('\t')+['']*4)[:4]
    b=rel.rsplit('.',1)[0]+'.ovl.bin'
    if k=='scene' and ptrs and b in lab:
        for p in ptrs.split():
            if okptr(int(p,16),rel): out.append('.org %s\n\t.word %s ; %s'%(p,lab[b],rel))
a=a.replace('.endarea\n','.endarea\n\n; pointers (override script.asm)\n'+'\n'.join(out)+'\n.close\n',1)
open(asm,'w').write(a)
n=len(lab); print('overlay scenes linked: %d, pointer writes: %d, Atlas failures: %d, no-pointer: %d'%(n,len(out),lg.count('OVERLAY ATLAS FAIL'),lg.count('OVERLAY NO POINTER')))
PY
step "armips (native v0.11): quote bare .incbin paths in scratch copies (bundled armips.exe is v0.7c 2010, which allowed them)"
python3 - <<'PY'
import re,glob
for f in ['asm/VWF/VWF.asm','asm/script.asm','asm/graphics.asm']:
    try: s=open(f,'rb').read().decode('latin-1')
    except FileNotFoundError: continue
    n=re.subn(r'(?im)^(\s*\.incbin\s+)(?!")([^\s;]+)',r'\1"\2"',s)
    open(f,'wb').write(n[0].encode('latin-1')); print(f, n[1], "incbin paths quoted")
PY
while IFS=$'\t' read -r op a; do [[ $op == armips ]] || continue
  echo "armips $a" | tee -a "$LOG"
  "$ARMIPS" -root "$T" "$a" 2>&1 | tee -a "$LOG"; [[ ${PIPESTATUS[0]} == 0 ]] || die "armips $a failed"
done < "$BUILD/steps.tsv"
if [[ $GFX == 1 ]]; then
  step "graphics (upstream asm/graphics.asm merged: outputGFX.gba -> output.gba, block relocated to $GFX_BASE)"
  python3 "$TOOLS/gfx_prep.py" "$T" "$GFX_BASE" "$GFX_AREA" 2>&1 | tee -a "$LOG"; [[ ${PIPESTATUS[0]} == 0 ]] || die "graphics merge check failed"
  python3 -c "import sys;d=open('rom/output.gba','rb').read();a=$GFX_BASE-0x08000000;sys.exit(0 if d[a:a+$GFX_AREA].count($FREE)==$GFX_AREA else 'gfx space not free')"
  "$ARMIPS" -root "$T" asm/graphics_merged.asm 2>&1 | tee -a "$LOG"; [[ ${PIPESTATUS[0]} == 0 ]] || die "armips graphics failed"
fi
if grep -q '^OVL_' "$OVL_ASM"; then
  python3 -c "import sys;d=open('rom/output.gba','rb').read();a=$OVL_BASE-0x08000000;b=$OVL_END-0x08000000;sys.exit(0 if d[a:b].count($FREE)==b-a else 'overlay space not free')"
  echo "armips asm/overlay_scenes.asm" | tee -a "$LOG"
  "$ARMIPS" -root "$T" asm/overlay_scenes.asm 2>&1 | tee -a "$LOG"; [[ ${PIPESTATUS[0]} == 0 ]] || die "armips overlay_scenes.asm failed"
fi

# overlay/patches/*.asm: small armips patches of our own (fixes to upstream data we must not edit in upstream/), applied last
if [[ $OVERLAY == 1 ]] && compgen -G "$HERE/overlay/patches/*.asm" > /dev/null; then
  step "overlay patches (overlay/patches/*.asm)"
  # generated inputs (built from the base ROM each time, never committed): patches/gen/
  mkdir -p "$T/patches/gen"
  python3 "$HERE/tools/gfx/clear_banner.py" "$BASE" "$T/patches/gen/clear_banner.lz" 2>&1 | tee -a "$LOG"; [[ ${PIPESTATUS[0]} == 0 ]] || die "clear_banner.py failed"
  python3 "$HERE/tools/gfx/title_prompt.py" "$BASE" "$T/patches/gen" 2>&1 | tee -a "$LOG"; [[ ${PIPESTATUS[0]} == 0 ]] || die "title_prompt.py failed"
  python3 "$HERE/tools/gfx/shop_sign.py" "$BASE" "$T/patches/gen/shop_sign.lz" 2>&1 | tee -a "$LOG"; [[ ${PIPESTATUS[0]} == 0 ]] || die "shop_sign.py failed"
  python3 "$HERE/tools/gfx/goal_banner.py" "$BASE" "$T/patches/gen/goal_banner.lz" 2>&1 | tee -a "$LOG"; [[ ${PIPESTATUS[0]} == 0 ]] || die "goal_banner.py failed"
  if [[ $LOGO == 1 ]]; then python3 "$HERE/tools/gfx/title_logo.py" "$BASE" "$T/patches/gen" 2>&1 | tee -a "$LOG"; [[ ${PIPESTATUS[0]} == 0 ]] || die "title_logo.py failed"
    python3 "$HERE/tools/gfx/staff_logo.py" "$BASE" "$T/patches/gen/staff_logo.lz" 2>&1 | tee -a "$LOG"; [[ ${PIPESTATUS[0]} == 0 ]] || die "staff_logo.py failed"; fi
  python3 "$HERE/tools/gfx/enemy_counter.py" "$T/patches/gen/enemy_counter.bin" > /dev/null || die "enemy_counter.py failed"
  python3 "$HERE/tools/gfx/pause_popin_fix.py" "$BASE" "$T/patches/gen/pause_popin_fix.asm" 2>&1 | tee -a "$LOG"; [[ ${PIPESTATUS[0]} == 0 ]] || die "pause_popin_fix.py failed"
  python3 -c "import sys;d=open('rom/output.gba','rb').read();sys.exit(0 if d[$PATCH_LO:$PATCH_HI].count($FREE)==$PATCH_HI-$PATCH_LO else 'patch area not free')" || die "patch area not free"
  for pf in "$HERE"/overlay/patches/*.asm; do
    if [[ $LOGO == 0 && "$(basename "$pf")" == 60_title_logo.asm ]]; then echo "skip patches/60_title_logo.asm (--no-logo)" | tee -a "$LOG"; continue; fi
    echo "armips patches/$(basename "$pf")" | tee -a "$LOG"
    "$ARMIPS" -root "$T" "patches/$(basename "$pf")" 2>&1 | tee -a "$LOG"; [[ ${PIPESTATUS[0]} == 0 ]] || die "armips $(basename "$pf") failed"
  done
fi

step "script size check (tools/check_script_sizes.py: every in-level script must fit the chat buffer, 0x100 margin)"
python3 "$TOOLS/check_script_sizes.py" rom/output.gba --margin 0x100 2>&1 | tee -a "$LOG"; [[ ${PIPESTATUS[0]} == 0 ]] || die "script size check failed"
if [[ $ROM16 == 1 ]]; then step "rom16 final check"; python3 "$TOOLS/rom16.py" final "$BASE" rom/output.gba "$BUILD/rom16_text.bin" 2>&1 | tee -a "$LOG"; [[ ${PIPESTATUS[0]} == 0 ]] || die "rom16 final check failed"; fi
fail=${fail:-0}; ovl_fail=${ovl_fail:-0}
step "create BPS"
cp rom/output.gba "$BUILD/stafy2_en.gba"
echo "patched ROM: $BUILD/stafy2_en.gba size=$(stat -c %s "$BUILD/stafy2_en.gba") crc32=$(crc "$BUILD/stafy2_en.gba")" | tee -a "$LOG"
rm -f "$OUT"
"$FLIPS" --create --bps-delta "$BASE" "$BUILD/stafy2_en.gba" "$OUT" 2>&1 | tee -a "$LOG"
[[ -s "$OUT" ]] || die "flips --create failed"
echo "BUILD OK crc=$(crc "$BUILD/stafy2_en.gba") bps=$(stat -c %s "$OUT") atlas_problems=$fail overlay_fail=$ovl_fail STRICT_ATLAS=$STRICT_ATLAS" | tee -a "$LOG"
echo "OK: $OUT ($(stat -c %s "$OUT") bytes)" | tee -a "$LOG"

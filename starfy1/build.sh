#!/usr/bin/env bash
# Build the Starfy 1 English cleanup patch.
# usage: ./build.sh [ALT_BASE.gba] [JP_BASE.gba]
#   ALT_BASE (default base/alt_base.gba): Starfy Translation Team v1.1 English ROM, CRC32 F7CB8EE3
#   JP_BASE  (default base/jp_base.gba, optional): Densetsu no Stafy (Japan), CRC32 FAE94C8B
# Output: out/Starfy 1 Eng v1.0.4.gba (patched ROM, CRC32 A78A3D9C), out/Starfy 1 Eng v1.0.4 (alt base).bps, and out/Starfy 1 Eng v1.0.4.bps if JP_BASE exists.
# Steps: build_s1.py --v103 (v1.0.3, CRC32 44C2017A), then names_s1.py (cross-game names, v1.0.4).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"; cd "$HERE"
case "$(uname -s)" in MINGW*|MSYS*|CYGWIN*) FLIPS=tools/bin/flips.exe;; *) FLIPS=tools/bin/flips;; esac
PY="${PYTHON:-python3}"
ALT="${1:-base/alt_base.gba}"; JP="${2:-base/jp_base.gba}"
crc(){ "$PY" -c 'import zlib,sys;print("%08X"%(zlib.crc32(open(sys.argv[1],"rb").read())&0xffffffff))' "$1"; }
[[ -f "$ALT" ]] || { echo "place the Starfy Translation Team v1.1 English ROM at $ALT (CRC32 F7CB8EE3)" >&2; exit 1; }
[[ $(crc "$ALT") == F7CB8EE3 ]] || { echo "wrong base: $ALT is not CRC32 F7CB8EE3" >&2; exit 1; }
mkdir -p out
"$PY" tools/build_s1.py "$ALT" "out/v103.gba" --v103 > out/build.log
C=$(crc "out/v103.gba"); echo "v1.0.3 stage: CRC32 $C (expected 44C2017A)"
[[ $C == 44C2017A ]] || { echo "v1.0.3 stage differs from the release; names_s1.py needs the exact v1.0.3 ROM" >&2; exit 1; }
"$PY" tools/names_s1.py "out/v103.gba" "out/Starfy 1 Eng v1.0.4.gba" --log out/names.tsv >> out/build.log
rm -f out/v103.gba
C=$(crc "out/Starfy 1 Eng v1.0.4.gba"); echo "patched ROM: out/Starfy 1 Eng v1.0.4.gba CRC32 $C (expected A78A3D9C)"
[[ $C == A78A3D9C ]] || echo "NOTE: CRC differs from the test build (expected if you edited the text)"
rm -f "out/Starfy 1 Eng v1.0.4 (alt base).bps" "out/Starfy 1 Eng v1.0.4.bps"
"$FLIPS" --create --bps-delta "$ALT" "out/Starfy 1 Eng v1.0.4.gba" "out/Starfy 1 Eng v1.0.4 (alt base).bps"
if [[ -f "$JP" ]]; then
  [[ $(crc "$JP") == FAE94C8B ]] || { echo "wrong JP base: $JP is not CRC32 FAE94C8B" >&2; exit 1; }
  "$FLIPS" --create --bps-delta "$JP" "out/Starfy 1 Eng v1.0.4.gba" "out/Starfy 1 Eng v1.0.4.bps"
fi
ls -l out/*.bps

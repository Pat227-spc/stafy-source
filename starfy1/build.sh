#!/usr/bin/env bash
# Build the Starfy 1 English cleanup patch.
# usage: ./build.sh [ALT_BASE.gba] [JP_BASE.gba]
#   ALT_BASE (default base/alt_base.gba): Starfy Translation Team v1.1 English ROM, CRC32 F7CB8EE3
#   JP_BASE  (default base/jp_base.gba, optional): Densetsu no Stafy (Japan), CRC32 FAE94C8B
# Output: out/Starfy 1 Eng v1.0.3.gba (patched ROM, CRC32 44C2017A), out/Starfy 1 Eng v1.0.3 (alt base).bps, and out/Starfy 1 Eng v1.0.3.bps if JP_BASE exists.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"; cd "$HERE"
case "$(uname -s)" in MINGW*|MSYS*|CYGWIN*) FLIPS=tools/bin/flips.exe;; *) FLIPS=tools/bin/flips;; esac
PY="${PYTHON:-python3}"
ALT="${1:-base/alt_base.gba}"; JP="${2:-base/jp_base.gba}"
crc(){ "$PY" -c 'import zlib,sys;print("%08X"%(zlib.crc32(open(sys.argv[1],"rb").read())&0xffffffff))' "$1"; }
[[ -f "$ALT" ]] || { echo "place the Starfy Translation Team v1.1 English ROM at $ALT (CRC32 F7CB8EE3)" >&2; exit 1; }
[[ $(crc "$ALT") == F7CB8EE3 ]] || { echo "wrong base: $ALT is not CRC32 F7CB8EE3" >&2; exit 1; }
mkdir -p out
"$PY" tools/build_s1.py "$ALT" "out/Starfy 1 Eng v1.0.3.gba" --v103 > out/build.log
C=$(crc "out/Starfy 1 Eng v1.0.3.gba"); echo "patched ROM: out/Starfy 1 Eng v1.0.3.gba CRC32 $C (expected 44C2017A)"
[[ $C == 44C2017A ]] || echo "NOTE: CRC differs from the release build (expected if you edited the text)"
rm -f "out/Starfy 1 Eng v1.0.3 (alt base).bps" "out/Starfy 1 Eng v1.0.3.bps"
"$FLIPS" --create --bps-delta "$ALT" "out/Starfy 1 Eng v1.0.3.gba" "out/Starfy 1 Eng v1.0.3 (alt base).bps"
if [[ -f "$JP" ]]; then
  [[ $(crc "$JP") == FAE94C8B ]] || { echo "wrong JP base: $JP is not CRC32 FAE94C8B" >&2; exit 1; }
  "$FLIPS" --create --bps-delta "$JP" "out/Starfy 1 Eng v1.0.3.gba" "out/Starfy 1 Eng v1.0.3.bps"
fi
ls -l out/*.bps

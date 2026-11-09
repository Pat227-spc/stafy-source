#!/usr/bin/env bash
# Build the Starfy 3 English cleanup patch.
# usage: ./build.sh [ALT_BASE.gba] [JP_BASE.gba]
#   ALT_BASE (default base/alt_base.gba): Dimedime v1.0 English ROM (Rev 1 + Dimedime's v1.0 BPS), CRC32 850B4137
#   JP_BASE  (default base/jp_base.gba, optional): Densetsu no Stafy 3 (Japan) (Rev 1), CRC32 2D6E4C3B
# Output: out/Starfy 3 Eng v1.0.5.gba (patched ROM, CRC32 852F70EE), out/Starfy 3 Eng v1.0.5 (alt base).bps, and out/Starfy 3 Eng v1.0.5.bps if JP_BASE exists.
# Steps: build_s3.py --v104 (v1.0.4, CRC32 4F31E799), then names_s3.py (cross-game names, v1.0.5).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"; cd "$HERE"
case "$(uname -s)" in MINGW*|MSYS*|CYGWIN*) FLIPS=tools/bin/flips.exe;; *) FLIPS=tools/bin/flips;; esac
PY="${PYTHON:-python3}"
ALT="${1:-base/alt_base.gba}"; JP="${2:-base/jp_base.gba}"
crc(){ "$PY" -c 'import zlib,sys;print("%08X"%(zlib.crc32(open(sys.argv[1],"rb").read())&0xffffffff))' "$1"; }
[[ -f "$ALT" ]] || { echo "place the Dimedime v1.0 English ROM (Rev 1 + Dimedime's v1.0 BPS) at $ALT (CRC32 850B4137)" >&2; exit 1; }
[[ $(crc "$ALT") == 850B4137 ]] || { echo "wrong base: $ALT is not CRC32 850B4137" >&2; exit 1; }
mkdir -p out
"$PY" tools/build_s3.py "$ALT" "out/v104.gba" --v104 > out/build.log
C=$(crc "out/v104.gba"); echo "v1.0.4 stage: CRC32 $C (expected 4F31E799)"
[[ $C == 4F31E799 ]] || { echo "v1.0.4 stage differs from the release; names_s3.py needs the exact v1.0.4 ROM" >&2; exit 1; }
"$PY" tools/names_s3.py "out/v104.gba" "out/Starfy 3 Eng v1.0.5.gba" --log out/names.tsv >> out/build.log
rm -f out/v104.gba
C=$(crc "out/Starfy 3 Eng v1.0.5.gba"); echo "patched ROM: out/Starfy 3 Eng v1.0.5.gba CRC32 $C (expected D9906201 (xh))"
[[ $C == 852F70EE ]] || echo "NOTE: CRC differs from the test build (expected if you edited the text)"
rm -f "out/Starfy 3 Eng v1.0.5 (alt base).bps" "out/Starfy 3 Eng v1.0.5.bps"
"$FLIPS" --create --bps-delta "$ALT" "out/Starfy 3 Eng v1.0.5.gba" "out/Starfy 3 Eng v1.0.5 (alt base).bps"
if [[ -f "$JP" ]]; then
  [[ $(crc "$JP") == 2D6E4C3B ]] || { echo "wrong JP base: $JP is not CRC32 2D6E4C3B" >&2; exit 1; }
  "$FLIPS" --create --bps-delta "$JP" "out/Starfy 3 Eng v1.0.5.gba" "out/Starfy 3 Eng v1.0.5.bps"
fi
ls -l out/*.bps

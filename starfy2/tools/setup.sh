#!/usr/bin/env bash
# Build the Linux toolchain used by build.sh (tested on Debian 13). Binaries go to tools/bin (not committed).
# Atlas.exe and lzss.exe are Windows tools run under wine; download them yourself (see tools/README.md)
# and copy them into tools/bin/.
set -euo pipefail
T="$(cd "$(dirname "$0")" && pwd)"; mkdir -p "$T/bin" "$T/src"
sudo dpkg --add-architecture i386 && sudo apt-get update
sudo apt-get install -y wine wine32:i386 wine64 cmake g++ make git python3
[[ -d "$T/src/armips" ]] || git clone --recursive https://github.com/Kingcom/armips.git "$T/src/armips"
git -C "$T/src/armips" checkout 62adab4 && git -C "$T/src/armips" submodule update --init --recursive
cmake -S "$T/src/armips" -B "$T/src/armips/build" -DCMAKE_BUILD_TYPE=Release && cmake --build "$T/src/armips/build" -j"$(nproc)"
cp "$T/src/armips/build/armips" "$T/bin/"
[[ -d "$T/src/Flips" ]] || git clone https://github.com/Alcaro/Flips.git "$T/src/Flips"
(cd "$T/src/Flips" && git checkout ff216a7 && make TARGET=cli CFLAGS=-O2) && cp "$T/src/Flips/flips" "$T/bin/"
for x in Atlas.exe lzss.exe; do [[ -f "$T/bin/$x" ]] || echo "still needed: tools/bin/$x (see tools/README.md)"; done
echo "tools ready in $T/bin"

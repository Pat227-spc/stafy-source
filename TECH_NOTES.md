# Technical notes

Current versions: Starfy 1 Eng v1.0.4, Starfy 2 Eng v0.9.9, Starfy 3 Eng v1.0.5 (release v1.0.5 at
https://github.com/Pat227-spc/stafy-patches). Hashes for every base, patch and result are in README.md.

## Patching notes
- BPS checks the base CRC, so a wrong base is refused.
- Starfy 1: our primary patch uses the clean Japanese base; the Starfy Translation Team v1.1 base patch is kept as an alternate.
- Starfy 3: our primary patch uses the clean Japanese (Rev 1) base; the Dimedime v1.0 base patch is kept as an alternate.
- Starfy 2 output is expanded to 32 MiB. Some flash carts (the Supercard SD) freeze on 32 MiB ROMs; `build.sh --rom16`
  makes a 16 MiB build with the same content (test build, CRC32 2535B598).
- Save type: SRAM 32 KB (SRAM_V112 / SRAM_V113) for all three.
- Emulator users: don't load savestates made with an older version; use the in-game save.

## Build / source notes
- Starfy 1 and Starfy 3: `build.sh` reproduces the release patches byte-for-byte (the `--v103` / `--v104` text sets, then
  the names pass in `tools/names_s1.py` / `tools/names_s3.py`).
- Starfy 2 is built from Megahog2014's Starfy 2 translation project, GPL-3.0
  (github.com/Megahog2014/Densetsu_no_Starfy_2_Translation_ENG), with art from Luckylodeon98's GPL-3.0 fork.
  Our build scripts and changes are GPL-3.0 too. Since v0.9.8 the build also runs `tools/check_script_sizes.py`,
  which fails the build if any in-level script would overflow the chat buffer. Since v0.9.9 any Atlas error fails the build
  by default (`STRICT_ATLAS=0` to warn and continue), and `build.sh` reproduces both release patches byte-for-byte.
- Bundled: armips (commit 62adab4, licence in thirdparty/armips/), flips (commit ff216a7, licence in thirdparty/flips/).
  Not bundled (no redistribution licence): Atlas 1.11, CUE's LZSS. Wine runs Atlas and lzss on Linux.

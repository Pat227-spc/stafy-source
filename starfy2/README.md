# Starfy 2 English patch (Densetsu no Stafy 2, GBA) - source

Source for "Starfy 2 Eng v0.9.9": the English fan translation of Densetsu no Stafy 2, built on Megahog2014's
Starfy 2 translation project (GPL-3.0) with art from Luckylodeon98's fork. Licence: GPL-3.0 (see LICENSE).

## Base ROM
Place your base ROM at `base/stafy2_jp.gba` (any path works; pass it to build.sh):
- Densetsu no Stafy 2 (Japan), clean, 16 MiB (16,777,216 bytes)
- CRC32 `EA73EB54`, SHA1 `8322867cc4369307048deb20a8bb16c3dd0910df`, MD5 `0635251b85657f9c1de295546da09aeb`

Release build (16 MiB, `./build.sh --rom16`): CRC32 `EC61D726`, SHA1 `bd3fbaf52e37bef3b58d3ba03437b337e69f4bf8`
(patch SHA1 `b3655af73d7e363c974c06d0346a8884c704bfd1`). The blocks that earlier versions put above 16 MiB are moved into
the original image's free space (`tools/rom16.py`; `tools/rom16_audit.py` compares the two layouts).
Old 32 MiB layout (`./build.sh` without `--rom16`, same content, not released): CRC32 `EE1ED052`,
SHA1 `f7b60e1a3de57f259a5b2f5a3c3e40b2686b7541`.
No ROMs are included.

## Layout
- `upstream/` - the upstream translation project tree (commit de569ee "World2_1 added"): Atlas scripts (`asm/bin/text/`),
  table files (`*.TBL`), graphics sources and edits (`asm/bin/graphics/`), VWF font/code (`asm/VWF/`, `VWF.bps`),
  armips sources (`asm/*.asm`) and `assemble.bat`. Never edited by the build; ROMs, .exe files and scratch archives removed.
- `backfill/scripts/` - additional/updated translated scripts (mirrors `upstream/asm/bin/text/`).
- `overlay/` - fixes layered over the upstream tree (see `overlay/README.md`): graphics, glyph overrides, armips patches.
- `tools/` - build helpers (`batsteps.py` parses assemble.bat, `overlay.py`, `glyphs.py`, `gfx_prep.py`, `rom16.py`, `check_script_sizes.py`, `gfx/*.py`; optional `env.sh`).
- `build.sh` - full build: base ROM -> patched ROM -> .bps.

## Tools
| tool | version | status |
|---|---|---|
| armips | v0.11.0 (git 62adab4) | bundled Linux x86-64 binary `tools/bin/armips` (MIT, `thirdparty/armips/`) - https://github.com/Kingcom/armips |
| Floating IPS (flips) | v199 (git ff216a7) | bundled Linux x86-64 binary `tools/bin/flips` (GPL-3.0, `thirdparty/flips/`) - https://github.com/Alcaro/Flips |
| Atlas | 1.11 (Klarth) | NOT bundled - download from https://www.romhacking.net/utilities/224/ and put `Atlas.exe` in `tools/bin/` |
| lzss (CUE, 2011) | `lzss.exe` | NOT bundled - from CUE's GBA/DS compressors, https://www.romhacking.net/utilities/826/ ; put `lzss.exe` in `tools/bin/` |
| wine | tested 10.0 | Linux only, runs Atlas.exe / lzss.exe |
| Python 3 | tested 3.13 | with numpy, scipy, Pillow (`pip install numpy scipy pillow`) |

`tools/setup.sh` rebuilds armips and flips from source on Debian/Ubuntu and installs wine.

## Build (Linux)
```
sudo apt install wine wine32:i386 python3 python3-numpy python3-scipy python3-pil   # or: tools/setup.sh
cp /path/to/Atlas.exe /path/to/lzss.exe tools/bin/
./build.sh base/stafy2_jp.gba out/stafy2_en.bps
```
The build works in `build/` (scratch copy) and prints the patched ROM CRC32; `build/stafy2_en.gba` is the patched ROM and
`out/stafy2_en.bps` the patch. Any Atlas error fails the build by default (`STRICT_ATLAS=0` warns and continues like
assemble.bat); `--no-logo` keeps the Japanese title logo; `--rom16` makes the 16 MiB release layout
(`./build.sh --rom16 base/stafy2_jp.gba out/stafy2_en_16.bps`). New scenes are built in parallel (`OVERLAY_JOBS=N`, default: all cores).
The first wine run creates a wine prefix in `tools/wineprefix` (set `WINEPREFIX` to use another). If wine is not on your
PATH, set `WINE_BIN` to its `bin/` folder (read by `tools/env.sh`).

## Build (Windows)
Easiest: use WSL2 (Ubuntu) and follow the Linux steps. Native alternative (Git Bash or MSYS2): install Python 3 with numpy,
scipy and Pillow, put Windows builds of `armips.exe` and `flips.exe` (from the links above) plus `Atlas.exe` and `lzss.exe`
in `tools\bin\`, then run `./build.sh base/stafy2_jp.gba` from Git Bash; build.sh runs the .exe tools directly there.
(The native Windows path is not tested; WSL2 is.)

## Edit the script and rebuild
- Dialogue/scene text: edit the `.txt` Atlas scripts. Put changed copies under `backfill/scripts/` (same relative path as in
  `upstream/asm/bin/text/`) or `overlay/asm/bin/text/`; overlay wins over backfill, both win over upstream.
  Keep the `#` Atlas commands and `<line>` codes; characters must exist in the matching `.TBL`.
- New scenes: add a `//POINTER: 0x0814E28C` header (the pointer to repoint) or a line in `scenes.tsv`; see `tools/overlay.py`.
- Graphics: replace the `.bin` under `overlay/asm/bin/graphics/...` and reference it in `overlay/asm/graphics.asm`.
- Font glyphs: `overlay/glyphs/<Font>/<index>.txt`; widths in an armips patch (see `overlay/patches/70_intro_font_quotes.asm`).
- Then rerun `./build.sh`. The CRC will no longer match the release once you change anything (expected).

## Make a .bps patch
build.sh already writes `out/stafy2_en.bps` (flips `--create --bps-delta`). By hand:
`tools/bin/flips --create --bps-delta base/stafy2_jp.gba build/stafy2_en.gba my_patch.bps`.
Apply with `flips --apply my_patch.bps base.gba out.gba` (or any BPS patcher).

## Credits

All credit goes to the translators and hackers who came before us. This is simply an assembly of their work, including the translations we used. We have no desire to take credit for it.

- Starfy Translation Team / Megahog2014 - Densetsu no Stafy English translation (v1.1), Stafy 2 translation project and scripts
  (source: github.com/Megahog2014/Densetsu_no_Starfy_2_Translation_ENG; romhacking.net/translations/7057)
- Starfy 1 translation (Starfy Translation Team), credited on romhacking.net/translations/7057:
  - Higsby - original translation
  - pablitox - original hacking
  - wowjinxy - graphics (text GFX and English font)
  - Megahog2015 - graphics
  - EvieMelody (EvieMelodylvsoulmate4ever) - production
- SomeUselessTranslations (AUselessMage) - complete Stafy 2 script localization (source for untranslated scenes; also the source of Dimedime's Stafy 3 script)
  (source: starfywiki.org/wiki/Fan_translation; youtube.com/playlist?list=PLA7NjZIk-WKX6E8fTEwiEtI3XlpZy2CQm)
- Dimedime - The Legendary Starfy 3 English patch v1.0
  (source: starfywiki.org/wiki/Fan_translation)
- Luckylodeon98 - World 5-3 fruit puzzle art and English clue chain (used as-is in Starfy 2 v0.9.5)
- Luckylodeon98 - Stafy 2 graphics and VWF integration (upstream fork of the Stafy 2 project); from his README:
  'VWF code by RayCarrot / Graphics by Megahog2015/Luckylodeon98 and WowJinxy / Translations supplied by SomeUselessTranslations'
- RayCarrot - VWF (variable-width font) code used in Stafy 2
- RayCarrot, Normmatt - font graphics, tools and technical help
  (Normmatt's VWF/text insertion tool: starfywiki.org/wiki/Fan_translation)
- Title logo based on EASTWOOD2002's English 'The Legendary Starfy 2' logo concept (LaunchBox forums, 2023)
  (`tools/gfx/title_logo_en.png`; thanks to u/ComicGamerDragon for suggesting it)

All translation credit belongs to the original translators. Starfy is (c) Nintendo / TOSE. Not affiliated with Nintendo.

An in-game translator credits page is planned for a future update.

### Tools
Everyone who built a tool we used:

- armips by Kingcom, with contributors sp1187, unknownbrackets, Prof9, Fothsid, StraDaMa, queueRAM, Normmatt, hrydgard, Blade2187, Zeturic, tclamb, kabochi, adakite1, PeterLemon, LemonBoy, warmenhoven, radimerry, nekopsykose, onlymx13, GermanAizek, kwyxz, jeffman, archshift, aliaspider, dfuchsgruber, Thar0, Bigpet, socram8888, lioncash, joeydumont, bentley, Amjad50 - https://github.com/Kingcom/armips (MIT; bundled Linux build of commit 62adab4, licence in thirdparty/armips/)
- Floating IPS (flips) by Alcaro, with contributors Sir-Walrus, Miepee, orbea, Kekun, mrexodia, althonos, foxsouns, bbhtt, trillllian - https://github.com/Alcaro/Flips (GPL-3.0; bundled Linux build of commit ff216a7, licence in thirdparty/flips/)
- Atlas 1.11 by Klarth - https://www.romhacking.net/utilities/224/ (not bundled: no redistribution licence)
- LZSS (CUE's GBA/DS compressors, 2011) by CUE - https://www.romhacking.net/utilities/826/ (not bundled: no redistribution licence)
- VWF (variable-width font) code by RayCarrot, integrated by Luckylodeon98 - https://github.com/Luckylodeon98/Densetsu_no_Starfy_2_Translation_ENG
- Normmatt's VWF/text insertion tool - https://www.starfywiki.org/wiki/Fan_translation
- mGBA by endrift - https://github.com/mgba-emu/mgba (testing)
- NanoBoyAdvance by fleroviux - https://github.com/nba-emu/NanoBoyAdvance (testing)
- VisualBoyAdvance-M by the VBA-M project - https://github.com/visualboyadvance-m/visualboyadvance-m (testing)
- Wine by the Wine project - https://www.winehq.org/ (runs Atlas and lzss on Linux)
- Python, NumPy, SciPy and Pillow by their projects - https://www.python.org/, https://numpy.org/, https://scipy.org/, https://python-pillow.org/

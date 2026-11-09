# Starfy 1 Eng v1.0.4 - source

Cleanup patch for the Starfy Translation Team v1.1 translation of Densetsu no Stafy (GBA): typo fixes, re-wrapped overflowing lines, leftover Japanese translated,
consistency renames. The builder is a Python script that edits the English base ROM's text in place or relocates edited
messages to free space and repoints them.

## Base ROMs
Place your base ROM at `base/alt_base.gba`:
- Starfy Translation Team v1.1 English ROM (8 MiB) - CRC32 `F7CB8EE3`, SHA1 `79c4f1847dace4efceecff0a211cf341ad372808`

Optional, to also make the primary patch for the clean Japanese ROM, place it at `base/jp_base.gba`:
- Densetsu no Stafy (Japan), clean, 8 MiB - CRC32 `FAE94C8B`, SHA1 `75f6297f42c41e2a6d108de9a372308ad2df6a9c`

Expected result: CRC32 `A78A3D9C`, SHA1 `9c15719d20c06722679170cbd46c05b074add576` (v1.0.4: the cross-game names pass and "the Great Moe"; the v1.0.3 release stage is CRC32 `44C2017A`). No ROMs are included.

## Tools
- Python 3 (tested 3.13; standard library only)
- Floating IPS (flips) v199, git ff216a7 - bundled Linux x86-64 binary `tools/bin/flips`, third-party tool by Alcaro,
  GPL-3.0 (`thirdparty/flips/`), source: https://github.com/Alcaro/Flips

## Build (Linux)
```
./build.sh                      # uses base/alt_base.gba and (if present) base/jp_base.gba
./build.sh ALT.gba [JP.gba]     # or pass paths
```
Outputs `out/Starfy 1 Eng v1.0.4.gba` (patched ROM; CRC printed and checked), `out/Starfy 1 Eng v1.0.4 (alt base).bps` and, with the JP base,
`out/Starfy 1 Eng v1.0.4.bps`. Manual equivalent: `python3 tools/build_s1.py base/alt_base.gba stage.gba --v103` then `python3 tools/names_s1.py stage.gba out.gba`.

## Build (Windows)
Install Python 3 and download a Windows flips.exe from https://github.com/Alcaro/Flips/releases into `tools\bin\`.
Run `build.sh` from Git Bash, or by hand in cmd:
```
py tools\build_s1.py base\alt_base.gba stage.gba --v103
py tools\names_s1.py stage.gba out.gba
tools\bin\flips.exe --create --bps-delta base\alt_base.gba out.gba patch.bps
```

## Edit the text and rebuild
All edits are data tables in the builder: TYPOS, RENAMES, FIXES_V102 and NAME_SETS in tools/build_s1.py; the cross-game names (decided 2026-11-03, same as Starfy 2) are the NAMES table in tools/names_s1.py (text codec: tools/s1text.py, width model: tools/s1width.py, Ogura/Doppel case conversion: tools/ogcase.py).
Add a (old, new) pair or a message entry, rerun `./build.sh`, and test in an emulator. The builders assert the base CRC and
fail loudly if an edit target is not found. The CRC will differ from the release once you change anything (expected).

## Make a .bps patch
build.sh writes the .bps files with `flips --create --bps-delta BASE PATCHED OUT.bps`. Apply with
`flips --apply OUT.bps BASE result.gba` or any BPS patcher (BPS checks the base CRC).

## Not included
The English base text itself is part of the base translation ROM, so no full text dump is shipped (it would be ROM data).

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

Thanks: EpicSignal (spotting the World 5-3 puzzle issue).

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

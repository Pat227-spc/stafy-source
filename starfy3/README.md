# Starfy 3 Eng v1.0.5 (test) - source

Cleanup patch for Dimedime's v1.0 translation of Densetsu no Stafy 3 (GBA): typo fixes, re-wrapped overflowing lines, leftover Japanese translated,
consistency renames. The builder is a Python script that edits the English base ROM's text in place or relocates edited
messages to free space and repoints them.

## Base ROMs
Place your base ROM at `base/alt_base.gba`:
- Dimedime v1.0 English ROM (Rev 1 + Dimedime's v1.0 BPS) - CRC32 `850B4137`, SHA1 `179920be4a0ae5ed60137103deca4a760811517b`

Optional, to also make the primary patch for the clean Japanese ROM, place it at `base/jp_base.gba`:
- Densetsu no Stafy 3 (Japan) (Rev 1), clean, 16 MiB - CRC32 `2D6E4C3B`, SHA1 `dae5354bfe4ccafc92d22b1389265dbf1f79b636`

Expected result: CRC32 `D9906201`, SHA1 `57da9abd33423a9d7b5f270369210d5b0ed8897d` (v1.0.5 test build xh, 2026-11-09; includes Snarley + 15 Great Moe Tier A lines on top of the xg names pass). No ROMs are included.

## Tools
- Python 3 (tested 3.13; standard library only)
- Floating IPS (flips) v199, git ff216a7 - bundled Linux x86-64 binary `tools/bin/flips`, third-party tool by Alcaro,
  GPL-3.0 (`thirdparty/flips/`), source: https://github.com/Alcaro/Flips

## Build (Linux)
```
./build.sh                      # uses base/alt_base.gba and (if present) base/jp_base.gba
./build.sh ALT.gba [JP.gba]     # or pass paths
```
Outputs `out/Starfy 3 Eng v1.0.5.gba` (patched ROM; CRC printed and checked), `out/Starfy 3 Eng v1.0.5 (alt base).bps` and, with the JP base,
`out/Starfy 3 Eng v1.0.5.bps`. Manual equivalent: `python3 tools/build_s3.py base/alt_base.gba stage.gba --v104` then `python3 tools/names_s3.py stage.gba out.gba`.

## Build (Windows)
Install Python 3 and download a Windows flips.exe from https://github.com/Alcaro/Flips/releases into `tools\bin\`.
Run `build.sh` from Git Bash, or by hand in cmd:
```
py tools\build_s3.py base\alt_base.gba stage.gba --v104
py tools\names_s3.py stage.gba out.gba
tools\bin\flips.exe --create --bps-delta base\alt_base.gba out.gba patch.bps
```

## Edit the text and rebuild
All edits are data tables in the builder: edits(), edits_v101(), TYPOS, chuta() and the v103 block in tools/build_s3.py; the cross-game names (decided 2026-11-03, same as Starfy 2) are the NAMES table in tools/names_s3.py (BMG message files: tools/bmg.py, text encoder: tools/s3text.py, width check: tools/s3width.py).
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

# Starfy (Densetsu no Stafy) GBA trilogy - English patch sources

> **Note:** AI tools were used in the making of this project.

Source handover for the English fan-translation patches of the three Densetsu no Stafy games on GBA, so the
translation can be rebuilt and continued. Each folder is a standalone git repo that rebuilds its patch from a
user-supplied base ROM. No ROMs are included.

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

Thanks: Giantbomb64 (reporting the World 2-1 crash) and EpicSignal (spotting the World 5-3 puzzle issue).

All translation credit belongs to the original translators. Starfy is (c) Nintendo / TOSE. Not affiliated with Nintendo.

An in-game translator credits page is planned for a future update.

### Verify it yourself
Please don't just take our word for it. These are the hashes to check against (also in SHA1SUMS.txt):

```
Starfy 1 Eng v1.0.4
  Base:  Densetsu no Stafy (Japan)   CRC32 FAE94C8B  SHA1 75f6297f42c41e2a6d108de9a372308ad2df6a9c
  Alt base: STT v1.1 English ROM     CRC32 F7CB8EE3  SHA1 79c4f1847dace4efceecff0a211cf341ad372808
  Result:                            CRC32 A78A3D9C  SHA1 9c15719d20c06722679170cbd46c05b074add576
  Patch SHA1: Starfy.1.Eng.v1.0.4.bps                   3ed5334d3952ef700de43a23f1b3f9c1f571aae9
              Starfy.1.Eng.v1.0.4.STT.v1.1.base.bps     f7788a3c7cdeca007cd29a71d46888f8b1bd31d9
Starfy 2 Eng v0.9.9
  Base:  Densetsu no Stafy 2 (Japan) CRC32 EA73EB54  SHA1 8322867cc4369307048deb20a8bb16c3dd0910df
  Result (32 MiB):                   CRC32 4F018FF0  SHA1 3f6bb3a001070e184d82736ac88cbd448dd095ca
  Patch SHA1: Starfy.2.Eng.v0.9.9.bps                   6d24a1c863a5a5c4ec02bc74dee6ef64b6f63330
  16 MiB test build (--rom16, Supercard):
  Result (16 MiB):                   CRC32 2535B598  SHA1 c5b2cd3a6e8b9ac3ee30e90cfbfad790522fe796
  Patch SHA1: Starfy.2.Eng.v0.9.9.16MB.TEST.bps         fb7627cb7b090efb29115f795c3f74736cb14d14
Starfy 3 Eng v1.0.5
  Base:  Densetsu no Stafy 3 (Japan) (Rev 1)  CRC32 2D6E4C3B  SHA1 dae5354bfe4ccafc92d22b1389265dbf1f79b636
  Alt base: Dimedime v1.0 English ROM         CRC32 850B4137  SHA1 179920be4a0ae5ed60137103deca4a760811517b
  Result:                                     CRC32 7D5EC993  SHA1 9fc07309de116572191518b1c791607497c0cab6
  Patch SHA1: Starfy.3.Eng.v1.0.5.bps                   d60f87f7c1ab0258fd72d5733c43cf15a43f8002
              Starfy.3.Eng.v1.0.5.Dimedime.v1.0.base.bps   805a4c58eb4553d668b11936118e507ed314c339
```

To check a file: `sha1sum <file>` (Linux/macOS) or `certutil -hashfile <file> SHA1` (Windows).
You can also rebuild the patches yourself from https://github.com/Pat227-spc/stafy-source (see each game's README),
then compare the SHA1 of your patched ROM with the Result SHA1 above. If anything doesn't match, please let us know.

## Original projects
If you enjoy these games, please visit and support the people who actually made the translations:
- Megahog2014 / Starfy Translation Team (Starfy 2 project): https://github.com/Megahog2014/Densetsu_no_Starfy_2_Translation_ENG
- Starfy Translation Team, Starfy 1 (romhacking.net): https://www.romhacking.net/translations/7057/
- Luckylodeon98 (Starfy 2 fork, graphics and VWF): https://github.com/Luckylodeon98/Densetsu_no_Starfy_2_Translation_ENG
- SomeUselessTranslations (Starfy 2 script videos): https://www.youtube.com/playlist?list=PLA7NjZIk-WKX6E8fTEwiEtI3XlpZy2CQm
- Starfy Wiki fan translation page (Dimedime, SomeUselessTranslations, Normmatt): https://www.starfywiki.org/wiki/Fan_translation

## Build on it

We'd love to see forks, improvements, or new projects built on our work. Pull requests and forks are welcome; we just ask that you keep crediting the original translators.
Found a bug? Please open an issue at https://github.com/Pat227-spc/stafy-patches/issues.

## Credit and takedown requests
If you are one of the original authors and would like your name changed or removed, or your work taken out,
please open an issue at https://github.com/Pat227-spc/stafy-patches/issues and it will be honored promptly. No questions asked.


## Tools
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

| folder | release | base ROM to supply | result CRC32 |
|---|---|---|---|
| `starfy1/` | Starfy 1 Eng v1.0.4 | Starfy Translation Team v1.1 English ROM, CRC32 F7CB8EE3 (SHA1 79c4f1847dace4efceecff0a211cf341ad372808); optional clean Densetsu no Stafy (Japan), CRC32 FAE94C8B (SHA1 75f6297f42c41e2a6d108de9a372308ad2df6a9c) | A78A3D9C |
| `starfy2/` | Starfy 2 Eng v0.9.9 | Densetsu no Stafy 2 (Japan), CRC32 EA73EB54 (SHA1 8322867cc4369307048deb20a8bb16c3dd0910df) | 4F018FF0 (16 MiB `--rom16` build: 2535B598) |
| `starfy3/` | Starfy 3 Eng v1.0.5 | Dimedime v1.0 English ROM, CRC32 850B4137 (SHA1 179920be4a0ae5ed60137103deca4a760811517b); optional clean Densetsu no Stafy 3 (Japan) (Rev 1), CRC32 2D6E4C3B (SHA1 dae5354bfe4ccafc92d22b1389265dbf1f79b636) | 7D5EC993 |

## Tools
- Starfy 1 / 3: Python 3 and flips (bundled Linux build).
- Starfy 2: Python 3 (numpy, scipy, Pillow), wine (Linux), armips v0.11.0 and flips (bundled Linux builds),
  Atlas 1.11 and CUE's lzss.exe (download; not redistributable). See `starfy2/README.md`.

## Quick start (Linux)
```
cd starfy1 && cp /path/to/your/rom.gba base/alt_base.gba && ./build.sh
cd starfy3 && cp /path/to/your/rom.gba base/alt_base.gba && ./build.sh
cd starfy2 && cp /path/to/Atlas.exe /path/to/lzss.exe tools/bin/ && ./build.sh /path/to/base.gba
```
Windows: use WSL2 with the same steps, or see each README for native Git Bash / cmd steps.
Editing the script, rebuilding and making a .bps patch are covered in each game's README.


# Starfy (Densetsu no Stafy) GBA trilogy - English patch sources

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

Thanks: EpicSignal (spotting the World 5-3 puzzle issue).

All translation credit belongs to the original translators. Starfy is (c) Nintendo / TOSE. Not affiliated with Nintendo.

An in-game translator credits page is planned for a future update.

### Third-party tools
- armips by Kingcom (MIT) - https://github.com/Kingcom/armips (bundled Linux build of commit 62adab4, licence in thirdparty/armips/)
- Floating IPS (flips) by Alcaro (GPL-3.0) - https://github.com/Alcaro/Flips (bundled Linux build of commit ff216a7, licence in thirdparty/flips/)
- Atlas 1.11 by Klarth - https://www.romhacking.net/utilities/224/ (not bundled: no redistribution licence)
- LZSS (CUE's GBA/DS compressors, 2011) by CUE - https://www.romhacking.net/utilities/826/ (not bundled: no redistribution licence)

| folder | release | base ROM to supply | result CRC32 |
|---|---|---|---|
| `starfy1/` | Starfy 1 Eng v1.0.2 | Starfy Translation Team v1.1 English ROM, CRC32 F7CB8EE3 (SHA1 79c4f1847dace4efceecff0a211cf341ad372808); optional clean Densetsu no Stafy (Japan), CRC32 FAE94C8B (SHA1 75f6297f42c41e2a6d108de9a372308ad2df6a9c) | 72AE1467 |
| `starfy2/` | Starfy 2 Eng v0.9.5 | Densetsu no Stafy 2 (Japan), CRC32 EA73EB54 (SHA1 8322867cc4369307048deb20a8bb16c3dd0910df) | 2165E2C8 |
| `starfy3/` | Starfy 3 Eng v1.0.3 | Dimedime v1.0 English ROM, CRC32 850B4137 (SHA1 179920be4a0ae5ed60137103deca4a760811517b); optional clean Densetsu no Stafy 3 (Japan) (Rev 1), CRC32 2D6E4C3B (SHA1 dae5354bfe4ccafc92d22b1389265dbf1f79b636) | 23170373 |

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


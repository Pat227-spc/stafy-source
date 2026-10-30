; overlay/asm/graphics.asm (v0.9.2-test) - Luckylodeon98's asm/graphics.asm from his fork of the Starfy 2 translation
; (GPL-3.0), commit dbfd7cc (art from a5d1a18 "All art is finished!"), MODIFIED by us: lines marked
; '[v0.9.2 overlay: excluded ...]' are commented out because our own overlay/patches/ English graphic covers the same
; asset (S2-D decision items). v0.9.5: the 5-3 food puzzle uses Luckylodeon98's a5d1a18 set (S2-D022; fixes headerless sprites).

.gba				; Set the architecture to GBA
.open "rom/outputGFX.gba",0x08000000		; Open input.gba for output.
					; 0x08000000 will be used as the
					; header size

.org 0x09000000
.area 0x09000004

;-------------------------------Graphics & Tilemaps
;HUD Assets
;This also holds the back button for the tutorial signs!
HUDLZSS1:
	.incbin asm/bin/graphics/Health/1HUDLZSS.bin

;Moe's (Kyorosuke) House
.align 4
MoeHouseOBJ:
	.incbin asm/bin/graphics/MoeHouse/1MoeHouseOBJ.bin

.align 4
MoeHouseBG:
	.incbin asm/bin/graphics/MoeHouse/2MoeHouseBG.bin
	
.align 4
MoeHouseSelection_Tilemap1:
	.incbin asm/bin/graphics/MoeHouse/1MoeHouseSelectionTilemap1.bin

.align 4
MoeHouseSelection_Tilemap2:
	.incbin asm/bin/graphics/MoeHouse/2MoeHouseSelectionTilemap2.bin
	
.align 4
MoeHouseBGTileMap:
	.incbin asm/bin/graphics/MoeHouse/3MoeHouseBGTileMap.bin
	

;File Select Screen
.align 4
FileSelect_Object:
	.incbin asm/bin/graphics/FileSelect/1FileSelectOBJ.bin

.align 4
FileSelect_BG:
	.incbin asm/bin/graphics/FileSelect/2FileSelectBG.bin
	
.align 4
FileSelect_BG_Tilemap:
	.incbin asm/bin/graphics/FileSelect/2FileSelectBGTilemap.bin
	
.align 4
FileSelect_FileErasePrompt_Tilemap:
	.incbin asm/bin/graphics/FileSelect/3FileSelect_FileErasePrompt_Tilemap.bin
	
.align 4
FileSelect_CopyAndErasePopup_Tilemap:
	.incbin asm/bin/graphics/FileSelect/4CopyAndErasePopup_FileTileMap.bin
;Game Over Screen
.align 4
GameOverOBJ:
	.incbin asm/bin/graphics/GameOver/1GameOverOBJ.bin

;World 1-3 Lovely's Shop Sign
.align 4
LovelyShop1_3:
;[v0.9.2 overlay: excluded, ours wins / decision item] 	.incbin asm/bin/graphics/lovelyshop1_3/1lovelyshop1_3OBJ.bin

;World 1-3 Lovely's Pamphlet
.align 4
LovelyPamphlet:
	.incbin asm/bin/graphics/lovelyshop1_3/2lovelypamphletobj.bin

.align 4
Goalflag4_3: ;GOAL flag 4-3
;[v0.9.2 overlay: excluded, ours wins / decision item] 	.incbin asm/bin/graphics/goalflag/1goalflag.bin

;World 5-3 Fruits
;------------------------------------------------------
;Served only for other translations if needed (YOU ADD THE LOCATION)
;.align 4
;Banana_Replacement:
;	.incbin asm/bin/graphics/Food_Puzzle/Replacements/
;------------------------------------------------------
.align 4
Eggplant_Replacement:
	.incbin asm/bin/graphics/Food_Puzzle/Replacements/Eggplant_Replacement/1EggplantToApple.bin

.align 4
Pumpkin_Replacement:
	.incbin asm/bin/graphics/Food_Puzzle/Replacements/Pumpkin_Replacement/1PumpkinToTomato.bin

.align 4
Persimmon_Replacement:
	.incbin asm/bin/graphics/Food_Puzzle/Replacements/Persimmon_Replacement/1PersimmonToTurnip.bin

.align 4
Cucumber_Replacement:
	.incbin asm/bin/graphics/Food_Puzzle/Replacements/Cucumber_Replacement/1CucumberToPumpkin.bin

.align 4
Shell_Replacement:
	.incbin asm/bin/graphics/Food_Puzzle/Replacements/Shell_Replacement/1ShellToTumeric.bin

.align 4
Squid_Replacement:
	.incbin asm/bin/graphics/Food_Puzzle/Replacements/Squid_Replacement/1SquidToCarrot.bin

.align 4
Melon_Replacement:
	.incbin asm/bin/graphics/Food_Puzzle/Replacements/Melon_Replacement/1MelonToEggplant.bin

.align 4
Apple_Replacement:
	.incbin asm/bin/graphics/Food_Puzzle/Replacements/Apple_Replacement/1AppleToNuts.bin
	
.align 4
Food_Sign_Replacement:
	.incbin asm/bin/graphics/Food_Puzzle/Replacements/Food_Sign_Replacement/1Food_Signs.bin
	
;World 5-4 Mole Poster
.align 4
Mole_Message:
	.incbin asm/bin/graphics/MessagefromMole/1MessagefromMole.bin

;World Selection Screen Graphics
.align 4
WorldSelectOBJ:
	.incbin asm/bin/graphics/World_Select_Map/1WorldSelectMapOBJ.bin
;Stuff Screen Graphics
.align 4
StuffScreenBG:
	.incbin asm/bin/graphics/Stuff_Screen/1StuffScreenBG.bin
.align 4
StuffScreenOBJ:
	.incbin asm/bin/graphics/Stuff_Screen/2StuffScreenOBJ.bin
;Stuff Screen Outfit and Accessory updates
.align 4
BoxOutfit:
	.incbin asm/bin/graphics/Stuff_Screen/Outfit/1boxoutfit.bin
.align 4
BaseballcapAcessory:
	.incbin asm/bin/graphics/Stuff_Screen/Accessory/1baseballcapaccessory.bin
.align 4
BaseballUniformOutfit:
	.incbin asm/bin/graphics/Stuff_Screen/Outfit/2baseballuniformoutfit.bin
.align 4
WrestlingLeotardOutfit:
	.incbin asm/bin/graphics/Stuff_Screen/Outfit/3wrestlingleotardoutfit.bin
.align 4
SwimsuitOutfit:
	.incbin asm/bin/graphics/Stuff_Screen/Outfit/4swimsuitoutfit.bin
.align 4
MotorJacketOutfit:
	.incbin asm/bin/graphics/Stuff_Screen/Outfit/5motorjacketoutfit.bin
;Book Screen
.align 4
BookScreenOBJ:
	.incbin asm/bin/graphics/Book/1BookScreenOBJ.bin
.align 4
BookScreenBG:
	.incbin asm/bin/graphics/Book/2BookScreenBG.bin
.align 4
BookScreenBGTilemap:
	.incbin asm/bin/graphics/Book/3BookScreenTilemap.bin
	
;Tutorial Signs
.align 4
TutorialSignSwimming:
	.incbin asm/bin/graphics/tutorial_signs/swimming/1swimming.bin
	
.align 4
TutorialSignTurboSwim:
	.incbin asm/bin/graphics/tutorial_signs/turbo_swim/1Turboswim.bin
	
.align 4
TutorialSignSurfJump:
	.incbin asm/bin/graphics/tutorial_signs/surf_jump/1surfjump.bin
	
.align 4
TutorialSignWalking:
	.incbin asm/bin/graphics/tutorial_signs/walking/1walking.bin
	
.align 4
TutorialSignDuck:
	.incbin asm/bin/graphics/tutorial_signs/duck/1duck.bin
	
.align 4
TutorialSignJump:
	.incbin asm/bin/graphics/tutorial_signs/jump/1jump.bin

.align 4
TutorialSignDash:
	.incbin asm/bin/graphics/tutorial_signs/dash/1dash.bin

.align 4
TutorialSignDashJump:
	.incbin asm/bin/graphics/tutorial_signs/dash_jump/1dashjump.bin

.align 4
TutorialSignSlide:
	.incbin asm/bin/graphics/tutorial_signs/slide/1slide.bin

.align 4
TutorialSignEnteringDoors:
	.incbin asm/bin/graphics/tutorial_signs/entering_doors/1enteringdoors.bin

.align 4
TutorialSignTalking:
	.incbin asm/bin/graphics/tutorial_signs/talking/1talking.bin

.align 4
TutorialSignStarSpin:
	.incbin asm/bin/graphics/tutorial_signs/starspin/1starspin.bin

.align 4
TutorialSignGlide:
	.incbin asm/bin/graphics/tutorial_signs/glide/1glide.bin

.align 4
TutorialSignAirJump:
	.incbin asm/bin/graphics/tutorial_signs/air_jump/1airjump.bin

.align 4
TutorialSignMightyStarSpin:
	.incbin asm/bin/graphics/tutorial_signs/mighty_star_spin/1mightystarspin.bin

.align 4
TutorialSignShootingStar:
	.incbin asm/bin/graphics/tutorial_signs/shooting_star/1shootingstar.bin

.align 4
TutorialSignUltraStarSpin:
	.incbin asm/bin/graphics/tutorial_signs/ultrastarspin/1ultrastarspin.bin

.align 4
TutorialSignBlimp:
	.incbin asm/bin/graphics/tutorial_signs/blimp/1blimp.bin

.align 4
TutorialSignJetBlimp:
	.incbin asm/bin/graphics/tutorial_signs/jetblimp/1jetblimp.bin

.align 4
TutorialSignSeaSkater:
	.incbin asm/bin/graphics/tutorial_signs/sea_skater/1seaskater.bin

.align 4
TutorialSignSoarinSeaSkater:
	.incbin asm/bin/graphics/tutorial_signs/SoarinSeaSkater/1soarinseaskater.bin

.align 4
TutorialSignRyun:
	.incbin asm/bin/graphics/tutorial_signs/ryun/1ryun.bin

.align 4
TutorialSignSuperRyun:
	.incbin asm/bin/graphics/tutorial_signs/SuperRyun/1superryun.bin

.align 4
TutorialSignKoalaCostume:
	.incbin asm/bin/graphics/tutorial_signs/Koala_Costume/1koalacostume.bin

.align 4
TutorialSignHooligatorCostume:
	.incbin asm/bin/graphics/tutorial_signs/Hooligator_Costume/1hooligatorcostume.bin

;Lovely's Shop
.align 4
LovelyShopBG:
	.incbin asm/bin/graphics/lovelyshop/1lovelyshopBG.bin

.align 4
LovelyShopOBJ:
	.incbin asm/bin/graphics/lovelyshop/2lovelyshopOBJ.bin

;Treasure Screen
.align 4
TreasureScreenBG:
	.incbin asm/bin/graphics/treasurescreen/1treasurescreenBG.bin

.align 4
TreasureScreenOBJ:
	.incbin asm/bin/graphics/treasurescreen/3treasurescreenOBJ.bin

.align 4
TreasureScreenTilemap:
	.incbin asm/bin/graphics/treasurescreen/2treasurescreenTilemap.bin

;Photo screen
.align 4
PhotoOBJ:
	.incbin asm/bin/graphics/photos/1photoOBJ.bin

.align 4
PhotoBG:
	.incbin asm/bin/graphics/photos/2photoBG.bin

.align 4
PhotoTilemap:
	.incbin asm/bin/graphics/photos/3photoTilemap.bin

;Sea Jams screen
.align 4
SeaJamsBG:
	.incbin asm/bin/graphics/seajams/1seajamsBG.bin

.align 4
SeaJamsOBJ:
	.incbin asm/bin/graphics/seajams/2seajamsOBJ.bin

.align 4
MinigameMenuAssets:
	.incbin asm/bin/graphics/minigamemenu/1MinigameMenuOBJ.bin

;MinigameHUD
.align 4
MinigameHUDBG:
	.incbin asm/bin/graphics/minigamehud/2minigamehudBG.bin

.align 4
MinigameHUDOBJ:
	.incbin asm/bin/graphics/minigamehud/3minigamehudOBJ.bin

.align 4
ColorMatcherOBJ:
	.incbin asm/bin/graphics/minigamehud/colormatcher/1colormatcherOBJ.bin

;PauseMenuGraphics
.align 4
PausemenuBG:
	.incbin asm/bin/graphics/pausemenu/1pausemenuBG.bin

.align 4
PausemenuOBJ:
	.incbin asm/bin/graphics/pausemenu/2pausemenuOBJ.bin
	
.align 4
PausemenuTilemap:
	.incbin asm/bin/graphics/pausemenu/3pausemenuTilemap.bin
;Clear Screen Graphics
.align 4
ClearScreenOBJ:
;[v0.9.2 overlay: excluded, ours wins / decision item] 	.incbin asm/bin/graphics/clearscreen/1clearscreenobj.bin
.align 4
;Level select assests (When you select a stage within a world)
Level1SelectAssetsOBJ:
	.incbin asm/bin/graphics/levelselectobj/1levelselectobj.bin
.align 4
Level2SelectAssetsOBJ:
	.incbin asm/bin/graphics/levelselectobj/2levelselectobj.bin
.align 4
Level3SelectAssetsOBJ:
	.incbin asm/bin/graphics/levelselectobj/3levelselectobj.bin
.align 4
Level4SelectAssetsOBJ:
	.incbin asm/bin/graphics/levelselectobj/4levelselectobj.bin
.align 4
Level5SelectAssetsOBJ:
	.incbin asm/bin/graphics/levelselectobj/5levelselectobj.bin
.align 4
Level6SelectAssetsOBJ:
	.incbin asm/bin/graphics/levelselectobj/6levelselectobj.bin
.align 4
Level7SelectAssetsOBJ:
	.incbin asm/bin/graphics/levelselectobj/7levelselectobj.bin
.align 4
Level8SelectAssetsOBJ:
	.incbin asm/bin/graphics/levelselectobj/8levelselectobj.bin
.align 4
Level9SelectAssetsOBJ:
	.incbin asm/bin/graphics/levelselectobj/9levelselectobj.bin
.align 4
Level10SelectAssetsOBJ:
	.incbin asm/bin/graphics/levelselectobj/10levelselectobj.bin
.align 4
Level11SelectAssetsOBJ:
	.incbin asm/bin/graphics/levelselectobj/11levelselectobj.bin
.align 4
;Staff Roll Screen Objects
GameLogoOBJ:
;[v0.9.2 overlay: excluded, ours wins / decision item] 	.incbin asm/bin/graphics/staffroll/1gamelogoobj.bin
.align 4
MoeChildhoodLogoOBJ:
	.incbin asm/bin/graphics/staffroll/2moechildhoodlogoobj.bin
;Post Credits Screen
.align 4
PostCredScreenOBJ:
	.incbin asm/bin/graphics/postcreditscreen/1congratsobj.bin
.align 4
ExitChest:
	.incbin asm/bin/graphics/exitchest/1exitchest.bin

.endarea

;----------------------------------------------------------
;TitleScreen Graphics
;(Important must leave them in the order shown!)
;Only Titlecreen has changeable pointers!
;Other files in this particular section don't!


Titlescreen:
;[v0.9.2 overlay: excluded, ours wins / decision item] .org 0x088F6B3C
;[v0.9.2 overlay: excluded, ours wins / decision item] 	.incbin asm/bin/graphics/titlescreen/1titlescreenbg.bin
	
SuspendsaveMesg:
.org 0x088FA308
	.incbin asm/bin/graphics/titlescreen/2filemessagebg.bin

TitlescreenOBJ:
;[v0.9.2 overlay: excluded, ours wins / decision item] .org 0x0890294C
;[v0.9.2 overlay: excluded, ours wins / decision item] 	.incbin asm/bin/graphics/titlescreen/3titlescreenobj.bin

TitlescreenBGPal:
;[v0.9.2 overlay: excluded, ours wins / decision item] .org 0x08956518
;[v0.9.2 overlay: excluded, ours wins / decision item] 	.incbin asm/bin/graphics/titlescreen/4titlescreenpalbg.bin


TitlescreenLogoTilemap: ;162 tiles for the title logo itself
;[v0.9.2 overlay: excluded, ours wins / decision item] .org 0x089568E0
;[v0.9.2 overlay: excluded, ours wins / decision item] 	.incbin asm/bin/graphics/titlescreen/6titlescreenlogotilemap.bin

TitlescreenLetterForegroundOAM:
;[v0.9.2 overlay: excluded, ours wins / decision item] .org 0x08957194
;[v0.9.2 overlay: excluded, ours wins / decision item] 	.incbin asm/bin/graphics/titlescreen/OAM/1letterforegroundOAM.bin

TitlescreenLetterBackgroundOAM:
;[v0.9.2 overlay: excluded, ours wins / decision item] .org 0x089574C8
;[v0.9.2 overlay: excluded, ours wins / decision item] 	.incbin asm/bin/graphics/titlescreen/OAM/2backgroundOAM.bin

SuspendSaveMesgTilemap:	;This is uncompressed normally!!!!
.org 0x08956F00
	.incbin asm/bin/graphics/titlescreen/2filemessagetilemap.bin
;----------------------------------------------------------	
	
	
	
	
	
;-------------------------------Palettes(Uncompressed)
;World 5-3 Fruits

;Served only for other translations if needed
;Banana_Pal:
;.org 0x087EDFF8

Eggplant_Pal:
.org 0x087EE0C4
	.incbin asm/bin/graphics/Food_Puzzle/Replacements/Eggplant_Replacement/1EggplantToApplePal.bin

Melon_Pal:
.org 0x088308A4
	.incbin asm/bin/graphics/Food_Puzzle/Replacements/Melon_Replacement/1MelonToEggplantPal.bin

Pumpkin_Pal:
.org 0x087EE19C
	.incbin asm/bin/graphics/Food_Puzzle/Replacements/Pumpkin_Replacement/1PumpkinToTomatoPal.bin

Cucumber_Pal:
.org 0x087EE31C
	.incbin asm/bin/graphics/Food_Puzzle/Replacements/Cucumber_Replacement/1CucumberToPumpkinPal.bin
	
Apple_Pal:
.org 0x0883098C
	.incbin asm/bin/graphics/Food_Puzzle/Replacements/Apple_Replacement/1AppleToNutsPal.bin
	
Persimmon_Pal:
.org 0x087EE264
	.incbin asm/bin/graphics/Food_Puzzle/Replacements/Persimmon_Replacement/1PersimmonToTurnipPal.bin
	
Shell_Pal:
.org 0x087EE400
	.incbin asm/bin/graphics/Food_Puzzle/Replacements/Shell_Replacement/1ShellToTumericPal.bin
	
Squid_Pal:
.org 0x087EE4D8
	.incbin asm/bin/graphics/Food_Puzzle/Replacements/Squid_Replacement/1SquidToCarrotPal.bin
	
Food_Sign_Pal:
.org 0x0881E1A8
	.incbin asm/bin/graphics/Food_Puzzle/Replacements/Food_Sign_Replacement/1Food_SignsPal.bin
	
;Staff Roll Game Logo
GamelogoPal1:
;[v0.9.2 overlay: excluded, ours wins / decision item] .org 0x086A2288
;[v0.9.2 overlay: excluded, ours wins / decision item] 	.incbin asm/bin/graphics/staffroll/1gamelogopal.bin
GamelogoPal2:
;[v0.9.2 overlay: excluded, ours wins / decision item] .org 0x086A22A8
;[v0.9.2 overlay: excluded, ours wins / decision item] 	.incbin asm/bin/graphics/staffroll/2gamelogopal.bin

;-------------------------------OAM

;--Game Over Screen
;Currently unused for ENG Fan Translation but can be used
;for other translations if needed.
;Continue Display
;.org 0x083E9B66
;	.incbin asm/bin/graphics/GameOver/OAM/1Continue.bin
;End Display
;.org 0x083E9B72
;	.incbin asm/bin/graphics/GameOver/OAM/2End.bin

;---Tutorial signs
;SwimmingSign
.org 0x082E47EA
	.incbin asm/bin/graphics/tutorial_signs/swimming/OAM/1swimmingoam.bin
	
;TurboSwimSign
.org 0x082E4B0A
	.incbin asm/bin/graphics/tutorial_signs/turbo_swim/OAM/1turboswimoam.bin
	
;SurfJumpSign
.org 0x082E4E0A
	.incbin asm/bin/graphics/tutorial_signs/surf_jump/OAM/1surfjumpoam.bin
	
;WalkingSign
.org 0x082E505E
	.incbin asm/bin/graphics/tutorial_signs/walking/OAM/1walkingoam.bin
	
;DuckSign
.org 0x082E52BA
	.incbin asm/bin/graphics/tutorial_signs/duck/OAM/1duckoam.bin
	
;JumpSign
.org 0x082E552A
	.incbin asm/bin/graphics/tutorial_signs/jump/OAM/1jumpoam.bin

;DashSign
.org 0x082E579E
	.incbin asm/bin/graphics/tutorial_signs/dash/OAM/1dashoam.bin

;DashJumpSign
.org 0x082E5ABE
	.incbin asm/bin/graphics/tutorial_signs/dash_jump/OAM/1dashjumpoam.bin

;SlideSign
.org 0x082E5D8E
	.incbin asm/bin/graphics/tutorial_signs/slide/OAM/1slideoam.bin

;EnteringDoorsSign
.org 0x082E601A
	.incbin asm/bin/graphics/tutorial_signs/entering_doors/OAM/1enteringdoorsoam.bin

;TalkingSign
.org 0x082E62BE
	.incbin asm/bin/graphics/tutorial_signs/talking/OAM/1talkingoam.bin

;StarSpinSign
.org 0x082E6582
	.incbin asm/bin/graphics/tutorial_signs/starspin/OAM/1starspinoam.bin

;GlideSign
.org 0x082E6A82
	.incbin asm/bin/graphics/tutorial_signs/glide/OAM/1glideoam.bin

;AirJumpSign
.org 0x082E6FD2
	.incbin asm/bin/graphics/tutorial_signs/air_jump/OAM/1airjumpoam.bin

;MightyStarSpinSign
.org 0x082E72AA
	.incbin asm/bin/graphics/tutorial_signs/mighty_star_spin/OAM/1mightystarspinoam.bin

;ShootingStarSign
.org 0x082E7A4E
	.incbin asm/bin/graphics/tutorial_signs/shooting_star/OAM/1shootingstaroam.bin

;UltraStarSpinSign
.org 0x082E7752
	.incbin asm/bin/graphics/tutorial_signs/ultrastarspin/OAM/1ultrastarspinoam.bin

;BlimpSign
.org 0x082E67A2
	.incbin asm/bin/graphics/tutorial_signs/blimp/OAM/1blimpoam.bin

;JetBlimpSign
.org 0x082E7FD2
	.incbin asm/bin/graphics/tutorial_signs/jetblimp/OAM/1jetblimpoam.bin

;SeaSkaterSign
.org 0x082E6CBA
	.incbin asm/bin/graphics/tutorial_signs/sea_skater/OAM/1seaskateroam.bin

;SoarinSeaSkaterSign
.org 0x082E8242
	.incbin asm/bin/graphics/tutorial_signs/SoarinSeaSkater/OAM/1soarinseaskateroam.bin

;RyunSign
.org 0x082E748A
	.incbin asm/bin/graphics/tutorial_signs/ryun/OAM/1ryunoam.bin

;SuperRyunSign
.org 0x082E877A
	.incbin asm/bin/graphics/tutorial_signs/SuperRyun/OAM/1superryunoam.bin

;KoalaCostumeSign
.org 0x082E7D5A
	.incbin asm/bin/graphics/tutorial_signs/Koala_Costume/OAM/1koalacostumeoam.bin

;HooligatorCostumeSign
.org 0x082E8556
	.incbin asm/bin/graphics/tutorial_signs/Hooligator_Costume/OAM/1hooligatorcostumeoam.bin

;---FileSelect Screen
;Copy Message 1
.org 0x0837925C
	.incbin asm/bin/graphics/FileSelect/OAM/1CopyMessage1OAM.bin
;Copy Message 2
.org 0x083799F4
	.incbin asm/bin/graphics/FileSelect/OAM/2CopyMessage2OAM.bin

;----Minigame Select Screen
;Easy Difficulty animation
;.org 0x0834F434
;	.incbin asm/bin/graphics/minigamemenu/OAM/1EasyAnimOAM.bin

;Normal Difficulty Animation
.org 0x0834F4C0
	.incbin asm/bin/graphics/minigamemenu/OAM/2NormalAnimOAM.bin

;Hard Difficulty Animation
.org 0x0834F52E
	.incbin asm/bin/graphics/minigamemenu/OAM/3HardAnimOAM.bin

;Difficulty Cleared Icon
.org 0x0834F40C
	.incbin asm/bin/graphics/minigamemenu/OAM/4ClearedIconOAM.bin

;----MinigameHUDOBJ
;START! Pop-up (Uses 5 sprites)
.org 0x085EB10E
	.incbin asm/bin/graphics/minigamehud/OAM/1startoam.bin

;Minigame Pause Message (When NO is Highlighted) (Uses 4 sprites)
.org 0x085EAF64
	.incbin asm/bin/graphics/minigamehud/OAM/2pausemesgoam.bin

;Minigame Pause Message (When YES is Highlighted) (Uses 4 sprites)
.org 0x085EAFA4
	.incbin asm/bin/graphics/minigamehud/OAM/2pausemesgoam.bin

;Minigame After Loss Message (When YES is Highlighted) (Uses 5 Sprites)
.org 0x085EB91A
	.incbin asm/bin/graphics/minigamehud/OAM/3afterminigameoam.bin

;Minigame After Loss Message (When NO is Highlighted) (Uses 5 Sprites)
.org 0x085EB8C2
	.incbin asm/bin/graphics/minigamehud/OAM/3afterminigameoam.bin

;OUT! Pop-up (uses 4 sprites) (There is alot of frames to this... I wouldn't bother trying to modify this one)
;.org 0x085EB2BC
;	.incbin asm/bin/graphics/minigamehud/OAM/4outoam.bin

;TIME UP! Pop-up
.org 0x085EB4B4
	.incbin asm/bin/graphics/minigamehud/OAM/5timeupoam.bin

;CLEAR! Pop-up
.org 0x085EB2A6
	.incbin asm/bin/graphics/minigamehud/OAM/6clearoam.bin

;----------PausemenuOBJ
;Hint pop in Animation (Uses 3 OAM sprite data blocks)
.org 0x0863D68A
	.incbin asm/bin/graphics/pausemenu/OAM/1hintoam.bin

;Hint graphic (Uses 3 OAM sprite data blocks)
.org 0x0863D72A
	.incbin asm/bin/graphics/pausemenu/OAM/1hintoam.bin

;Stuff pop in Animation (Uses 4 OAM sprite data blocks)
.org 0x0863D88E
	.incbin asm/bin/graphics/pausemenu/OAM/2stuffoam.bin

;Stuff graphic (Uses 4 OAM sprite data blocks)
.org 0x0863D934
	.incbin asm/bin/graphics/pausemenu/OAM/2stuffoam.bin

;Key Items pop in animation (Uses 4 OAM sprite data blocks)
.org 0x0863DA8C
	.incbin asm/bin/graphics/pausemenu/OAM/3keyitemsoam.bin

;Key Items graphic (Uses 4 OAM sprite data blocks)
.org 0x0863DB38
	.incbin asm/bin/graphics/pausemenu/OAM/3keyitemsoam.bin

;Vehicle Pop in Animation (Uses 4 OAM sprite data blocks
.org 0x0863DC96
	.incbin asm/bin/graphics/pausemenu/OAM/4vehiclesignoam.bin

;Vehicle Signs graphic (Uses 4 OAM sprite data blocks)
.org 0x0863DD3C
	.incbin asm/bin/graphics/pausemenu/OAM/4vehiclesignoam.bin

;Action pop in animation (Uses 5 OAM sprite data blocks)
;[v0.9.2 overlay: excluded, ours wins / decision item] .org 0x0863DE94
;[v0.9.2 overlay: excluded, ours wins / decision item] 	.incbin asm/bin/graphics/pausemenu/OAM/5actionsignoam.bin

;Action Signs graphic (Uses 5 OAM sprite data blocks)
;[v0.9.2 overlay: excluded, ours wins / decision item] .org 0x0863DF46
;[v0.9.2 overlay: excluded, ours wins / decision item] 	.incbin asm/bin/graphics/pausemenu/OAM/5actionsignoam.bin
	
;"LEFT:" graphic (Left of the numbers) in World 1-2 and 5-4 (Here if you need it)
;[v0.9.2 overlay: excluded, ours wins / decision item] .org 0x087D3AA6
;[v0.9.2 overlay: excluded, ours wins / decision item] 	.incbin asm/bin/graphics/orbsleftgfx/OAM/1StuffLeftSignOAM.bin

;The Numbers for the "LEFT:" graphic (This also effects the Countdown timer
;such as the Blimp race in world 4-3)
;[v0.9.2 overlay: excluded, ours wins / decision item] .org 0x087D3AB6
;[v0.9.2 overlay: excluded, ours wins / decision item] 	.incbin asm/bin/graphics/orbsleftgfx/OAM/2NumbersOAM.bin

;StaffRoll GameLogo
;[v0.9.2 overlay: excluded, ours wins / decision item] .org 0x086A2722
;[v0.9.2 overlay: excluded, ours wins / decision item] 	.incbin asm/bin/graphics/staffroll/OAM/1gamelogooam.bin
;StaffRoll 2 Moe's Childhood
.org 0x086A2776
	.incbin asm/bin/graphics/staffroll/OAM/2moechildhoodoam.bin


;-------------------------------------------------------------------Pointers
;HUD Assets
.org 0x0800C65C
	.word HUDLZSS1
;-------------------------------Just in case if needed
;.org 0x08036E90
;	.word HUDLZSS2
;Second Pointer for HUDLZSS
;.org 0x0812C578
;	.word HUDLZSS2
;-------------------------------

;Title Screen Graphics (It works but the tilemaps and palettes don't load!)
;.org 0x080DC910
;	.word Titlescreen

;Game Over
.org 0x0812C530
	.word GameOverOBJ

;Moe's (Kyorosuke) House
.org 0x08133E88
	.word MoeHouseOBJ

.org 0x08133E80
	.word MoeHouseBG
	
.org 0x08133E90
	.word MoeHouseBGTileMap

.org 0x08133E98
	.word MoeHouseSelection_Tilemap1

.org 0x08133EA8
	.word MoeHouseSelection_Tilemap2
	
;FileSelect Screen
.org 0x08128630
	.word FileSelect_Object
	
.org 0x0812861C
	.word FileSelect_BG
	
.org 0x08128644
	.word FileSelect_BG_Tilemap

.org 0x08128638
	.word FileSelect_FileErasePrompt_Tilemap
	
.org 0x08128658
	.word FileSelect_CopyAndErasePopup_Tilemap
	
;Tutorial signs
.org 0x0814EC28
	.word TutorialSignSwimming
	
.org 0x0814EC38
	.word TutorialSignTurboSwim
	
.org 0x0814EC48
	.word TutorialSignSurfJump
	
.org 0x0814EC58
	.word TutorialSignWalking
	
.org 0x0814EC68
	.word TutorialSignDuck
	
.org 0x0814EC78
	.word TutorialSignJump

.org 0x0814EC88
	.word TutorialSignDash

.org 0x0814EC98
	.word TutorialSignDashJump

.org 0x0814ECA8
	.word TutorialSignSlide

.org 0x0814ECB8
	.word TutorialSignEnteringDoors

.org 0x0814ECC8
	.word TutorialSignTalking

.org 0x0814ECD8
	.word TutorialSignStarSpin

.org 0x0814ECF8
	.word TutorialSignGlide

.org 0x0814ED18
	.word TutorialSignAirJump

.org 0x0814ED28
	.word TutorialSignMightyStarSpin

.org 0x0814ED58
	.word TutorialSignShootingStar

.org 0x0814ED48
	.word TutorialSignUltraStarSpin

.org 0x0814ECE8
	.word TutorialSignBlimp

.org 0x0814ED78
	.word TutorialSignJetBlimp

.org 0x0814ED08
	.word TutorialSignSeaSkater

.org 0x0814ED88
	.word TutorialSignSoarinSeaSkater

.org 0x0814ED38
	.word TutorialSignRyun

.org 0x0814EDA8
	.word TutorialSignSuperRyun

.org 0x0814ED68
	.word TutorialSignKoalaCostume

.org 0x0814ED98
	.word TutorialSignHooligatorCostume
	
;World 1-3 Lovelyshop
;[v0.9.2 overlay: excluded, ours wins / decision item] .org 0x082A7DE4
;[v0.9.2 overlay: excluded, ours wins / decision item] 	.word LovelyShop1_3
	
;World 1-3 Lovely's Pamphlet
.org 0x082A7DB4
	.word LovelyPamphlet

;World 5-3 Fruits
;---------------------------------------------
;Served only for other translations if needed
;.org 0x082A8774
;	.word Banana_Replacement
;---------------------------------------------
.org 0x082A878C
	.word Eggplant_Replacement
	
.org 0x082A87BC
	.word Pumpkin_Replacement
	
.org 0x082A87D4
	.word Persimmon_Replacement

.org 0x082A87EC
	.word Cucumber_Replacement
	
.org 0x082A881C
	.word Shell_Replacement
	
.org 0x082A8834
	.word Squid_Replacement
	
.org 0x082A87A4
	.word Melon_Replacement
	
.org 0x082A8804
	.word Apple_Replacement
	
.org 0x082AAB74
	.word Food_Sign_Replacement
	
;World 5-4 Mole Poster
.org 0x082A88AC
	.word Mole_Message

;World Selection Screen Assets
.org 0x0810FAD4
	.word WorldSelectOBJ
	
;Stuff Screens Graphics
.org 0x08109724
	.word StuffScreenBG
.org 0x08109768
	.word StuffScreenOBJ
;Book Screen
.org 0x08130B5C
	.word BookScreenOBJ
.org 0x08130B48
	.word BookScreenBG
.org 0x08130B78
	.word BookScreenBGTilemap
;Stuff Screen Outfit and Accessory updates
.org 0x082C5558
	.word BoxOutfit
.org 0x082C718C
	.word BoxOutfit
.org 0x082C55E8
	.word BaseballcapAcessory
.org 0x082C721C
	.word BaseballcapAcessory
.org 0x082C539C
	.word BaseballUniformOutfit
.org 0x082C6FD0
	.word BaseballUniformOutfit
.org 0x082C54A4
	.word WrestlingLeotardOutfit
.org 0x082C70D8
	.word WrestlingLeotardOutfit
.org 0x082C5528
	.word SwimsuitOutfit
.org 0x082C715C
	.word SwimsuitOutfit
.org 0x082C5564
	.word MotorJacketOutfit
.org 0x082C7198
	.word MotorJacketOutfit
;LovelyShop Graphics
.org 0x0813854C
	.word LovelyShopBG

.org 0x08138558
	.word LovelyShopOBJ

;Treasure Screen Graphics
.org 0x081401D4
	.word TreasureScreenBG

.org 0x081401F0
	.word TreasureScreenTilemap

.org 0x081401E0
	.word TreasureScreenObj

;Photo Screen Graphics
.org 0x0810C91C
	.word PhotoBG

.org 0x0810CCE4
	.word PhotoOBJ

.org 0x0810C93C
	.word PhotoTilemap

;Sea Jams Graphics
.org 0x0813E4C4
	.word SeaJamsBG

.org 0x0813E4D4
	.word SeaJamsOBJ

;Minigame Menu Graphics
.org 0x080E87D0
	.word MinigameMenuAssets

;MinigameHUD Graphics
;MinigameHUDBG
.org 0x080F8CF0
	.word MinigameHUDBG

.org 0x080FB2A8
	.word MinigameHUDBG

.org 0x080FD6F4
	.word MinigameHUDBG

.org 0x08100310
	.word MinigameHUDBG

.org 0x08101D88
	.word MinigameHUDBG

;MinigameHUDOBJ
.org 0x080F8D08
	.word MinigameHUDOBJ

.org 0x080FB2C0
	.word MinigameHUDOBJ

.org 0x080FD70C
	.word MinigameHUDOBJ

.org 0x08100328
	.word MinigameHUDOBJ

.org 0x08101DA0
	.word MinigameHUDOBJ

;ColorMatcherOBJ
.org 0x080F8D3C
	.word ColorMatcherOBJ

;PauseMenuBG
.org 0x08104578
	.word PausemenuBG

;PauseMenuOBJ
.org 0x08104A18
	.word PausemenuOBJ
	
;PauseMenuTilemap
.org 0x08104A08
	.word PausemenuTilemap
	
;ClearScreenOBJ
;[v0.9.2 overlay: excluded, ours wins / decision item] .org 0x08121EB8
;[v0.9.2 overlay: excluded, ours wins / decision item] 	.word ClearScreenOBJ
	
;------------------------------------------------------------------------
;Level Select pointers for the "Select" button prompt on stage selection 1-11 screen for each world
;------------------------------------------------------------------------
.org 0x080E11BC
	.word Level1SelectAssetsOBJ
.org 0x080E12E4
	.word Level1SelectAssetsOBJ
.org 0x080E14F4
	.word Level1SelectAssetsOBJ
.org 0x080E1668
	.word Level1SelectAssetsOBJ
.org 0x080E1814
	.word Level1SelectAssetsOBJ
.org 0x080E1AF8
	.word Level1SelectAssetsOBJ
.org 0x080E1D40
	.word Level1SelectAssetsOBJ
.org 0x080E1EE8
	.word Level1SelectAssetsOBJ
.org 0x080E212C
	.word Level1SelectAssetsOBJ
.org 0x080E24A0
	.word Level1SelectAssetsOBJ
.org 0x080E26FC
	.word Level1SelectAssetsOBJ
.org 0x080E2898
	.word Level1SelectAssetsOBJ
.org 0x080E29D8
	.word Level1SelectAssetsOBJ
.org 0x080E2BE8
	.word Level1SelectAssetsOBJ
.org 0x080E2D98
	.word Level1SelectAssetsOBJ
.org 0x080E2F58
	.word Level1SelectAssetsOBJ
.org 0x080E323C
	.word Level1SelectAssetsOBJ
.org 0x080E3484
	.word Level1SelectAssetsOBJ
.org 0x080E362C
	.word Level1SelectAssetsOBJ
.org 0x080E3870
	.word Level1SelectAssetsOBJ
.org 0x080E3BE4
	.word Level1SelectAssetsOBJ
.org 0x080E3E40
	.word Level1SelectAssetsOBJ
;---------------------------------------------------------------

;World 2 Level Select OBJ Assets
.org 0x080E12D4
	.word Level2SelectAssetsOBJ
.org 0x080E29C8
	.word Level2SelectAssetsOBJ

;World 3 Level Select OBJ Assets
.org 0x080E14E4
	.word Level3SelectAssetsOBJ
.org 0x080E2BD8
	.word Level3SelectAssetsOBJ
	
;World 4 Level Select OBJ Assets
.org 0x080E1658
	.word Level4SelectAssetsOBJ
.org 0x080E2D88
	.word Level4SelectAssetsOBJ

;World 5 Level Select OBJ Assets
.org 0x080E1804
	.word Level5SelectAssetsOBJ
.org 0x080E2F48
	.word Level5SelectAssetsOBJ

;World 6 Level Select OBJ Assets
.org 0x080E1AE8
	.word Level6SelectAssetsOBJ
.org 0x080E322C
	.word Level6SelectAssetsOBJ

;World 7 Level Select OBJ Assets
.org 0x080E1D30
	.word Level7SelectAssetsOBJ
.org 0x080E3474
	.word Level7SelectAssetsOBJ
	
;World 8 Level Select OBJ Assets
.org 0x080E1ED8
	.word Level8SelectAssetsOBJ
.org 0x080E361C
	.word Level8SelectAssetsOBJ
	
;World 9 Level Select OBJ Assets
.org 0x080E211C
	.word Level9SelectAssetsOBJ
.org 0x080E3860
	.word Level9SelectAssetsOBJ

;World 10 Level Select OBJ Assets
.org 0x080E2490
	.word Level10SelectAssetsOBJ
.org 0x080E3BD4
	.word Level10SelectAssetsOBJ
	
;World 11 Level Select OBJ Assets

.org 0x080E26EC
	.word Level11SelectAssetsOBJ
.org 0x080E3E30
	.word Level11SelectAssetsOBJ
	
;Exit Chest for post game levels
.org 0x082A7CF4
	.word ExitChest

;StaffRoll Screen
;Game Logo
;[v0.9.2 overlay: excluded, ours wins / decision item] .org 0x08114838
;[v0.9.2 overlay: excluded, ours wins / decision item] 	.word GameLogoOBJ
;[v0.9.2 overlay: excluded, ours wins / decision item] .org 0x082C7EB4
;[v0.9.2 overlay: excluded, ours wins / decision item] 	.word GameLogoOBJ
;[v0.9.2 overlay: excluded, ours wins / decision item] .org 0x082C7F44
;[v0.9.2 overlay: excluded, ours wins / decision item] 	.word GameLogoOBJ
;Moe's Childhood Logo
.org 0x08114978
	.word MoeChildhoodLogoOBJ


;PostCreditScreen
.org 0x082C7F38
	.word PostCredScreenOBJ

;World 4-3 Goal Flag
;[v0.9.2 overlay: excluded, ours wins / decision item] .org 0x082A94C4
;[v0.9.2 overlay: excluded, ours wins / decision item] 	.word Goalflag4_3

;World 1-2 Orb Countdown OBJ Assets (POINTER DOES NOT WORK DO NOT CHANGE)
;.org 0x0803BB80
;	.word OrbsleftOBJ


;--------------------Misc. Stuff that was uncompressed
;This total sign was uncompressed!
.org 0x082EED00
TOTALUNCOMP:
	.incbin asm/bin/graphics/Health/1TotalUncomp.bin


HUDLZSS2:
.org 0x082ED240
	.incbin asm/bin/graphics/Health/2HUDLZSS.bin

;----Minigame HUD
MinigameHUDTilemap:
.org 0x08604812
	.incbin asm/bin/graphics/minigamehud/1minigamehudtilemap.bin

;World 1-2 and World 5-4 Orb Countown
OrbsleftOBJ:
;[v0.9.2 overlay: excluded, ours wins / decision item] .org 0x087D3E58
;[v0.9.2 overlay: excluded, ours wins / decision item] 	.incbin asm/bin/graphics/orbsleftgfx/1orbsleftgfx.bin
	
;----FileSelect Stage Nametag Tile ID's and size
;First value is the length of the tag. Change it to increase or decrease the size of the tag.
;Third and fourth is the location of the first Part of the tag.
;The Location is the Tile ID in hex in reverse
;In example Lobber's Cave's first part of the tag is at Tile 0180 in hex. (or Tile #384 in decimal)

;Lobber's Cave Nametag for FileSelect
.org 0x082C9580
	.byte 0x07,0x00,0x80,0x01

;Gluglug Lagoon's Nametag for FileSelect
.org 0x082C9584
	.byte 0x08,0x00,0xA0,0x01

;Shelltop Islands' Nametag for FileSelect
.org 0x082C9588
	.byte 0x08,0x00,0xC0,0x01
	
;Slippery Glasier's Nametag for FileSelect
.org 0x082C958C
	.byte 0x08,0x00,0xE0,0x01

;Jumbowood Forest's Nametag for FileSelect
.org 0x082C9590
	.byte 0x0A,0x00,0x00,0x02
;Pitch Black Caverns' Nametag for FileSelect
.org 0x082C9594
	.byte 0x0A,0x00,0x20,0x02
;Yodel-Lay-Hee Heights' Nametag for FileSelect
.org 0x082C9598
	.byte 0x0A,0x00,0x8A,0x01
;Pufftop's Nametag for FileSelect
.org 0x082C959C
	.byte 0x05,0x00,0xAA,0x01
;Loch Ress' Nametag for FileSelect
.org 0x082C95A0
	.byte 0x06,0x00,0xCA,0x01
;Torrential Falls' Nametag for FileSelect
.org 0x082C95A4
	.byte 0x09,0x00,0xEA,0x01
;Ogura's Castle Nametag for FileSelect
.org 0x082C95A8
	.byte 0x08,0x00,0x0A,0x02
;Unknown Tag's Nametag settings for FileSelect
.org 0x082C95AC
	.byte 0x06,0x00,0x2A,0x02
;Nametag for FileSelect

.close

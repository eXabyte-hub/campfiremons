# Campfiremons

A Cobblemon modpack for our friend group: catch, explore and battle your way through the Radical Red gym
challenge on Minecraft 1.21.1. Built on the
[Cobblemon Official Modpack](https://modrinth.com/modpack/cobblemon-neoforge).

## Installing

You need [Prism Launcher](https://prismlauncher.org/) (Windows, macOS or Linux) and a Microsoft account that owns
Minecraft Java Edition.

1. Install Prism and sign in with your Microsoft account.
2. Download `Campfiremons.zip` from the
   [latest release](https://github.com/eXabyte-hub/campfiremons/releases/latest).
3. In Prism: **Add Instance → Import**, pick the zip.
4. Press **Play**. The first time, a window downloads about 200 mods, so give it a few minutes.

You only do this once. Every time you press Play, the pack updates itself before the game starts.

The Modrinth App and the CurseForge app aren't supported: some mods are CurseForge-only, and the auto-updater runs
through Prism.

## Joining the server

Ask whoever runs the server for the address and to be added to the whitelist, then use **Multiplayer → Add Server** in game.

## How the pack plays

- **Gyms are the progression.** Beating each Radical Red gym leader moves you to the next stage (8 gyms, then the
  Elite Four and Champion). The quest book has a chapter for every stage, plus guide chapters (getting started,
  evolution, Poké Balls, battle gimmicks, training, raids, archaeology and fishing), a checklist of every legendary,
  Ultra Beast and Paradox Pokémon, and chapters for the big mods (Create, Oritech, storage, relics, artifacts, gear).
- **Dying** leaves a grave with your items where you fell: walk back and open it.
- **Creepers** still explode and hurt, but don't break blocks.
- **Farming:** right-click a grown crop to harvest it; it replants itself.
- **Vein mining:** hold the Ultimine key (` by default, change it in Controls) while you mine to break a whole
  ore vein or tree at once.
- **You start in Pallet Town.** New worlds (and the server) put the spawn in the nearest Pallet Town, so that's
  where you begin and where you come back to without a bed.
- **Finding your next gym:** you get a map to it when you first join and after every gym win, with the distance and
  direction in chat. Lost it? Type `/gymmap`. The last three gyms are in the Nether and the End: you get directions
  once you're there.
- **Level cap.** Your Pokémon stop gaining EXP at the level of your next big fight, and trainers won't battle you
  while a party Pokémon is over the cap. You can catch anything at any level; box the over-levelled ones before a
  trainer battle.
- **Legendaries unlock by stage:** sub-legendaries at Stage 5, Ultra Beasts and Paradox Pokémon at 6, mythicals and
  box legends at 7. Before that you can't battle or catch them.
- **Gear unlocks by stage.** Better balls, Bottle Caps, TMs and the PokéNav can be crafted any time but only used
  once you reach their stage. Mega Bracelets, Z-Rings, Tera Orbs and other power items turn up in structure chests
  after the gym that unlocks them, and every player gets their own copy of the loot.
- **Out in the world:** Pokécenters and PokéStops heal your team and have a PC; rare Poké Labs hold extra loot.
  Pokémon towns (Pallet, Lavender, Twinleaf and more) have their own Pokécenters, Pokémarts and Pokémon, and the
  Kanto cities (Pewter to Cinnabar, plus the Indigo Plateau) have landmark buildings, shops, trainers and townsfolk.
  Their gym leaders are the Radical Red ones: talk to them for the same badge battle as at the Radical Red gyms.
  Sophisticated Backpacks can take PC and healing upgrades so you can do both on the go. Waystones (some in villages)
  let you teleport between the ones you've found, and Ping Wheel marks a spot or a Pokémon for your friends.
- **Pokémon at home:** Pokémon in a pasture produce items (wool, eggs and more), and wild Pokémon show whether
  you've caught their species yet. Your PC has 60 boxes.
- **Livelier Pokémon and towns:** about 200 Pokémon get new idle, walking and attack animations (CobbleMotion),
  and villagers look like people from the Pokémon games, Nurse Joy included (CobbleFolk).
- **Sounds:** Pokémon battle themes for wild, trainer and PvP battles, the games' cries, and Pokémon music for every
  biome, the title screen, the Nether and the End (CobbleSounds).
- **Side activities:** Raid Dens open star by star as you progress, the Battle Tower opens at Stage 4, Ultra Space at
  Stage 6. The Master Ball is the Champion's reward.

## Tips and troubleshooting

- **The first Play stops with an error about the pre-launch command:** press Play again.
- **Memory:** the instance asks for 8 GB. With 16 GB of RAM or less, lower it to 6 GB in
  **Edit → Settings → Java**.
- **Shaders** (Complementary Reimagined) are on by default. On a weaker PC, press **K** to toggle them, or turn them
  off under **Options → Video Settings → Shader Packs**.
- **Distant Horizons** draws terrain far past your render distance. On a weaker PC, turn it down or off with its
  button in **Options → Video Settings**. On the server it shows terrain you've already been near.
- **The Pokémon music is a 418 MB download.** The updater asks once which optional files you want: untick
  **CobbleSounds Soundtrack** to skip it and keep Minecraft's music. To change your mind later, press **Optional
  mods...** in the update window that shows when you press Play.
- **Your own files are safe.** The updater only touches the pack's own files, so your settings, resource packs and
  shaders stay as you left them.
- **Sorting and moving items:** every chest and your own inventory get search, sort and transfer buttons, and the
  sort key sorts whatever is under your mouse (your hotbar stays as it is). Sophisticated Item Actions adds keys that
  highlight nearby chests holding an item and deposit into or restock from them without opening anything. Find and
  change the keys in **Options → Controls → Key Binds** (search "sophisticated").

## Mod list

<!-- modlist:start -->
<details>
<summary>All 199 mods, plus resource packs and shaders (click to open)</summary>

Generated from the pack files by `tools/gen_modlist.py`. "Client only" mods are only on players' computers, "server only" ones only on the server.

### Mods (199)

| Name | Notes | From |
| --- | --- | --- |
| [[EMF] Entity Model Features](https://modrinth.com/project/4I1XuqiY) | client only | Modrinth |
| [[ETF] Entity Texture Features](https://modrinth.com/project/BVzZfTc1) | client only | Modrinth |
| [Accessories](https://modrinth.com/project/jtmvUHXj) |  | Modrinth |
| [Advanced Core Info (ACI)](https://modrinth.com/project/BaR4ijFC) |  | Modrinth |
| [Advanced Loot Info (ALI)](https://modrinth.com/project/PEPVViac) |  | Modrinth |
| [Advancement Plaques](https://modrinth.com/project/9NM0dXub) | client only | Modrinth |
| [Almanac](https://modrinth.com/project/Gi02250Z) |  | Modrinth |
| [Ambient Environment](https://modrinth.com/project/DyTvM1dv) | client only | Modrinth |
| [Amendments](https://modrinth.com/project/6iTJugQR) |  | Modrinth |
| [AppleSkin](https://modrinth.com/project/EsAfCjCV) |  | Modrinth |
| [Architectury API](https://modrinth.com/project/lhGA9TYQ) |  | Modrinth |
| [Artifacts](https://modrinth.com/project/P0Mu4wcQ) |  | Modrinth |
| [Athena](https://modrinth.com/project/b1ZV3DIJ) | client only | Modrinth |
| [Bad Wither No Cookie - Reloaded](https://modrinth.com/project/lL2MtE37) | client only | Modrinth |
| [Balm](https://modrinth.com/project/MBAkmtvl) |  | Modrinth |
| [Berry Harvester](https://modrinth.com/project/wZks2uy6) |  | Modrinth |
| [Better Advanced Tooltips](https://modrinth.com/project/iHLDc0eo) |  | Modrinth |
| [Better Advancements](https://modrinth.com/project/Q2OqKxDG) | client only | Modrinth |
| [Better Ping Display [Forge/NeoForge]](https://modrinth.com/project/ZvaHbwoZ) | client only | Modrinth |
| [Better Third Person](https://modrinth.com/project/G1s2WpNo) | client only | Modrinth |
| [Better Tooltips](https://modrinth.com/project/Z7rKZJ8k) | client only | Modrinth |
| [BisectHosting Server Integration Menu](https://modrinth.com/project/yWSAtnfH) | client only | Modrinth |
| [Bookshelf](https://modrinth.com/project/uy4Cnpcm) |  | Modrinth |
| [Building Gadgets](https://www.curseforge.com/projects/298187) |  | CurseForge |
| [Catch Indicator [Cobblemon Addon]](https://modrinth.com/project/tpTcu2PM) | client only | Modrinth |
| [Chipped](https://modrinth.com/project/BAscRYKm) |  | Modrinth |
| [Chunky](https://modrinth.com/project/fALzjamp) | server only | Modrinth |
| [CIT Resewn](https://modrinth.com/project/otVJckYQ) | client only | Modrinth |
| [CITResewnNeoPatcher](https://modrinth.com/project/yYE9h4iu) | client only | Modrinth |
| [Cloth Config API](https://modrinth.com/project/9s6osm5g) |  | Modrinth |
| [Clumps](https://modrinth.com/project/Wnxd13zP) |  | Modrinth |
| [CobbleDollars [Cobblemon Addon]](https://modrinth.com/project/s7N7AsqL) |  | Modrinth |
| [CobbleFurnies](https://modrinth.com/project/AXY1OO9m) |  | Modrinth |
| [Cobbleloots: Loot Balls and More!](https://modrinth.com/project/kcudYghD) |  | Modrinth |
| [Cobblemon](https://modrinth.com/project/MdwFAVRL) |  | Modrinth |
| [Cobblemon : Poke Labs](https://modrinth.com/project/Wk0xZVPQ) |  | Modrinth |
| [Cobblemon : Simple Pokecenter's](https://modrinth.com/project/9U50uRY3) |  | Modrinth |
| [Cobblemon Battle Extras](https://modrinth.com/project/2iY8VFqL) |  | Modrinth |
| [Cobblemon Battle Tower](https://modrinth.com/project/v19DG9nW) |  | Modrinth |
| [Cobblemon Capture XP](https://modrinth.com/project/LBl4Qguc) |  | Modrinth |
| [Cobblemon Catch Rate Display](https://modrinth.com/project/vADO40xp) |  | Modrinth |
| [Cobblemon Cities & Structures](https://modrinth.com/project/IqCPvv9e) |  | Modrinth |
| [Cobblemon Pasture Loot](https://modrinth.com/project/XP2jcAo0) |  | Modrinth |
| [Cobblemon PokeNav](https://modrinth.com/project/bI8Nt3uA) |  | Modrinth |
| [Cobblemon Quests Reloaded](https://modrinth.com/project/agTMcrPN) |  | Modrinth |
| [Cobblemon Raid Dens](https://modrinth.com/project/GebWh45l) |  | Modrinth |
| [Cobblemon Spawn Notification](https://modrinth.com/project/LPuJjiQz) |  | Modrinth |
| [Cobblemon Tim Core](https://modrinth.com/project/lVP9aUaY) |  | Modrinth |
| [Cobblemon Ultra-Beasts](https://www.curseforge.com/projects/1333072) |  | CurseForge |
| [Cobblemon: Armory](https://modrinth.com/project/2GSJkNsi) |  | Modrinth |
| [Cobblemon: Create Industries (3D Production Models)](https://modrinth.com/project/7BX9lbH9) |  | Modrinth |
| [Cobblemon: Extra Structures](https://modrinth.com/project/IkJ2gbjT) |  | Modrinth |
| [Cobblemon: Legendary Monuments (CB 1.8 Version Out)](https://modrinth.com/project/m6RyHSbV) |  | Modrinth |
| [Cobblemon: Mega Showdown](https://modrinth.com/project/SszvX85I) |  | Modrinth |
| [Cobblemon: Poke Stops](https://modrinth.com/project/HiwZaUgN) |  | Modrinth |
| [Cobblemon: SafePastures](https://modrinth.com/project/qpe01spE) |  | Modrinth |
| [Cobblemon: Trainers Backpack](https://modrinth.com/project/7m9uI5ma) |  | Modrinth |
| [Cobblemore Lib](https://modrinth.com/project/VYP2vmDS) |  | Modrinth |
| [Cobbleworkers](https://modrinth.com/project/i3XVG2gn) |  | Modrinth |
| [Cobbreeding](https://modrinth.com/project/ItmVb4zY) |  | Modrinth |
| [Complete Cobblemon Collection](https://modrinth.com/project/qoL4kNxC) |  | Modrinth |
| [Configurable](https://modrinth.com/project/lGffrQ3O) |  | Modrinth |
| [Connected Glass](https://modrinth.com/project/DghO0R02) |  | Modrinth |
| [Controlling](https://modrinth.com/project/xv94TkTM) | client only | Modrinth |
| [Crafting Tweaks](https://modrinth.com/project/DMu0oBKf) |  | Modrinth |
| [CraftPresence](https://modrinth.com/project/DFqQfIBR) | client only | Modrinth |
| [CraterLib](https://modrinth.com/project/Nn8Wasaq) | server only | Modrinth |
| [Create](https://modrinth.com/project/LNytGWDc) |  | Modrinth |
| [Create Contraption Terminals](https://modrinth.com/project/gOPAFzp0) |  | Modrinth |
| [Create Crafts & Additions](https://modrinth.com/project/kU1G12Nn) |  | Modrinth |
| [Create Deco](https://modrinth.com/project/sMvUb4Rb) |  | Modrinth |
| [Create: Copycats+](https://modrinth.com/project/UT2M39wf) |  | Modrinth |
| [Create: Klinks n' Klangs](https://modrinth.com/project/AS2XNT4R) |  | Modrinth |
| [Curios API](https://modrinth.com/project/vvuO3ImH) |  | Modrinth |
| [Default Options](https://modrinth.com/project/WEg59z5b) | client only | Modrinth |
| [Distant Horizons](https://modrinth.com/project/uCdwusMi) | client only | Modrinth |
| [Dynamic Crosshair](https://modrinth.com/project/ZcR9weSm) | client only | Modrinth |
| [EMI](https://modrinth.com/project/fRiHVvU7) |  | Modrinth |
| [EMI Enchanting](https://modrinth.com/project/wbWoo11W) | client only | Modrinth |
| [EMI Ores](https://modrinth.com/project/sG4TqDb8) |  | Modrinth |
| [EMI professions (EMIP)](https://modrinth.com/project/LGVihYcz) | client only | Modrinth |
| [Enchantment Descriptions](https://modrinth.com/project/UVtY3ZAC) |  | Modrinth |
| [Enhanced Attack Indicator](https://modrinth.com/project/eTy17BBS) | client only | Modrinth |
| [Entity Culling](https://modrinth.com/project/NNAgCjsB) | client only | Modrinth |
| [Falling Leaves (NeoForge/Forge)](https://modrinth.com/project/2JAUNCL4) | client only | Modrinth |
| [FancyMenu](https://modrinth.com/project/Wq5SjeWM) |  | Modrinth |
| [FerriteCore](https://modrinth.com/project/uXXizFIs) |  | Modrinth |
| [Forgified Fabric API](https://modrinth.com/project/Aqlf1Shp) |  | Modrinth |
| [FramedBlocks](https://modrinth.com/project/wbgfS34j) |  | Modrinth |
| [FTB Library (NeoForge)](https://www.curseforge.com/projects/404465) |  | CurseForge |
| [FTB Quests (NeoForge)](https://www.curseforge.com/projects/289412) |  | CurseForge |
| [FTB Teams (NeoForge)](https://www.curseforge.com/projects/404468) |  | CurseForge |
| [FTB Ultimine (NeoForge)](https://www.curseforge.com/projects/386134) |  | CurseForge |
| [Fusion (Connected Textures)](https://modrinth.com/project/p19vrgc2) | client only | Modrinth |
| [Geckolib](https://modrinth.com/project/8BmcQJ2H) |  | Modrinth |
| [GraveStone Mod](https://modrinth.com/project/RYtXKJPr) |  | Modrinth |
| [Handcrafted](https://modrinth.com/project/pJmCFF0p) |  | Modrinth |
| [Iceberg](https://modrinth.com/project/5faXoLqX) | client only | Modrinth |
| [ImmediatelyFast](https://modrinth.com/project/5ZwdcRci) | client only | Modrinth |
| [Incendium Legacy](https://modrinth.com/project/ZVzW5oNS) |  | Modrinth |
| [InvMove](https://modrinth.com/project/REfW2AEX) | client only | Modrinth |
| [InvMoveCompats](https://modrinth.com/project/6IpcGP7T) | client only | Modrinth |
| [Iris Shaders](https://modrinth.com/project/YL57xq9U) | client only | Modrinth |
| [Jade 🔍](https://modrinth.com/project/nvQzSEkH) |  | Modrinth |
| [JamLib](https://modrinth.com/project/IYY9Siz8) |  | Modrinth |
| [Just Enough Cobblemon](https://modrinth.com/project/8ZP0JLoK) |  | Modrinth |
| [Just Enough Effect Descriptions (JEED)](https://modrinth.com/project/EO27GKs1) | client only | Modrinth |
| [Just Enough Items (JEI)](https://modrinth.com/project/u6dRKJwZ) |  | Modrinth |
| [Konkrete](https://modrinth.com/project/J81TRJWm) |  | Modrinth |
| [Kotlin for Forge](https://modrinth.com/project/ordsPcFz) |  | Modrinth |
| [KryptonFoxified](https://modrinth.com/project/rmFH8I1v) |  | Modrinth |
| [KubeJS](https://modrinth.com/project/umyGl7zF) |  | Modrinth |
| [LambDynamicLights [Unofficial NeoForge]](https://modrinth.com/project/g1BboDNl) | client only | Modrinth |
| [LanguageReloadUnofficial](https://modrinth.com/project/4zpN0syd) | client only | Modrinth |
| [Let Me Despawn](https://modrinth.com/project/vE2FN5qn) |  | Modrinth |
| [Lithium](https://modrinth.com/project/gvQqBUqZ) |  | Modrinth |
| [Lithostitched](https://modrinth.com/project/XaDC71GB) |  | Modrinth |
| [Lootr](https://modrinth.com/project/EltpO5cN) |  | Modrinth |
| [Lootrmon: Lootr & Cobblemon Gilded Chest Compatibility](https://modrinth.com/project/ywwXJDli) |  | Modrinth |
| [Melody](https://modrinth.com/project/CVT4pFB2) |  | Modrinth |
| [MezzConfig](https://modrinth.com/project/7tEfOcA7) |  | Modrinth |
| [ModernFix](https://modrinth.com/project/nmDcB62a) |  | Modrinth |
| [Monsters in the Closet](https://modrinth.com/project/GMA8jFBD) |  | Modrinth |
| [Moonlight Lib](https://modrinth.com/project/twkfQtEc) |  | Modrinth |
| [MoreCobblemonTweaks](https://modrinth.com/project/5KWlJ2HC) | client only | Modrinth |
| [Mouse Tweaks](https://modrinth.com/project/aC3cM3Vq) | client only | Modrinth |
| [Mythic Upgrades](https://modrinth.com/project/ERH7cFoy) |  | Modrinth |
| [Navas ZA Megas](https://modrinth.com/project/2V1Y86sc) |  | Modrinth |
| [Neruina - Ticking Entity Fixer](https://modrinth.com/project/1s5x833P) |  | Modrinth |
| [NetherPortalFix](https://modrinth.com/project/nPZr02ET) |  | Modrinth |
| [Not Enough Animations](https://modrinth.com/project/MPCX6s5C) | client only | Modrinth |
| [Nullscape](https://modrinth.com/project/LPjGiSO4) |  | Modrinth |
| [Only Bottle Caps](https://modrinth.com/project/tDRRddpZ) |  | Modrinth |
| [Open Loader](https://modrinth.com/project/KwWsINvD) |  | Modrinth |
| [Oritech](https://modrinth.com/project/4sYI62kA) |  | Modrinth |
| [OS Cobblemon Library](https://modrinth.com/project/8hdkMUPs) |  | Modrinth |
| [oωo (owo-lib)](https://modrinth.com/project/ccKDOlHs) |  | Modrinth |
| [Packet Fixer](https://modrinth.com/project/c7m1mi73) |  | Modrinth |
| [Particle Rain](https://modrinth.com/project/nrikgvxm) |  | Modrinth |
| [Particular ✨ Reforged](https://modrinth.com/project/pYFUU6cq) | client only | Modrinth |
| [Ping Wheel](https://modrinth.com/project/QQXAdCzh) |  | Modrinth |
| [PokeBadges [Cobblemon & Pixelmon Addon]](https://modrinth.com/project/XoK0D7K2) |  | Modrinth |
| [Presence Footsteps](https://modrinth.com/project/rcTfTZr3) | client only | Modrinth |
| [Prickle](https://modrinth.com/project/aaRl8GiW) |  | Modrinth |
| [Radical Cobblemon Trainers](https://modrinth.com/project/lRwTUnD7) |  | Modrinth |
| [Radical Cobblemon Trainers API](https://modrinth.com/project/CBfM2yw7) |  | Modrinth |
| [Radical Gyms & Structures [Cobblemon]](https://modrinth.com/project/3sLJoaQH) |  | Modrinth |
| [Rechiseled](https://modrinth.com/project/B0g2vT6l) |  | Modrinth |
| [Rechiseled: Chipped](https://modrinth.com/project/ryYcxeeA) |  | Modrinth |
| [Rechiseled: Cobblemon](https://modrinth.com/project/Mqaobp5i) |  | Modrinth |
| [Reese's Sodium Options](https://modrinth.com/project/Bh37bMuy) | client only | Modrinth |
| [Refined Storage](https://modrinth.com/project/KDvYkUg3) |  | Modrinth |
| [Relics](https://www.curseforge.com/projects/445274) |  | CurseForge |
| [Reliquified Artifacts](https://www.curseforge.com/projects/1100379) |  | CurseForge |
| [Resourceful Lib](https://modrinth.com/project/G1hIVOrD) |  | Modrinth |
| [Rhino](https://modrinth.com/project/sk9knFPE) |  | Modrinth |
| [RightClickHarvest](https://modrinth.com/project/Cnejf5xM) |  | Modrinth |
| [RightClickHarvest Supplementaries Compat](https://modrinth.com/project/1UdKJCjq) |  | Modrinth |
| [Searchables](https://modrinth.com/project/fuuu3xnx) | client only | Modrinth |
| [ShatterLib \| OctoLib](https://www.curseforge.com/projects/916747) |  | CurseForge |
| [Shulker Box Tooltip](https://modrinth.com/project/2M01OLQq) |  | Modrinth |
| [Simple Discord Link](https://modrinth.com/project/Sh0YauEf) | server only | Modrinth |
| [SimpleTMs: TMs and TRs for Cobblemon](https://modrinth.com/project/yFqR0DNc) |  | Modrinth |
| [Sinytra Connector](https://modrinth.com/project/u58R1TMW) |  | Modrinth |
| [Sodium](https://modrinth.com/project/AANobbMI) | client only | Modrinth |
| [Sodium Extra](https://modrinth.com/project/PtjYWJkn) | client only | Modrinth |
| [Sodium Shadowy Path Blocks (SSPB)](https://modrinth.com/project/EIa1eiMm) | client only | Modrinth |
| [Soft Imprints](https://modrinth.com/project/UhxJgB1o) | client only | Modrinth |
| [Sophisticated Backpacks](https://modrinth.com/project/TyCTlI4b) |  | Modrinth |
| [Sophisticated Backpacks Create Integration](https://modrinth.com/project/s85zLEDe) |  | Modrinth |
| [Sophisticated Core](https://modrinth.com/project/nmoqTijg) |  | Modrinth |
| [Sophisticated Inventory Interactions](https://modrinth.com/project/orgY0JIo) |  | Modrinth |
| [Sophisticated Item Actions](https://modrinth.com/project/RMW7bKVL) |  | Modrinth |
| [Sophisticated Storage](https://modrinth.com/project/hMlaZH8f) |  | Modrinth |
| [Sophisticated Storage Create Integration](https://modrinth.com/project/MJ0hdevs) |  | Modrinth |
| [Sophisticated Storage in Motion](https://modrinth.com/project/6vtFbyaJ) |  | Modrinth |
| [SuperMartijn642's Config Lib](https://modrinth.com/project/LN9BxssP) |  | Modrinth |
| [SuperMartijn642's Core Lib](https://modrinth.com/project/rOUBggPv) |  | Modrinth |
| [Supplementaries](https://modrinth.com/project/fFEIiSDQ) |  | Modrinth |
| [SwingThrough](https://modrinth.com/project/JyKlunuD) | client only | Modrinth |
| [Tectonic](https://modrinth.com/project/lWDHr9jE) |  | Modrinth |
| [Terralith](https://modrinth.com/project/8oi3bsk5) |  | Modrinth |
| [Tips](https://modrinth.com/project/AMCbgyVw) |  | Modrinth |
| [Tom's Simple Storage Mod](https://modrinth.com/project/XZNI4Cpy) |  | Modrinth |
| [UniLib](https://modrinth.com/project/nT86WUER) | client only | Modrinth |
| [Visuality: Reforged](https://modrinth.com/project/z13R7Et1) | client only | Modrinth |
| [Wakes Reforged](https://modrinth.com/project/E0SdeAoH) |  | Modrinth |
| [Waystones](https://modrinth.com/project/LOpKHB2A) |  | Modrinth |
| [When Dungeons Arise](https://modrinth.com/project/8DfbfASn) |  | Modrinth |
| [Wild Battle API](https://modrinth.com/project/v7VZE8kh) |  | Modrinth |
| [Xaero's Minimap](https://modrinth.com/project/1bokaNcj) |  | Modrinth |
| [Xaero's World Map](https://modrinth.com/project/NcUtCpym) |  | Modrinth |
| [YetAnotherConfigLib (YACL)](https://modrinth.com/project/1eAoo2KR) |  | Modrinth |
| [YUNG's API](https://modrinth.com/project/Ua7DFN59) |  | Modrinth |
| [YUNG's Better Dungeons](https://modrinth.com/project/o1C1Dkj5) |  | Modrinth |
| [YUNG's Better Mineshafts](https://modrinth.com/project/HjmxVlSr) |  | Modrinth |
| [YUNG's Better Nether Fortresses](https://modrinth.com/project/Z2mXHnxP) |  | Modrinth |
| [YUNG's Better Strongholds](https://modrinth.com/project/kidLKymU) |  | Modrinth |
| [Zume](https://modrinth.com/project/o6qsdrrQ) | client only | Modrinth |

### Resource packs (15)

| Name | Notes | From |
| --- | --- | --- |
| [CobbleFolk Skin Pack](https://modrinth.com/project/FTbFC6tW) | client only | Modrinth |
| [Cobblemon Advancement Plaques](https://www.curseforge.com/projects/862925) | client only | CurseForge |
| [Cobblemon Pasture Enhanced](https://modrinth.com/project/mBVaf2pS) | client only | Modrinth |
| [CobbleMotion](https://modrinth.com/project/lIDAJAby) | client only | Modrinth |
| [CobbleSounds BattleTunes](https://modrinth.com/project/yIgJQt6H) | client only | Modrinth |
| [CobbleSounds PokeCries](https://modrinth.com/project/yIgJQt6H) | client only | Modrinth |
| [CobbleSounds SFX](https://modrinth.com/project/yIgJQt6H) | client only | Modrinth |
| [CobbleSounds Soundtrack](https://modrinth.com/project/yIgJQt6H) | client only, optional | Modrinth |
| [E19 - Cobblemon Minimap Icons](https://modrinth.com/project/Va3BanZa) | client only | Modrinth |
| [Faithful 32x](https://modrinth.com/project/w0TnApzs) | client only | Modrinth |
| [Faithful 32x AppleSkin Addon](https://modrinth.com/project/cPFBIJcb) | client only | Modrinth |
| [Faithful Fusion Connected Default Glass 32x Add-on](https://modrinth.com/project/xIVQ9z6p) | client only | Modrinth |
| [Motschen's Better Leaves](https://modrinth.com/project/uvpymuxq) | client only | Modrinth |
| [Radical Cobblemon Trainer Textures Plus](https://modrinth.com/project/ARGDWSQq) | client only | Modrinth |
| [Tom's Cobblemoned](https://www.curseforge.com/projects/1214115) | client only | CurseForge |

### Shaders (1)

| Name | Notes | From |
| --- | --- | --- |
| [Complementary Shaders - Reimagined](https://modrinth.com/project/HVnmMxH1) | client only | Modrinth |

### Data packs (1)

| Name | Notes | From |
| --- | --- | --- |
| [CobbleMotion](https://modrinth.com/project/lIDAJAby) |  | Modrinth |

</details>
<!-- modlist:end -->

---

Maintaining the pack: [DEVELOPMENT.md](DEVELOPMENT.md). Design notes: [DESIGN.md](DESIGN.md).

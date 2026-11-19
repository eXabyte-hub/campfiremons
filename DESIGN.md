# Cobblemon Pack: Design Brief

Status: **draft v2** (2026-11-09).
- v1 came from the initial interview.
- v2 lowers the difficulty: catching has no level limit (the cap applies to gyms instead), loot is only lightly gated, and the chosen §5.2 mods move into §5.1.
Pack name: **Campfiremons**, namespace `campfiremons`.

Legend: **[decided]** came from the interview. **[proposed]** is a default I picked that you should change if you disagree.
Numbers marked *draft* get tuned in playtesting.

---

## 1. Goals

- **Cobblemon-first.** It plays like a Pokémon game, with tech and automation as support, not as the main course.
- **Curated.** Roughly 75 base mods plus ~30–40 additions, against ATMons' ~400. Every addition needs a reason to be here.
- **Gated progression that survives a group of rushers without turning into a grind.**
  - Legendaries, gym levels, battle mechanics, balls and a handful of broken items unlock by stage.
  - Normal catching, and most loot, stay open.
- **One-click updates** for friends and the server, with the pack kept in git.
- **Target length: 40–60 h** of group play [decided]. Expect the group to do it faster, so the gates need to hold.

Non-goals: kitchen-sink tech, magic mods, a skyblock or questing-only format, or copying ATMons code.
ATMons has no license, so we only study its approach (see §6).

## 2. Platform facts

| | |
|---|---|
| Minecraft / loader | 1.21.1 / NeoForge **21.1.264** (what the official pack 1.8.4 pins) |
| Base | **Cobblemon Official Modpack [NeoForge] 1.8.4** (Modrinth `cobblemon-neoforge`, 2026-10-27): Cobblemon **1.8.4**, about 75 mostly client and performance mods (Sodium, Iris, EMI+JEI, Xaero's maps, Sinytra Connector) |
| Cobblemon line | **1.8.x** [decided]. ATMons is on 1.7.3, so some ATMons-era addons need testing (§5) |
| Scripting | KubeJS **2101.7.2-build.381** + Rhino 2101.2.8 (Modrinth) |
| Quests | FTB Quests + FTB Library + FTB Teams (**CurseForge-only**, not on Modrinth) |
| Hosting | **Rented host** [decided], provider not chosen yet (requirements in §8) |
| Players | Small friend group, **mixed or unknown launchers** [decided] |
| Unlocks | **Per player** [decided] |
| Repo | **Public GitHub** [decided] |
| Trainers | Radical Cobblemon Trainers 0.19.2-beta, **Radical Red series** for everyone [decided] |

## 3. Progression model

### 3.1 Stages = quest chapters, each ending in a gym [decided]

- Every FTB Quests chapter is one **stage**. The chapter's capstone quest is that stage's **gym battle**.
- Earning the badge completes the stage. The **stage number = badges earned**, giving one progression number for everything.
- Stage flags are **advancements**: `campfiremons:stage/1` … `campfiremons:stage/9` [proposed].
  - *Advancement*: a per-player flag the game saves, visible in the advancements screen, and grantable by command.
  - FTB Quests grants them with a command reward (`/advancement grant @p only campfiremons:stage/3`).
  - Vanilla **loot tables can test advancements**, which is the main reason to prefer them over KubeJS "stages" (§4.4).
- Gyms are a **mix** [decided]. Proposed split:
  - Gyms 1–4 (Brock, Misty, Lt. Surge, Erika) live in a **hub town** at spawn, admin-built and placed with RCT commands.
  - Gyms 5–8 (Sabrina, Koga, Blaine, Clair) are **out in the world** (Radical Gyms & Structures).
  - The Elite Four and Champion Terry are back in the hub's **League** building.
  - The rival, Brendan/May and Team Rocket fights are RCT key trainers that spawn in the world; they raise the level cap but aren't stage gates.
- Side chapters (not stage gates): Breeding, Raids, Legends, Create/Engineering, Economy.
- **Spawn town** [decided, F10]: on a new world's first load, `spawn_town.js` moves the world spawn to the centre of
  the nearest Pallet Town (CobbleTowns; structure tag `campfiremons:spawn_town`), so everyone starts and respawns
  without a bed there. Runs once per world; a world over a minute old keeps its spawn, so existing worlds don't move.
- **Gym maps** [decided, F10]: on first login, after every stage-up and with `/gymmap` (30 s cooldown), a player gets
  directions to the gym of their next stage (`config.js` `nextGym`, `gym_maps.js`): an explorer map with a red X
  for overworld gyms (loot tables `campfiremons:gym_map/<id>`, structure tags `campfiremons:gym/<id>`) plus distance,
  direction and coordinates in chat. Cinnabar (Nether), Blackthorn and the League (End) get chat directions once
  you're in that dimension. Gyms sit on their own structure grids, so the search is quick. Idea from COBBLEVERSE.

### 3.2 Parity rule [decided]

**Before you face a trainer, you can get the same class of power they use.** If a trainer brings a Mega, Megas are unlocked for you by then; if they bring a legendary, so is that tier. Unlocking *earlier* than the first trainer that uses something is fine ("at least equivalent").

From RCT's Radical Red data, the first fight that uses each class:

| Power class | First used by | You face them with | So it unlocks at |
|---|---|---|---|
| Mega Evolution | Lt. Surge (Mega Manectric) | 2 badges | **Stage 2** |
| Perfect IVs (and trained EVs) | Brock, and every trainer after | 0 badges | Bottle Caps at **Stage 2** (as early as the gate allows) |
| Sub-legendary, Ultra Beast, box legend | Giovanni's 3rd team (Tapu Lele, Celesteela, Mega Mewtwo Y) | 7 badges | by **Stage 7** (ramped in from Stage 5, see below) |
| Mythical | Clair (Magearna) | 7 badges | **Stage 7** |
| Primal Reversion, Crowned Zacian | Elite Four (Lorelei, Bruno) | 8 badges | **Stage 8** |
| Z-Moves, Tera, Dynamax | never used by RR trainers | — | kept as **player-only bonuses** [decided] |

### 3.3 Stage table

| Stage | Reached by | Level cap while at this stage | Legend tier | Main unlocks |
|---|---|---|---|---|
| 0 | start | 15 | none | Poké Ball, apricorn basics, Create basics, Cobbleworkers basics, breeding, raids ★1 |
| 1 | Brock | 21 → 27 | none | Great Ball, evolution stones in loot, TRs, raids ★2 |
| 2 | Misty | 29 → 34 | none | **Megas**, **Bottle Caps**, shop tier 2, Cobblenav |
| 3 | Lt. Surge | 44 | none | **Ultra Ball** via a Create chain, Z-Moves (bonus), raids ★3 |
| 4 | Erika | 46 → 59 | none | Battle Tower, raids ★4 |
| 5 | Sabrina | 63 → 68 | **T1** sub-legends | TM crafting, specialty balls (Quick/Timer/Dusk…) |
| 6 | Koga | 73 → 76 | **T2** UB + Paradox | Beast Ball, Ultra Space (Ultra-Beasts wormholes), Tera (bonus), raids ★5 |
| 7 | Blaine | 79 → 81 | **T3** mythicals + **T4** box legends | Dynamax (bonus), raids ★6 |
| 8 | Clair | 81 → 85 | all | **Primal orbs, Rusted Sword/Shield**, Ability Capsule/Patch, raids ★7 |
| 9 | Elite Four + Champion Terry (hub) | 100 | all | One Master Ball per player (direct reward), endgame |

- The **level cap is RCT's**, not ours: the ace level of your next unbeaten key trainer in the series (minimum 15). It rises with every key fight, including rivals and Team Rocket, so the "→" ranges show how it climbs within a stage.
- The cap limits **EXP** and **which Pokémon you can bring to any RCT trainer battle** (§4.2). It does **not** limit catching (§4.1).
- Legendary tiers ramp in [decided]: T1 at Stage 5, T2 at 6, T3 and T4 at 7. Parity alone would only require all four at 7; the ramp gives time to catch and train them before Giovanni and Clair.

### 3.4 Legendary tiers: by power, not region [decided]

| Tier | Contents (examples) | Default source of membership |
|---|---|---|
| T1 Sub-legendary | Birds, beasts, regis, lake trio, Swords of Justice, Forces of Nature, Tapus, Kubfu… | label `legendary` **minus** label `restricted` (44 species) |
| T2 Ultra Beast + Paradox | Nihilego…Blacephalon, Great Tusk…Iron Leaves… | labels `ultra_beast`, `paradox` (31) |
| T3 Mythical | Mew, Celebi, Jirachi, Deoxys, … | label `mythical` (22, Arceus moved to T4) |
| T4 Box/restricted | Mewtwo, Lugia, Ho-Oh, the weather trio, the creation trio, Arceus, … Koraidon, Miraidon, Terapagos | Cobblemon's own label `restricted` (27) + Arceus override |

Tier lists live in one config file. Any species can be moved by hand (for example, putting Kubfu earlier).
Label names verified against the Cobblemon 1.8.4 species data. Tier stages, label rules and per-species overrides live in `kubejs/startup_scripts/campfiremons/config.js`.

**Sources once a tier is unlocked** [decided: all of them]:
- Legendary Monuments shrines and summoning
- Ultra Space for T2 (Cobblemon Ultra-Beasts: rare wormholes to a one-Ultra-Beast dimension; entry is Stage 6+, below that the mod's void-fall return sends you home)
- Rare wild spawns (Complete Cobblemon Collection adds rare/ultra-rare Paradox and Ultra Beast spawns)
- Big quest rewards

## 4. What gets gated, and how

The group said it rushes **strong Pokémon, ball/item spam and loot**. Tech is less of a problem, so tech gating is lighter.

The core idea (v2): **catch whatever you can, but the level cap decides what you can bring to a gym.** Exploring is generous; the gyms are where progression holds.

### 4.1 Catching & tier locks (first feature)

Implemented as our own KubeJS hooks into Cobblemon's events (§6).
- **No level limit on catching** [decided]. Any wild non-legendary Pokémon can be caught if you can weaken it and land the ball.
  - A Lv60 mon is still hard to beat with a Lv15 team, and good balls are gated (§4.3), so the challenge stays natural.
- **Tier locks** (unchanged): throwing at, or starting a battle with, a wild T1–T4 Pokémon whose tier you haven't unlocked is cancelled. You get a chat/actionbar message and an error sound.
- **Master Ball:** no special catching rule, and it can't get around tier locks.
- **Trading: trust the group** [decided]. You can trade a legendary to someone without the unlock, and they can use it outside gym battles. Only catching and wild battles check tiers.
- An **admin bypass**: the hidden `campfiremons:bypass` advancement. Creative mode is deliberately *not* a bypass, so locks can be tested in creative.
- Other capture flows: where a mod catches without a thrown ball, we gate access to the content instead (raid star tier, wormhole entry, summon item).
  - Raid Dens [checked, F7]: after a win, a reward screen catches the boss with the ball in your main hand. The ball only sets which ball it lives in (the catch rate comes from the star tier's config), so ball use-locks don't matter there. Its bosses are ordinary species: there are no legendary bosses in Raid Dens 0.13.5.

### 4.2 Level cap: trainers and EXP (handled by RCT)

Verified in the RCT 0.19.2-beta source: RCT already does both halves, so we configure it rather than write code.
- **Trainer battle gate:** every RCT trainer refuses to battle if your party's highest-level Pokémon is above your cap ("over level cap"). It refuses; there's no scaling down.
  - This applies to **all** RCT trainers, not only gyms. The v2 idea of leaving roaming trainers uncapped isn't possible without patching RCT, and isn't needed: the EXP cap means only caught over-cap mons can trip it, and you box those first.
- **EXP stops at the current cap** (`allowOverLeveling = false`, RCT's default), with an action-bar warning.
  - Rare Candy and EXP Candy go through the same Cobblemon EXP event, so they respect the cap too, and a candy that would add nothing isn't used up.
  - Caught over-cap mons keep their level. They just can't gain more and can't battle trainers until the cap catches up.
- **Config** (shipped as `defaultconfigs/rctmod-server.toml`, copied into each new world): `initialSeries = "radicalred"`, so everyone starts in the series without visiting a Trainer Association; initial cap 15 and over-leveling off are RCT's defaults.
- **Scaling instead of refusing: not now** [decided]. Over-cap Pokémon get boxed before a trainer fight.
  - Config and KubeJS can't do it: RCT refuses before a battle exists (its own start method re-checks the cap), and RCT API's level rule is flat (every player Pokémon set to one level, up *and* down) and comes from Cobblemon's shared battle formats, so it can't be set per trainer.
  - The only route is a small companion Java mod (mixins: skip RCT's cap refusal, scale only over-cap Pokémon down). Level-adjusted battles also run on copies of your Pokémon, which likely means no EXP/EVs from them; that needs checking first.
  - Revisit after F6, once we see how often boxing actually gets in the way.

### 4.3 Balls & items (recipe changes via KubeJS)

- **Stage finds** [decided, F3]: beating a gym doesn't hand you its power items; it makes them start turning up in **structure chests** for you, so you have to go exploring for them.
  - Per player: **Lootr** (+ Lootrmon for Cobblemon's gilded chests) gives every player their own loot from every chest, rolled with that player's stage.
  - Mechanism: NeoForge `neoforge:add_table` loot modifiers, gated by a player predicate on `campfiremons:stage/N` (and "not found yet"), limited to 193 exploration chest tables (vanilla structures, Cobblemon ruins and shipwreck coves, Mega Showdown sites, Legendary Monuments shrines, Cobbleloots loot balls, YUNG's dungeons/strongholds/fortresses, When Dungeons Arise treasure chests, Incendium and Terralith structures, Cobblemon Extra Structures, Poké Labs; no villages, Pokécenters/PokéStops or spawn chest). All generated by `tools/gen_finds.py` from one config.
  - **Find once** for one-of-a-kind items (~1 in 4 eligible chests): once it has been in your inventory, a hidden-trigger `campfiremons:found/<item>` advancement completes and it stops appearing for you. Consumables (Ability Capsule 8%, Patch 5%) keep appearing.
  - **Hints**: each stage's toast title names what it unlocks (e.g. "Stage 2 · Mega Bracelet") and its description says where to look; each find shows in the League tab as a child of its stage until you've found it.
  - Finds: S2 Mega Bracelet, S3 Z-Ring, S6 Tera Orb, S7 Dynamax Band, S8 Red/Blue Orb + Rusted Sword/Shield (+ Ability Capsule/Patch, repeatable). The **Master Ball** stays the Champion's direct reward (S9).
  - Why not gate crafting: in 1.21 the crafting grid doesn't know who is crafting (KubeJS's `modifyResult` sees only the grid), and most enabler recipes fill all 9 slots, leaving no room for a seal ingredient. So their recipes are removed.
  - Mega Stones, Z-Crystals and Tera Shards stay obtainable as Mega Showdown ships them: they do nothing for a player without the matching enabler.
  - Cosmetic looks (17 bracelets, 15 Z-Rings) swap from the base item and back at a stonecutter. The Omni Ring is crafted from all four enablers, so it's naturally Stage 7.
  - Stage seals (a per-player crafting ingredient) turned out unnecessary: repeatable items use use-locks instead (balls, caps; below).
- Balls:
  - **Use-locks** [decided, F3b]: balls are crafted (and later automated with Create) freely, but **throwing** one above your stage is refused with a message and the ball isn't used up (KubeJS `ItemEvents.rightClicked`/`entityInteracted`, list in `config.js` `itemLocks`).
  - Ladder = Cobblemon's own ball material tiers: T1 (Poké, Premier, Heal, Safari, apricorn colour balls) S0 → T2 (Great, Net, Dive, Nest, Level, Lure, Heavy, Moon, Friend, Fast, Sport, Park) S1 → T3 (Ultra, Quick, Dusk, Timer, Repeat, Luxury, Love) S3 → T4 (Dream, Beast) S6.
  - A Create production chain for balls is optional flavour later (when Create is added); the per-player gate doesn't depend on it.
  - **Master Ball is never craftable or lootable.** One per player comes from the Stage 9 reward; Cobblemon's own recipe is removed and it's use-locked to S9. Create add-ons that make one lose that recipe by id in `gimmick_items.js` (Create Industries' sequenced assembly; Cobblemon Integrations' Nether Star bottom, superheated sheet and final deploy). Check any new ball add-on for one.
  - For that chain we'd try *Create: Cobblemon Balls Overhaul* first; if it breaks on 1.8, our own Create recipes in KubeJS.
- **Only the truly broken items are held back** [decided], each at its parity point (§3.2):
  - Mega Bracelet: S2 find (Mega Stones stay free; useless without it)
  - Bottle Caps: use-locked to S2 (Only Bottle Caps; crafting stays free, Withered caps never locked)
  - **Other mods' loot is not stripped; locks hold however you got the item** [F6]: Cobbleloots, Raid Dens and Legendary Monuments can drop Ability Capsules/Patches, Red/Blue Orbs and Rusted items early. Master Ball and Ability Capsule/Patch are use-locked (S9/S8). One exception [F10, v0.1.13]: Cobbleloots' Master Loot Ball gave a Master Ball on a quarter of its rolls and players found them early, so `kubejs/data/cobbleloots/loot_table/loot_ball/master.json` is its table without that entry (the rest keep their weights). Master Balls still come from the Champion, the post-game Battle Tower shop, the Lavender Town tower top chest, two Extra Structures chests (great dungeon, suerebe); RCT trainers very rarely drop an Origin Ball (2 in 5,680 per loot roll), locked to S9 like the Master Ball. Orbs and Rusted items work just by being held, so a **held-item lock** refuses any battle while a party Pokémon holds one above your stage (`config.js` `heldItemLocks`, checked at battle start).
  - Primal orbs (Red/Blue Orb), Rusted Sword/Shield: S8 finds (no other survival source exists)
  - Ability Capsule/Patch: S8 finds, repeatable (recipes removed; Cobblemon's own loot copies are F4)
  - Master Ball: S9 reward only
- Everything else stays craftable and lootable as normal: Rare Candy, EXP Candy, evolution stones, and competitive held items (Choice items, Life Orb, Leftovers).
  - The EXP cap stops candies from over-leveling (verified, §4.2).
- Item IDs to gate in F3 (from the jars):
  - Mega: `mega_showdown:mega_bracelet` (+ colour variants), `mega_ring`, `may_bracelet`, `lysandre_ring`, `omni_ring`, `keystone`, and 93 Mega Stones (`*ite`, `*ite_x`/`_y`/`_z`).
    `omni_ring` likely enables every gimmick at once, so it gates at the *latest* gimmick stage.
  - Z-Moves: `z_ring` (+ variants, `*_z_power_ring`) and 35 Z-Crystals (`*ium_z`). Tera: `tera_orb`, 19 Tera Shards. Dynamax: `dynamax_band`.
  - Primal/Crowned: `mega_showdown:red_orb`, `blue_orb`, `rusted_sword`, `rusted_shield`. Abilities: `cobblemon:ability_capsule`, `ability_patch`.
  - Bottle Caps: **Only Bottle Caps 1.5.0** (`obc:bottle_cap`, `bottle_cap_<stat>`, `bottle_cap_gold`). Cobblemon Utility+ was dropped: its Master Candy/Cobblemax set Pokémon to Lv100, bypassing the level cap.

### 4.4 Loot (light touch) [decided]

- Exploring should feel rewarding, so most loot is left as the mods ship it.
- We only **strip the §4.3 held-back items** from world loot and re-add them at their stage.
  - Plain datapack JSON can check the looting player's advancements, e.g. "Bottle Caps only if `campfiremons:stage/2`". No extra mod is needed.
  - *Loot table*: the JSON that decides what a chest, mob or block drops. KubeJS can ship datapack files under `kubejs/data/`.
- Tables to check for those items:
  - vanilla structure chests
  - Cobbleloots loot balls
  - Extra Structures and Legendary Monuments chests
  - SimpleTMs' loot injections

### 4.5 Economy: CobbleDollars + gated shops [decided]

- Money comes from trainer battles, quests and selling.
- Shop stock unlocks per stage, using either per-player conditions in CobbleDollars' config (unverified) or one merchant per stage plus a KubeJS purchase check.
- Shops must never sell above-stage items, or they would undo §4.3.
  - As built (F6 batch 2): CobbleDollars' default shop is kept (balls, healing, EXP items) because use-locks already stop players *using* above-stage balls/caps, the same as crafting. Only the Master Ball and Hisuian Origin Ball are removed: `tools/gen_shop.py` writes `config/cobbledollars/default_shop.json` (CobbleDollars reads that file, not its datapack template).
  - The Battle Tower's BP shop keeps its Master Ball and Origin Ball [decided], raised to 200 BP each: a long-term goal, usable from S9 (use-locked).
  - Hisuian "ancient" balls are use-locked by their tier too (Great/Wing/Leaden S1, Ultra/Jet/Gigaton S3, Origin S9).
- **Poké Balls only from shops and Create** [decided 2026-11-16, v0.1.22]: `poke_ball_recipes.js` removes every crafting
  recipe whose result is in `#cobblemon:poke_balls` (Cobblemon's 47, and Legendary Monuments' Origin Ball). Every ball
  but the two guaranteed catches is in the CobbleDollars shop, and Cobblemon Create Industries and Create: Klinks 'n'
  Klangs make every ball by sequenced assembly or a spout (74 recipes; Industries makes the lids from apricorns). Mechanical
  Crafters, the vanilla Crafter and crafting upgrades use the removed recipes, so they can't make balls. The Light, Smoke
  and Iron Balls are held items outside the tag and keep their recipes.

### 4.6 Battle mechanics & side systems

| System | Gate |
|---|---|
| Megas / Z-Moves / Tera / Dynamax (Mega Showdown) | S2 / S3 / S6 / S7: the enabler (Mega Bracelet, Z-Ring, Tera Orb, Dynamax Band) becomes findable at that stage and can't be crafted. Megas are parity; the other three are player-only bonuses |
| Primal Reversion, Crowned forms | S8 finds (Red/Blue Orb, Rusted Sword/Shield) |
| Raid Dens | Star tiers by stage [decided, F7], matched to boss level vs. the level cap: ★1 from the start, ★2 S1, ★3 S3, ★4 S4, ★5 S6 (★6 S7, ★7 S8 have no bosses in 0.13.5). Right-clicking a den crystal above your stage is refused, which covers hosting and join requests (`config.js` `raidTierLocks`). Rewards need no extra gate: Ability Capsule/Patch (★4+/★5+) are use-locked and candies respect the EXP cap |
| TMs (SimpleTMs) | Use-locked by item tag: TRs (`#simpletms:tr_items`) S1, TMs (`#simpletms:tm_items`) S5 (`config.js` `itemTagLocks`) |
| Breeding (Cobbreeding) | Not gated [decided, F7]: open from the start. Create-driven incubation dropped (Cobbreeding hatches eggs in your inventory, and tech isn't gated) |
| Cobblenav | Use-locked to S2 (PokéNav, PokéFinder, FishingNav) |
| Battle Tower | S4, mid-game side activity [decided]: right-clicking the Holo Battle Tower is use-locked (`config.js` `blockLocks`). Its gated shop items stay use-locked (Master/Origin Ball S9, Ability Patch S8); Master and Origin Ball cost 200 BP (was 30) via `config/cobblemon_battle_tower/bp_shop_items.json` |

### 4.7 Tech: no gating [decided, F6 batch 3]

- Tech is open from the start; progression stays on the Pokémon side (the group doesn't rush tech).
- **Create 6** with Pokémon production: Cobblemon: Create Industries (balls, candy, mochi on Create lines),
  Klinks n Klangs (Cobblemon medicine/vitamins as fluids), Berry Harvester (harvesters pick Cobblemon berries).
  Plus Crafts & Additions (electricity), Create Deco and Copycats+ (building).
- **Refined Storage 2** and **Tom's Simple Storage** for storage, **Oritech** as the late automation tier. No
  Mekanism, no AE2.
- Ball use-locks still apply to Create-made balls. Create Industries' Master Ball recipe is removed (by id: it's a
  Create sequenced-assembly recipe KubeJS may not read the output of).

### 4.8 World, mobs and gear [decided, F6]

- **Structures share one grid** [decided, F10]: every mod places its structures on its own grid, so they piled up
  next to each other (6 within a few dozen blocks at one spot), and spreading each grid out (×1.5, then ×2) didn't
  stop it. The common overworld surface structures (vanilla temples, portals, outposts, ocean ruins and shipwrecks;
  Cobblemon ruins, habitats and boats; Terralith; Mega Showdown; most Extra Structures; When Dungeons Arise's minor
  set) are now one structure set, `campfiremons:surface_structures`: one structure per 20×20-chunk cell, neighbours at
  least 176 blocks apart, each weighted by its current rate (modded ×2, vanilla as shipped) and biomes. A weighted
  empty cell (`campfiremons:empty_cell`, places nothing) keeps sparse biomes as they were and caps dense ones (desert
  about 18 → 6 per km², deep ocean 25 → 7).
  Finding something on the shared grid means generating every cell it could be in, which is slow for rare
  structures, so whatever maps or mods look up keeps a grid of its own, kept 5 chunks clear of every shared-grid cell
  (spacing cut ×0.84 to make up for the lost spots): villages, mansions, monuments, shipwreck coves, explorer-map
  destinations from loot (When Dungeons Arise's major set, four Extra Structures), Legendary Monuments (its tracker)
  and the 7 Kanto gyms (×1.5: their buildings contain the leaders, and the hub for gyms 1–4 isn't built yet).
  Pokécenters, PokéStops and Poké Labs share a grid of their own (`campfiremons:services`, one per 42×42 chunks, kept
  clear the same way). Unchanged: underground structures and the other dimensions; Supplementaries ×2. Five gyms'
  biome lists are widened to Terralith's biomes through Cobblemon's tags (`kubejs/data/rgs/tags/worldgen/biome/`),
  which brings Vermilion and Celadon closer to spawn. Pewter (Brock, the first gym) goes further: any land biome and
  one cell per 32 chunks, so a new player nearly always has one nearby (one test world had the nearest 6.2 km out).
  All generated by `tools/gen_structure_spacing.py`.
  Measured on a test seed (1 km² around spawn): 18 → 12 surface structures, pairs under 32 blocks apart 18 → 0,
  median gap to the nearest 40 → 95 blocks. `/locate` stays instant for villages, services, gyms and monuments, but
  takes seconds for shared-grid structures (desert pyramid 0.6 s, swamp hut 7 s, a Dungeons Arise lighthouse 17 s).
- **No vanilla passive animals** except frogs (Froglights) and bees (pollination): farm animals, mounts and pets,
  water life and misc wildlife are gone. Pokémon cover their drops (feathers/chicken ~60 species, leather 15,
  porkchop, mutton, rabbit, wool + shearing, milking, ink, scutes, honey). Villagers and traders stay.
  Rotten flesh also cooks into leather (furnace, smoker, campfire; `leather.js`, asked for on 2026-11-16), since
  leather otherwise means beating Tauros, Miltank, Ponyta and the like.
  - Natural spawns: NeoForge biome modifier `remove_passive_mobs.json`. Everything else (structure pens, village
    cats, trader llamas, spawn eggs): KubeJS cancels them joining the world (`config.js` `removedMobs`).
- **Pokémon drop fixes** (`tools/gen_drops.py`): Cobblemon's `species_additions` *replace* drop tables, so Cobblemon
  Armory (90 species), Legendary Monuments (50) and Mega Showdown (2) were wiping normal drops. We override their
  files at the same ids with original + mod drops merged, and give the Pidgey, Spearow and Starly lines and
  Fletchling a 35% egg drop (otherwise only the Chansey and Exeggcute lines drop eggs).
- **Hostile mobs stay.** For the harder structures: Cobblemon Armory (Pokémon-themed weapons/armour),
  Artifacts (accessories found in dungeons) reworked by **Reliquified Artifacts** into Relics' levelling system
  (accessories grow stronger with use), and Mythic Upgrades (late-game gear tiers).
  - Relics needs **Curios**, so the pack runs two accessory systems: Accessories (Mega Bracelet/Z-Ring/badges)
    and Curios (relics). Same setup as All the Mons, which runs both. Curios and Artifacts come from Modrinth;
    Relics, Reliquified Artifacts and OctoLib from CurseForge (they allow third-party downloads).

## 5. Mod list

Additions on top of the official pack. "1.8?" shows whether the addon's latest NeoForge 1.21.1 build explicitly supports Cobblemon 1.8:
- ✅ explicitly supports 1.8
- 🟡 recent build that doesn't say
- ⚠️ last updated in the 1.7 era, so test it and drop or replace it if it breaks

### 5.1 Chosen

| Mod | Why | 1.8? |
|---|---|---|
| KubeJS + Rhino | All our gating logic | ✅ |
| FTB Quests / Library / Teams | Quest book, stage rewards. Since v0.1.10 four groups [decided, F10]: **Guide** (Getting Started hub, Evolution, Poké Balls by stage, Battle Gimmicks, Training, Raid Dens, Gotta Find 'Em All: Pokédex milestones, archaeology and fishing), **Legends** (Legendary, Ultra Beasts, Paradox: one optional catch quest per species, real Pokémon icons through Cobblemon's `pokemon_model` item), **Gym Challenge** (Stages 1–9 as hubs around each badge) and **Mods & Gear** (Tools & Weapons by tier and damage, Armor by points, Artifacts, Relics, Storage, Home & Building, Create, Oritech: optional item checklists). Built by `tools/quest_book/` (README there), art by `tools/gen_quest_art.py`; layout ideas came from screenshots of other packs, the art is our own | CurseForge-only, check packwiz download permission |
| Cobblemon Quests Reloaded 2.0.2 | FTB Quests tasks for catch/defeat/evolve (replaces the 1.7-only "Cobblemon Quests") | ✅ |
| Radical Cobblemon Trainers 0.19.2 + RCT API 0.16.2 | Trainers, gym leaders, League | 🟡 |
| Radical Gyms & Structures 0.7 | World gyms 5–8 | ✅ |
| Mega Showdown 1.3.3 | Megas, Z, Tera, Dynamax | ✅ |
| Navas ZA Megas 1.8.2 | Legends Z-A megas; adds Accessories, owo-lib and Architectury. Kept if it launches cleanly with Mega Showdown 1.3.3 | 🟡 |
| PokeBadges 2.0 | Physical badges: each stage advancement hands out its Radical Red gym badge (Badge Box at Stage 1) | 🟡 |
| Cobblemon Capture XP | EXP for catching | ✅ |
| Cobblemon Spawn Notification | Server-wide broadcast when a legendary, mythical, Ultra Beast or Paradox Pokémon spawns (or is fished up or drawn by a Poké Snack), and when someone catches, hatches or revives any of those or a shiny, ultra-rare or Alpha [decided, F10]. Shiny, ultra-rare and Alpha spawns aren't announced, and nothing is announced when it despawns or faints: out of the box it announced every ultra-rare and Alpha spawn (Cobblemon 1.8.4's own odds: 0.2% and 0.3% of wild spawns, plus each member of a group spawn) and each despawn, which flooded chat. Set in `config/spawn_notification.json` (`disabledSituations`). Spawn odds: see the wild spawn rarity row below | ✅ |
| Wild spawn rarity [decided, F10] | `config/cobblemon/spawning/best-spawner-config.json` cuts Cobblemon 1.8.4's wild odds for the rare buckets about fourfold: rare 0.5% → 0.15%, ultra-rare 0.2% → 0.05%, boss (Alpha herds) 0.3% → 0.1% of wild spawns (0.05% in v0.1.13, raised in v0.1.19 when they felt too scarce), so 1 in 330 instead of 1 in 100. With the defaults players met them every few minutes (a Ditto, starter evolutions: Cobblemon puts starter lines in the ultra-rare and boss buckets, Ditto in rare/ultra-rare outside mansions). Fishing, Poké Snack and habitat odds stay Cobblemon's. Cobblemon only reads that file with `exportSpawnConfig` on, so `cobblemon_settings.js` switches it on and reloads the spawner config when the server loads (before anyone joins: each player's spawner copies the odds at login). `replaceWithNewVersion: false` keeps it when Cobblemon ships new defaults: after a Cobblemon update, compare it with the jar's `data/cobblemon/spawning/best-spawner-config.json` | n/a |
| Cobblemon: SafePastures | Pastured mons can't die (Cobbleworkers) | ✅ |
| Catch Rate Display | Client-only catch-chance UI | ✅ |
| Cobblemon Battle Extras | Battle UI QoL | 🟡 |
| Cobblemon Armory 1.5.4, Mythic Upgrades 5.1.1 | Gear for hard structures (§4.8). Simply Swords was tried and dropped: didn't fit the theme | n/a |
| Artifacts 13.2.5 + Reliquified Artifacts 1.0.9 + Relics 0.12.11 (+ Curios, OctoLib) | Levelling accessories found in dungeons (§4.8) | n/a |
| Building: Framed Blocks, Handcrafted, Supplementaries + Amendments, Rechiseled (+ Rechiseled: Cobblemon, + Chipped compat, Fusion), Connected Glass, Building Gadgets 2 (CurseForge) | The group's ATMons building set, plus Cobblemon-block variants; alongside Chipped, CobbleFurnies and Legendary Monuments' block sets | n/a |
| Terralith 2.6.2 + Tectonic 3.0.28 | Overworld biomes and terrain; all 95 Terralith biomes are in Cobblemon spawn tags (`tools/check_biomes.py`). Less ocean [decided 2026-11-17, F10]: Tectonic's default `ocean_offset` (-0.8) made the live seed 63% ocean within 8,000 blocks of spawn (Terralith alone: 32%), with Terralith's Skylands (floating islands over deep ocean) between the islands. `config/tectonic.json` ships `ocean_offset` -0.6 (52% ocean on the same seed; everything else at Tectonic's defaults). It only changes chunks generated afterwards: coastlines don't line up where new land meets the pregenerated circle and explored areas, and gyms not generated yet can move (`/gymmap` locates them afresh). Measured by sampling the biome source on a scratch server with the live seed | n/a |
| Incendium 5.4.4, Nullscape 1.2.14 | Nether and End overhauls (End cities kept for Champion Terry) | n/a |
| MES - Moog's End Structures 2.1.1 + Moog's Structure Lib 3.4.2 (LGPL-3.0, server-only) [F10, asked for on 2026-11-19] | 25 vanilla-styled End structures (spires, watchtowers, citadels, meteorites, End forests, mega ships), each on its own spread grid from 1,000 blocks out. The live End had been pregenerated by Chunky to 3,000 blocks but no player had entered it (no `enter_the_end` advancement, dragon never fought), so it was reset with this release (its `DIM1` folder deleted with the server stopped) to generate with them everywhere. The Blackthorn Gym and Kanto League are End structures placed from the seed, so they regenerate where they were; both still locate with MES in (test server). Overlaps between MES and gym structures aren't prevented | n/a |
| YUNG's Better Dungeons / Mineshafts / Strongholds / Nether Fortresses, When Dungeons Arise | Structures; their chests join the finds | n/a |
| YUNG's Better Caves 3.1.6 (LGPL-3.0, server-only) [F10, asked for on 2026-11-18] | Bigger, more varied caves in new land: underground lakes and rivers, flooded caverns, lava regions, surface openings. It swaps the overworld's vanilla cave carvers for its own (biome modifiers on `#minecraft:is_overworld`, plus aquifer mixins) and leaves the noise router alone, so Tectonic's noise caves and terrain and Terralith's cave biomes are kept. Test (2026-11-18, live seed, 8x8 chunks at x 192-319, z 3840-3967): cave air underground 79k → 118k blocks (+49%), water 8.5k → 22k, exposed lava 3.3k → 59 in that area; surface heights differ no more than between two plain runs (trees and boulders vary run to run); generation 12 s → 15 s per 100 chunks. Only new chunks get it, so caves can stop at the edge of old land. Server-only in packwiz (Modrinth marks the client unsupported) | n/a |
| Lootr 1.11.38 + Lootrmon 0.0.0.3 | Per-player chest loot, so stage finds are fair in multiplayer (Lootrmon covers Cobblemon's gilded chests) | n/a / ⚠️ (Lootrmon predates 1.8) |
| Cobblemon Raid Dens 0.13.5 | Co-op raids, ★1–5 bosses (no legendaries) | 🟡 |
| SimpleTMs 2.3.3 | TMs/TRs | ⚠️ |
| Cobblemon Battle Tower 1.11 | Endgame | 🟡 |
| Legendary Monuments 8.2 | Shrines/summoning. Its 12 `battle_victory` callbacks (Archie, Maxie, Zinnia, Mustard, Calyrex, the dojo trainers, legendary battles) run for every NPC a player beats and call `q.player.set_npc_variable(t.loser.npc, …)`. RCT trainers are `npc_losers` too (actor type NPC) but not Cobblemon NPCs, so `t.loser.npc` is 0, the call throws, and Cobblemon's recovery (stopping a battle Showdown already closed) crashed the server: beating an RCT trainer, gym leaders included, took it down on 2026-11-16 [F10, v0.1.19]. `kubejs/data/cobblemon/callbacks/battle_victory/` blanks LM's 12 files (ARR, so nothing of theirs is copied) and `campfiremons_npc_battle_end.molang` does what they did (quest update, defeated or cooldown flag, each NPC's reward) once per win, only when `t.loser.npc.is_npc`. Recheck after updating LM: new callbacks there need the same treatment | ✅ (says 1.8.1) |
| Cobbleloots 2.5.0-alpha | Loot balls (we retune) | 🟡 |
| Cobblemon Extra Structures 1.3.0 | Exploration | ⚠️ |
| Cobblemon Ultra-Beasts 4.2 (CurseForge) | T2 source: Ultra Space wormholes; replaced Ultra Wormholes (1.7-era). Stage 6+ entry (`ultra_space.js`) | ✅ (1.8.4) |
| Cobbleworkers 2.0.7 | Pokémon-powered automation | ✅ |
| Create: Cobblemon Balls Overhaul 0.0.4 | Create ball recipes | ⚠️ (fallback: our own KubeJS recipes) |
| Cobblenav 2.4.2 | Pokénav / spawn finder | 🟡 |
| MoreCobblemonTweaks | QoL | 🟡 |
| Only Bottle Caps 1.5.0 | Bottle Caps (IV maxing), use-locked to Stage 2 | ✅ |
| Cobbreeding 2.4.1 | Breeding. `config/cobbreeding/main.json` is its defaults with `eggEncryptionEnabled: false` [decided 2026-11-16]: encryption hides an egg's nature, IVs and shininess from clients until it hatches, and the tooltip then shows a red "unable to read egg data" warning players took for a bug. Its `encryption/` keys stay server-side, not shipped. Eggs laid while it was on need one right-click to decrypt | ✅ (needs ≥ 1.8.2) |
| CobbleDollars 2.0.0-beta | Economy | ⚠️ (last build July 2026) |
| Create 6.0.10 | Tech backbone | n/a |
| Refined Storage 2.0.9 | Storage (not gated) | n/a |
| Tom's Simple Storage 2.4.2 + Create Contraption Terminals 1.4.0 + Tom's Cobblemoned (resource pack, on by default) | Simple early storage network (inventory connectors and terminals, wireless terminal), next to Refined Storage; terminals also work on Create contraptions; Cobblemon-style textures. Not gated | n/a |
| Oritech 1.2.13 | Late automation (not gated) | n/a |
| Create addons: Cobblemon: Create Industries 1.5.0 (+ Cobblemore Lib), Klinks n Klangs 2.0.1, Berry Harvester 1.0, Crafts & Additions 1.7.2, Create Deco 2.1.3, Copycats+ 3.0.11 | Pokémon production lines, power, building (§4.7) | ⚠️ (Create Industries/Klinks/Berry Harvester predate Cobblemon 1.8) |
| More Create addons [F10, asked for on 2026-11-18]: Create: Connected 1.3.3 (AGPL-3.0), Create Cobblestone 1.5.1 (CC0), Create: Enchantment Industry 2.5.4b + Create: Central Kitchen 2.6.2b (LGPL-3.0, both need Create: Dragons Plus 1.11.9), Create: Interiors 0.6.1 (GPL-3.0), Create: Cobblemon Integrations 0.3.9 (MIT) | Connected: clutches, gearboxes, kinetic battery, inventory bridge, fan catalysts (its copycats moved to Copycats+). Cobblestone: a cobblestone generator block run on stress units. Enchantment Industry: automatic enchanting and liquid XP. Central Kitchen: more Farmer's Delight automation beside Slice & Dice. Interiors: chairs, sofas and other furniture. Cobblemon Integrations: Slugma and Magcargo caught into Blaze Burners, Create lines for every Poké Ball (its Master Ball chain removed, §4.3), and Create mixing/filling for medicine, X-items, mochi, EV candies, vitamins and Exp. Candy XS (the same ingredients as Cobblemon's Campfire Pot, except vitamins, which become craftable). Picked from a survey of 170+ Create add-ons for NeoForge 1.21.1, all checked against Create 6.0.10; Sophisticated Storage Create Integration was already in. Test server (2026-11-18): starts clean, no crafting-table balls, no way to finish a Master Ball (only the harmless sheet→top press survives KubeJS's removal) | 🟡 (Cobblemon Integrations asks for Cobblemon 1.7.3+) |
| Create: Diesel Generators 1.21.1-1.3.15 (MIT) [F10, asked for on 2026-11-18, with Crafts & Additions, which was already in] | Pumpjacks, crude oil refining (diesel, gasoline), fermenters, compact engines, burners, plus chemical turrets/sprayers and lighters (fire spread is off on the server). Oil comes from `OilChunksSavedData`: each chunk's amount is worked out from the seed and its biomes on demand, so explored land has oil too. Its `oil_biomes` tag names only vanilla biomes, so `kubejs/data/createdieselgenerators/tags/worldgen/biome/oil_biomes.json` adds `#c:is_desert`, `#c:is_savanna`, `#c:is_badlands`, `#c:is_plains` (Terralith fills these): 38 biomes, 20 of them Terralith's. Both mods take fluids by shared tag: diesel (`c:diesel`) and biodiesel (`c:biodiesel`) already crossed over, but Oritech's crude is `c:oil` and Diesel Generators' is `c:crude_oil`, so `kubejs/data/c/tags/fluid/oil.json` and `crude_oil.json` add each to the other (asked for on 2026-11-18): either crude now feeds Oritech's Refinery and Fuel Generator and Diesel Generators' distillation. Gasoline stays Diesel Generators only. Crafts & Additions' Blaze Burner with a Straw superheats only on `c:biofuel` (Oritech's Biofuel, C&A's Bioethanol; every other liquid fuel just heats, 4-20 min a bucket), so `kubejs/data/c/tags/fluid/biofuel.json` adds Diesel Generators' Biodiesel (asked for on 2026-11-18); it also feeds Oritech's Refinery biofuel recipe (diesel + naphtha). Test server: starts clean, 119 recipes, both crudes in both tags, biodiesel in `c:biofuel`; one loot-table error for an optional Strut Your Stuff block, harmless | n/a |
| Create Utilities (Unofficial Port) 0.3.7 (MIT, SmartStreamLabs; original by duquee___) [F10, asked for on 2026-11-18] | Void Motor (rotation between linked motors at any distance), Void Chest and Void Tank (shared item/fluid storage at any distance), Gearcube. The original stopped at 1.20.1, so this is a community port; it declares Create [6.0.9, 6.1.0). Test server: starts clean, 21 recipes, all four blocks registered. Being a small port, recheck it on Create updates | 🟡 (unofficial port) |
| Complete Cobblemon Collection 1.8.4 (mod build) | Models, animations and spawns for the 34 species Cobblemon 1.8.4 has no model for (Paradox Pokémon, Celebi/Jirachi/Manaphy…, the Pawmi line, …), so trainer and raid Pokémon stop showing as stand-ins. Adds rare/ultra-rare wild Paradox and Ultra Beast spawns (tier-locked to Stage 6); no wild legendaries. All Rights Reserved, modpacks allowed without profit. It and Mega Showdown ship the same model files for ~74 legendaries/forms; Mega Showdown's must win (CCC's versions drop Calyrex riders, Ogerpon Tera, Deoxys colours and point at missing textures). Verified in game: NeoForge stacks Mega Showdown above CCC, so it wins all 70; recheck after updating either mod | ✅ (1.8.4) |
| Animation fixes [F10] | CCC replaces some animation files and Mega Showdown some pose files; mixed together, a pose can ask for an animation its group lacks and the client crashes when it plays (a friend's crash: Lucario's `sleep_quirk`). `tools/gen_animation_fixes.py` rebuilds the 50 affected groups in `kubejs/assets` (7 animations restored from lower-priority copies, 93 empty placeholders for ones nothing ships). Cobblemon keys posers and groups by file name and keeps the last in path order (checked in its source), so only the poser it uses counts. The fixes are checked with every resource pack on and with none, since players can leave packs off. CobbleMotion is All Rights Reserved, so nothing of it is copied: where one of its groups is broken, that Pokémon goes back to its previous group and poser instead It also writes posers a mod forgot: CCC 1.8.4 has Hisuian Growlithe with no poser (invisible, "No poser found"), so ours gives it a procedural head look and walk on CCC's bones (`MISSING_POSERS`). | n/a |
| CobbleMotion 1.6 (resource pack + data pack, All Rights Reserved, on Modrinth) [F10] | Idle, walking and some attack animations for about 200 Pokémon, for Cobblemon 1.8. It replaces 205 animation groups (176 of Cobblemon's own, 23 of CCC's, 6 of Mega Showdown's; 16 end up with fewer animations, e.g. CCC's Amoonguss 13 → 5) and some of its posers ask for animations its groups lack (the Lucario-style crash). The animation fixes can't patch its files (no permission to copy them), so 8 Pokémon go back to their previous animations: Decidueye, Emboar, Primarina, Sceptile and Galarian Weezing fully; Hisuian Decidueye, Kommo-o and Salazzle keep CobbleMotion's poser on Cobblemon's animations, because their old poser is built into Cobblemon's code. If its author allows copying, or fixes these upstream, re-run the tool to get them back. Its folders aren't Cobblemon's (`posers/amoonguss.json`, not `posers/0591_amoonguss/`), so its files sort last and win by file name. The same zip ships twice: as a resource pack (client) and in `datapacks/` (both sides) for its 46 species additions: mostly walk speeds that match the new walk cycles, plus Wigglytuff can fly, Togepi rides shoulders and small Absol/Espurr herd tweaks [decided] | n/a |
| CobbleFolk Skin Pack CF-1.1.0 (resource pack, MIT, from CobbleTowns: Continued) [F10] | Pokémon-world skins for every villager (176 random ones, Nurse Joy by name), zombie villagers, the witch, the wandering trader, Cobblemon's nurse and the CobbleDollars banker. Its OptiFine random-entity files run on Entity Texture Features, which the base pack has. Ranked above Faithful, which also skins villagers. Client-only | n/a |
| Client QoL [F10]: Mouse Tweaks, Jade, Controlling (+ Searchables), Zume | Inventory dragging, look-at info (Cobblemon shows species/level), keybind search, zoom. Zume instead of Zoomify (no NeoForge build). Sorting comes from Sophisticated Inventory Interactions (below); Inventory Profiles Next was removed [decided, F10] | n/a |
| Performance [F10]: ModernFix 5.27.27, ImmediatelyFast 1.6.15 | Load time, memory and rendering, which the base pack left out (picked up from Cobblemon Plus+; FerriteCore already came with the base). ModernFix runs on the server too; ImmediatelyFast is client-only | n/a |
| Advancement Plaques 1.6.8 (+ Iceberg) + Cobblemon Advancement Plaques 1.0.2 (resource pack, on by default) | Stage-ups and stage finds (both advancements with toasts) show as a Cobblemon-styled banner across the top of the screen instead of a corner toast. Client-only | n/a |
| GraveStone Mod 1.0.40 (henkelmax, All Rights Reserved, from Modrinth) [F10] | Your items go into a grave where you die instead of scattering; Jade shows whose grave it is. Breaking it (`break_pickup`) sorts items back into the vanilla slots only, so accessories landed in the main inventory. Since 2026-11-18 (asked for): Gravestone x Curios API Compat 4.2.1 (+ BaguetteLib 2.0.7; MIT, both server-only) puts Curios items back in their slots (Artifacts, Relics, the backpack's back slot, goggles), and the live world's game rule `accessories.keepAccessoryInventory` is true, since no grave mod restores the Accessories slots (Mega Showdown's Mega Bracelet, Z-Ring, Tera Orb, Dynamax Band; Legendary Monuments). Switching grave mods was ruled out: removing GraveStone would delete the graves still in the world | n/a |
| RightClickHarvest 4.6.1 (+ JamLib, + its Supplementaries compat; MIT) [F10] | Right-click a grown crop to harvest it and replant in one go (Supplementaries' flax too). 4.6.1, not the 3-day-old 4.7.0, when added | n/a |
| FTB Ultimine 2101.1.15 (FTB, from CurseForge, like FTB Library and Quests) [F10] | Hold the Ultimine key (default `) while mining or using a tool to break, till or harvest a whole vein or patch at once (asked for on 2026-11-16). Default limits (64 blocks); it shares FTB Library with the quest book | n/a |
| Cobblemon Ultimine Harvest 1.0.0 (Dawson/dwson, MIT) [F10, asked for on 2026-11-18] | Hold the Ultimine key and right-click a ripe berry or apricorn to pick the whole patch. Registers an FTB Ultimine right-click handler for Cobblemon blocks whose id ends in `_berry` or contains `apricorn` (API checked against Ultimine 2101.1.15). The requested FTB Ultimine Cobblemon Compat is Fabric-only. The author turned off CurseForge's third-party downloads, so the pack serves the unmodified jar itself (`mods/ultimine_cobblemon_harvest-1.0.0.jar`, sha1 6d18796c) with its MIT notice in `licenses/`; `tools/gen_modlist.py` lists it from its `HOSTED` table | n/a |
| FTB Essentials 2101.1.10 (FTB, All Rights Reserved, from CurseForge like the other FTB mods) [F10, asked for on 2026-11-18] | Player commands: `/home` (`/sethome`), `/tpa`, `/back`, `/spawn`, `/rtp`, `/warp` (admins set warps), plus `/enderchest`, `/crafting`, `/anvil`, `/smithing`, `/stonecutter`, `/trashcan`, `/hat`, `/nick`, `/near`, `/leaderboard`, `/rec`, `/kickme`; admin `/heal`, `/fly`, `/god`, `/invsee`, `/mute`, `/kit` and others need op. `config/ftbessentials.snbt` ships its defaults except: 3 homes (default 1) with a 60 s cooldown, a 3 s warm-up on `/home`, `/spawn`, `/tpa`, `/back`, `/rtp` (no escaping a fight), and `/rtp` at most 2,500 blocks from spawn (default 25,000), which keeps it inside the 3,000-block pregenerated circle so it never makes the server generate land. It is shipped exactly as the server rewrites it (no added comments), so a restart doesn't re-sync it. Free travel weighs against Waystones and the gym maps; the home limit and cooldowns are the brake. No dimension blacklists beyond its default (no `/rtp` in the End). `packwiz cf add` re-pointed `architectury-api.pw.toml` to CurseForge again; reverted to Modrinth | n/a |
| Almost Unified 1.4.2 (MIT) [F10] | Where several mods add the same material, recipes use and make one version and EMI hides the rest (asked for on 2026-11-16). Its default `mod_priorities` (minecraft, kubejs, create) covered none of our duplicates, so `config/almostunified/unification/materials.json` lists minecraft, kubejs, create, oritech, createaddition, createdeco, refinedstorage and adds `c:silicon` to its tags. Test server: electrum ingots all Oritech (was 5 Oritech, 3 Crafts & Additions), silicon Oritech (Refined Storage had one), zinc sheet Crafts & Additions (Create Deco had one), copper nugget Create. Recheck the counts after adding mods that bring metals | n/a |
| Polymorph 1.2.0 (LGPL-3.0) [F10] | When two mods' recipes share a crafting pattern, a button picks which result you get | n/a |
| Easy Magic v21.1.4 + Enchanting Infuser v21.1.4 + Easy Anvils v21.1.0 + Universal Enchants 21.1.9 + Universal Bone Meal v21.1.0 (Fuzss, MPL-2.0, + Puzzles Lib) [F10, asked for on 2026-11-19] | Universal Enchants: existing enchantments on more items (Infinity/Power on crossbows, Looting/Sharpness on tridents, protection on animal armour), Infinity + Mending and Multishot + Piercing allowed together, Infinity truly infinite, extra XP from Looting/Fortune; vanilla enchantments only. Test server: Infinity on a crossbow, Looting and Sharpness on a trident, Mending on a bow all apply. Universal Bone Meal: bone meal on plants vanilla ignores (sugar cane, cactus, vines, nether wart, coral and more), also from dispensers. Easy Anvils: items stay in the anvil (shown on the block), much smaller prior-work penalty, cheaper book applications, free renaming with formatting codes, iron blocks repair damaged anvils, anvils break less; its 2024 build loads clean with Puzzles Lib 21.1.66. NeoEnchant+ (57 data-driven enchantments, 26 in the table) was tried on the test server and loads, but was not wanted. Easy Magic: the enchanting table keeps its item and lapis after closing (shown floating round the block), a cheap re-roll button (a little lapis and a few XP points), and anything without a collision box (torches, grass) no longer blocks bookshelves. Tables placed before it need breaking and placing again. Enchanting Infuser: a second table to pick the exact enchantment for XP, no randomness (plus an advanced one). Both keep vanilla enchantments. Chosen over Apothic Enchanting, which Easy Magic says it is incompatible with (and which needs Apothic Attributes); Create: Enchantment Industry and Enchantment Descriptions are unaffected. Test server: starts clean, both infuser recipes load | n/a |
| Disconnect screen fix [F10] (KubeJS client script `disconnect_screen.js`) | Microsoft's sign-in service sometimes answers a join with an Azure error web page; Minecraft shows its source as the reason, the Back button ends up below the screen and the screen ignores Esc, so players had to restart the game (2026-11-15 to 17: seven times across three players; a retry a minute later works). On `ScreenEvent.Init.Post` for `DisconnectedScreen` the script swaps a web-page reason for a short explanation, cuts other over-long reasons to 400 characters and re-centres the widgets so the buttons stay on screen. No NeoForge mod does this. Tested 2026-11-17 on a player's client: kicked with a fake error page (`/kick` reasons stop at 256 characters), the screen showed the short message and a working Back button | n/a |
| Farmer's Delight 1.21.1-1.3.4 (MIT) + Create Slice & Dice 4.3.4 + Tomtaru's Cobblemon and Farmer's Delight Tweaks 2.0.4 (MPL-2.0) [F10] | Cooking beyond bread (asked for on 2026-11-17): cooking pot, skillet, cutting board, knives, cabbage/tomato/onion/rice, meals with Comfort and Nourishment. Its meat recipes take the drops Pokémon give (no vanilla farm animals). Slice & Dice: a Create Slicer runs every cutting-board recipe, every cooking-pot recipe is also heated mixing, and Sprinklers (water, liquid fertilizer). Tomtaru's: Cobblemon's Campfire Pot goes on a Farmer's Delight stove, berries and Hearty Grains plant on rich soil farmland, and FD crops feed the fossil Restoration Tank; 2.0.x dropped the old recipe changes (X-items in the cooking pot). Its mixins (`CampfirePotItem.useOn`, `CampfireBlockEntityRenderer.render`) were checked against Cobblemon 1.8.4. FD's wild crops only generate in new chunks and the server's world was pregenerated first, so `tools/gen_shop.py` adds a Seeds tab (cabbage seeds, tomato seeds, onion, rice, 500 each); chests in villages, shipwrecks, mineshafts and dungeons have them too (loot rolls when a chest is first opened). Test server (2026-11-17): starts clean; 105 cutting-board and 28 cooking-pot recipes, Slice & Dice injects 121 heated-mixing and 143 Slicer recipes (Cobblemon ships 32 cutting-board recipes of its own), and CobbleDollars loads the Seeds tab. Tomtaru's renderer mixin is client-side, so only a client shows it | 🟡 (Tomtaru's) |
| Simple Discord Link 3.4.5 (+ CraterLib; MIT, server-only) [F10] | Links the server with our Discord: chat both ways, joins and leaves, deaths, advancements, server start/stop. Server-only (CraterLib's network channels are optional, so players don't need it). Its config, with the encrypted bot token, is generated on the server and kept out of the pack so syncs never touch it; setup in DEVELOPMENT.md "Running the server" | n/a |
| Just Enough Cobblemon 1.4.0 (MIT per its page, both sides) [F10] | Pokémon drops in EMI/JEI with chances (R on an item, U on a Pokémon): Advanced Loot Info's Entity Drops can't show them, since Cobblemon keeps drops on species, not loot tables, and every Pokémon is one entity type. Also a Pokédex spawn tab that unlocks per species once encountered (the server copy sends the spawn data), which keeps the Stage 2 PokéNav lock meaningful; Cobblemon Info was the fuller alternative but shows every spawn from day one | n/a |
| Waystones 21.1.46, Ping Wheel 1.12.2 [F10] | Fast travel between waystones you've found (some generate in villages); pings to mark spots and Pokémon for the group. From COBBLEVERSE. No XP cost to warp and global by default [decided 2026-11-18]: `config/waystones-common.toml` is the live server's generated file with `enableCosts = false` (cooldowns and warp stone durability unchanged) and `defaultVisibility = "GLOBAL"`, so waystones placed or generated from then on are on everyone's list without visiting them; ones already activated keep their visibility unless someone changes it in the waystone's settings. With GLOBAL, Waystones lets everyone manage global waystones, but `restrictedWaystones = ["PLAYER"]` still keeps player-placed ones editable only by their owner. The file matches what the server writes, so restarts don't re-sync it | n/a |
| Magnum Torch v21.1.1 (Fuzss, MPL-2.0, + Puzzles Lib) [F10, asked for on 2026-11-19] | Torches that stop natural mob spawns in a big area: Diamond for monsters (8 chunks across), Emerald for passive mobs and wandering traders (16 across), Amethyst for water and cave mobs. Cobblemon's spawner spawns every Pokémon (water ones too) as a `CREATURE` with spawn reason NATURAL, so the Emerald torch would have stopped all wild Pokémon around it. Wanted for hostile mobs only, so `config/magnumtorch-server.toml` (its defaults otherwise) puts `cobblemon:pokemon` on all three torches' `mob_whitelist`. Test server: the entity id exists and the config is kept as shipped | n/a |
| Catch Indicator 3.1.1 (+ OS Cobblemon Library) [F10] | Wild Pokémon show whether you've caught their species. Client-only. From COBBLEVERSE | ✅ |
| Cobblemon Pasture Loot 2.0.0 [F10] | Pastured Pokémon produce species-fitting items; with no vanilla farm animals, pastures are the farms. From COBBLEVERSE | ✅ |
| Neruina 3.3.5 (+ Configurable), Packet Fixer 3.3.1 [F10] | Server safety: a crashing entity is removed instead of making the world unloadable; no "packet too big" kicks from full PCs and backpacks. From COBBLEVERSE | n/a |
| Chunky 1.4.23 (GPL-3.0) [F10] | Chunk pregeneration for the server: generate the land around spawn ahead of time, so exploring it doesn't lag the server while our worldgen (Terralith, Tectonic, the structure mods) catches up. Server-only in packwiz; run from the console (DEVELOPMENT.md, Running the server). Chosen over Chunk Pregenerator, which has no NeoForge 1.21.1 build on Modrinth. Not tried on the scratch server: first tested on the live one [decided] | n/a |
| PC boxes [F10] | 60 per new PC (Cobblemon 1.8.4 gives 40), set on server load by `cobblemon_settings.js` from `config.js` `pcBoxes` instead of shipping Cobblemon's whole `main.json` | n/a |
| CobbleTowns: Continued CT-1.1.3 (data pack, MIT; community port of CobbleTowns to 1.21.1 / Cobblemon 1.6.1) [F10] | Seven Pokémon towns as village variants (Pallet, Lavender, Cherrygrove, Pacifidlog, Twinleaf, Floaroma, Lentimas), each in its own biomes, with Pokécenters, Pokémarts and marker-spawned Pokémon (fixed levels, Lavender's tower Gastly 18–21 and a Marowak 30). The towns join the shared structure grid; its scattered Pokécenters and Pokémarts are switched off (`DROPPED` in `gen_structure_spacing.py`), since `campfiremons:services` already places ours. Shipped inside `kubejs/data/` (MIT notice in `kubejs/data/cobbletowns/license.txt`, pristine zip in `tools/vendor/`): as an Open Loader pack it outranked our overrides, so in v0.1.4 its scattered Pokécenters and Pokémarts stayed on and its towns also kept their own grids. Two fixes in `kubejs/data`: Lentimas' small-chest loot table (uses `minecraft:grass`, renamed `short_grass` in 1.20.3) and a `minecraft:village/jungle/villagers` pool (plains villagers) for the villager on Pacifidlog's ship. The original CobbleTowns is 1.20.1-only | n/a |
| Cobblemon Cities & Structures 1.0.17 (pinned; MIT, data-only mod; author calls it in development) [F10] | The Kanto cities and the Indigo Plateau as one structure set (on its own grid, ×1.5, its guide maps point at them): landmark buildings, CobbleDollars shops (balls and TMs, use-locked as usual), townsfolk and level-scaled trainers. Cities only [decided]: CCS's own leader battles are off, its gyms hook into RCT instead. `ccs_leaders.js` swaps each of the 8 CCS gym leader NPCs (picked out by `ForcedResourceIdentifier` `ccs:leaders/<name>`) for that leader's RCT trainer (`config.js` `ccsLeaders`) when the NPC loads, in a new city or one saved before: persistent, tagged `campfiremons_ccs_leader`, on the NPC's exact spot and facing, held there with Slowness as Radical Gyms' own command blocks do. So each city gym has one leader, and talking to them starts the RCT challenge under RCT's own rules (required defeats, level cap): a CCS gym is just another place to fight the same leader as in Radical Gyms [decided, F10]. It only runs when a `cobblemon:npc` joins the world, never on a tick. Entities load out to view-distance (10 on the server) but only run within simulation-distance (8), and a chunk that isn't running hides its entities from searches, so the swap waits for the NPC's chunk to run, for as long as it stays loaded (until v0.1.19 it gave up after 15 s, which left CCS's own leader in gyms players only walked past, often next to an RCT one from an earlier try: the duplicate and missing leaders players reported on 2026-11-16). The NPC is frozen (NoAI) while it waits, the leader is summoned already tagged (`summon_persistent ... {Tags:[...]}`) and teleported through a one-off tag, and each gym keeps one tagged leader: a swap keeps the one nearest the NPC, and a placed leader loading checks its gym (32 blocks) too, keeping one with the Slowness hold and removing other tagged or untagged copies (`discard()` also clears RCT's persistent record). RCT's despawn checks skip persistent trainers. If it can't place one after 15 s, the CCS NPC stays, and its dialogue (`kubejs/data/ccs/dialogues/generated/`) still offers "Challenge <leader>", which summons the RCT leader beside it. The Elite Four and Champion only talk (their Radical Red variants aren't mapped yet). CCS's Kanto advancement goals for the leaders and Champion complete on the matching RCT win, quietly (our stage banner is the announcement); its badge-item rewards are emptied (`ccs:badges/*`) because they give Cobbleverse Badges items, a mod we don't ship. Its own "essential NPCs" mode would keep leaders in place with an every-tick NBT scan of all entities. Overrides carry its MIT notice (`kubejs/data/ccs/license.txt`). Oak's Welcome (teleport to its Pallet or Pewter after the starter) is off (`ccs:open_welcome` emptied); Daisy still gives its starter kit. Its roadside Pokécenter is dropped (`DROPPED_STRUCTURES`). Rival Gary and Giovanni story fights are left as optional | n/a |
| CobbleSounds 1.4 Redux (resource packs, MPL-2.0) [F10]: PokeCries, SFX and BattleTunes on by default; Soundtrack an optional download, ticked by default | BattleTunes adds 102 Pokémon battle tracks to Cobblemon's wild, NPC (RCT trainers too) and PvP battle music; PokeCries swaps in the games' cries; SFX gives toasts (Advancement Plaques included) and level-ups Pokémon jingles. The Soundtrack replaces every vanilla music event (biomes, title screen, Nether, End). Every track is streamed, so none of it sits in RAM. It is 418 MB, so it's a packwiz optional file [decided]: the installer asks once, and a friend on a slow line can untick it and keep Minecraft's music. Skipped [decided]: its [Data] pack (full copies of 130+ Terralith and vanilla biome files, of which only 12 change music; 14 others carry older spawn lists or features, and as an Open Loader pack they would outrank Terralith 2.6.2, which already maps most biomes to vanilla music events), MC Soundtrack Replacement (only swaps the 19 vanilla tracks the Soundtrack still mixes in) and [Complete] (the all-in-one alternative to Redux). Client-only | n/a |
| Distant Horizons 3.3.3 (LGPL-3.0) [F10] | Draws terrain past the render distance as simplified LODs; works with Sodium, Iris and Complementary. Client-only [decided]: on the server it would generate distant chunks for everyone, which a rented host can't spare, so in multiplayer it shows terrain you've already been near (cached per server in the instance's `Distant_Horizons_server_data/`) and in singleplayer it generates ahead too. Its own defaults (Medium quality); players turn it down or off from its button in Video Settings | n/a |
| RCT Trainer Textures Plus 2.2 (resource pack, on by default) | Skins for all 1,559 RCT trainers, replacing RCT's plain defaults | n/a |
| E19 Cobblemon Minimap Icons 1.5.7 (resource pack, on by default) | Pokémon icons on Xaero's minimap radar, incl. Mega Showdown and CCC forms. Its model definitions only swap textures (alpha variants), never models. Needs radar icons on: the shipped `xaerominimap_entities.json` sets them to Always | n/a |
| Faithful 32x (1.21.1 June 2026) + Faithful Fusion Connected Default Glass 32x + Faithful 32x AppleSkin add-on (resource packs, on by default) [F10] | 32x remaster of the vanilla textures (replaced Stay True). Its OptiFine folder doesn't load on NeoForge; the glass add-on connects vanilla glass through Fusion; the AppleSkin add-on matches AppleSkin's food overlay to Faithful's hunger bar (it declares 1.21.3's pack format, so the default options also list it as allowed-incompatible). Better Leaves stays above them: its leaf textures are 32x too. No current Faithful packs exist for Create, Cobblemon or our other big mods (the community Faithful32 Modded stopped in 2022), so modded blocks keep their own textures. Bushy Leaves for Faithful left out: it would fight Better Leaves' models | n/a |
| Cobblemon Pasture Enhanced v4 (resource pack, on by default) | Pasture block shows its egg state at a glance | n/a |
| Cobblemon: Simple Pokécenters 1.2.1, Poké Stops 1.0.0, Poké Labs 1.1.2 | World structures with a healing machine, PC and loot chests (balls up to Ultra/Quick/Dusk, Rare Candy, vitamins: covered by use-locks and the EXP cap). Labs are rare (5 chests) and a stage-find source; Pokécenter/Stop chests aren't. Kept CobbleDollars: none of these sells anything [decided, F10] | ⚠️ (predate Cobblemon 1.8; server boots clean) |
| Sophisticated Backpacks 3.26 + Cobblemon: Trainers Backpack 1.0.2 | Backpacks with PC, party-heal (2.5 min cooldown, tiers down to 15 s) and cooking-pot upgrades, all allowed from the start [decided, F10] | ⚠️ (Trainers Backpack predates 1.8) |
| Sophisticated family [F10]: Storage 1.6, Inventory Interactions 0.1, Item Actions 0.5, Storage in Motion 0.10, Backpacks and Storage Create Integration (Core 1.5.35) | Tiered chests, barrels and shulker boxes with upgrades and storage controllers; search, sort (Name/Mod/Count/Tags) and transfer buttons on vanilla and modded inventory screens, plus the Sophisticated sort key (replaces Inventory Profiles Next); keys to highlight nearby storage holding an item, deposit into it and restock from it; storage on minecarts, boats and Create contraptions, backpacks on contraptions. Not gated. Official P3pp3rF1y add-ons only (no third-party sorters, upgrade tiers or the second Create compat) | n/a |
| ~~Cherished Worlds~~ (official pack) | Removed [F10]: it looks up its platform service on a worker thread during client setup, which failed on a fresh instance's first launch and crashed the game. It only pins favourite worlds in the singleplayer list | n/a |

### 5.2 Remaining candidates (not in unless you say so)

| Mod | My take |
|---|---|
| Structurify 2.0 | **Skip** [decided, F10]. Its spacing settings duplicate `gen_structure_spacing.py`, and its overlap prevention claims chunks as structures generate, so whether a structure appears depends on what generated first: `/gymmap`, the spawn town and explorer maps could point at one that never gets built. Its flatness check is the one thing we lack; revisit if cities or towns sit badly on slopes |
| Cobblemon Fight or Flight Reborn | Wild mons flee or attack. Skip for now, since it adds difficulty. 🟡 |
| Myths and Legends sidemod | Legendary key items/spawns, but overlaps Legendary Monuments. ⚠️ |
| Cobblemon Size Variations, Catch Indicator, CobbleStats, Cobbledex | Optional cosmetic/QoL |
| Cobblemon Smartphone | Heal/PC anywhere. If added, gate it, since it weakens exploration. |
| PKGBadges | Alternative badge mod (badges + trainer clothing sets) if PokeBadges disappoints |
| Cobblemon Create Industries | Alternative to the Balls Overhaul (Create production of balls/candy). ⚠️ |
| Lucky blocks, Gacha, GTS, Wonder Trade, Shiny Cookie | **Skip.** They bypass loot/item gating |
| Cobbled Levels, Limited Legends, RCT Capture Cap | **Skip.** They overlap our own gating (RCT Capture Cap is the closest off-the-shelf alternative) |
| Complete Cobblemon Collection, big fakemon packs | **Skip for now.** Huge asset/perf cost |

## 6. Catch-restriction implementation approach

This is studied from ATMons' `catch_restrictions.js`. The design is ours; no ATMons code is copied.

- **Startup script** (`kubejs/startup_scripts/`): subscribe to Cobblemon's own Kotlin event bus once at startup.
  - The events are `THROWN_POKEBALL_HIT` and `BATTLE_STARTED_PRE`, at a late priority so other mods see them first.
  - *Startup scripts* run once when the game boots, on both client and server. *Server scripts* run on the server and reload with `/reload`.
- The hook only forwards each event to a handler on `global.campfiremons`, looked up per event. The handlers and config live in other startup scripts, because KubeJS 2101 makes `global` read-only in server/client scripts. `/kubejs reload startup` swaps in new logic without a restart.
  - Ball hit: tier lock only. There is no level check on catching any more.
  - Battle start: tier lock for wild battles. For gym/League trainers it also runs the over-cap party check, unless RCT already handles that (§4.2).
- Config: `kubejs/startup_scripts/campfiremons/config.js` (caps, tiers, which RCT trainers count as gym/League).
- Data: `kubejs/data/campfiremons/advancement/stage/*.json` (hidden-trigger advancements granted by command).
- **Verify before writing code** (rule 5):
  - exact event class and field names in the Cobblemon 1.8.4 jar
  - how Rhino calls `subscribe(Priority, …)` on a Kotlin observable
  - species label names
  - what cancelling a ball hit does to the ball
  - whether in-battle throws fire the same event

## 7. Repo & update distribution

### 7.1 Repo = a packwiz pack [proposed]

*packwiz* stores each mod as a small `.pw.toml` file (download URL + hash), not the jar. It can export to Modrinth and CurseForge formats.

```
<pack>/                 git root, public GitHub
  DESIGN.md README.md DEVELOPMENT.md CHANGELOG.md
  pack.toml index.toml  packwiz metadata
  mods/*.pw.toml        one file per mod (Modrinth or CurseForge source)
  config/               incl. config/ftbquests/quests/
  defaultconfigs/
  kubejs/{startup_scripts,server_scripts,client_scripts,data,assets}
  tools/                dev-instance setup, base-pack diff script
  .github/workflows/    release build
```

- The base is imported from the official 1.8.4 `.mrpack`, and our additions go on top.
- When the official pack bumps, a `tools/` script diffs it against ours.

### 7.2 Who gets updates how

| Who | Path | Effort per update |
|---|---|---|
| Friends on **Prism** (recommended for everyone) | One-time import of a prepared instance whose **pre-launch hook** runs `packwiz-installer-bootstrap` against the repo's `release` branch | **Zero.** Press Play and it syncs |
| Friends on **Modrinth App** | Not supported [decided, F10]: 9 mods are CurseForge-only, so a `.mrpack` would have to bundle (rehost) their jars. Switch to Prism | n/a |
| Friends on **CurseForge app** | CF zip export is possible, but Modrinth-only mods complicate it | Not supported by default. Ask them to switch to Prism |
| **Rented server** | Server starter zip from the GitHub Release: the host starts `campfiremons-server.jar` (or `start.sh`, which runs it), which installs NeoForge once, runs the same bootstrap with `-s server` on every start, then starts NeoForge in the same JVM (NeoForged's ServerStarterJar). Works on any host that lets you pick the server jar | One restart |

### 7.3 Branches & release flow

- `main` holds work in progress; your dev instance tracks it.
- `release` is what friends and the server pull.
- To ship: merge to `release` and tag `vX.Y.Z`. CI (`tools/release/build.py`) builds the Prism instance zip and the server starter zip into a GitHub Release; neither holds mod jars. The version's `CHANGELOG.md` section becomes the release notes.
- A check workflow fails on any push where `index.toml` is out of date, since players would hit hash mismatches.
- Friends never see half-finished work.

### 7.4 Dev loop (your machine)

- A separate Prism instance runs the pack from the repo.
- `kubejs/` and `config/` are linked into the instance so edits land straight in git, and the FTB Quests editor saves into the repo.
- I read `logs/kubejs/startup.log`, `logs/kubejs/server.log` and `logs/latest.log` in the instance after each launch (KubeJS 2101 writes its logs there, not under `kubejs/logs/`).
- The details (symlink vs `packwiz serve`, keeping hashes in sync with `packwiz refresh`) get settled in setup.

## 8. Multiplayer / server

- The host needs:
  - NeoForge 21.1.264
  - **10–12 GB RAM** (about 160 mods incl. Create, Oritech, Terralith/Tectonic worldgen)
  - SFTP access
  - a **custom server jar** (or startup command) for auto-updates: the launcher jar runs the sync itself, so hosts
    that only let you pick the jar work too [decided, F10]
  - an Australian location (Sydney) for the group's ping
  - automatic backups
- Everyone keeps **solo FTB Teams**. Joining a party shares quest progress, which would break "per-player unlocks".
- The pack maintainer is op, with a whitelist. The starter's `server.properties` turns the whitelist and `allow-flight` on (Pokémon riding and Create contraptions get kicked for flying otherwise) and spawn protection off.
- Client-only mods (Sodium, Iris, shaders, etc.) are marked client-side in packwiz so the server never downloads them.
- Chunky (server-only) pregenerates around spawn once the world exists (DEVELOPMENT.md, Running the server).
- Host [decided, F10]: PebbleHost 25 GB Premium, Sydney node (AU128), bought 2026-11-15. Its NeoForge preinstall
  launches NeoForge 21.1.266 itself through its own `forge_modpack.jar` and ignores the jar setting, so the launcher
  runs there as a Java agent (`-javaagent:campfiremons-server.jar` in the startup flags) that syncs the pack first.
  PebbleHost accepts the EULA itself.
- The base pack includes **Sinytra Connector** (it runs Fabric mods on NeoForge). We keep it because the official pack depends on it, but prefer native NeoForge builds for everything we add.

## 9. Roadmap (small, testable steps)

| # | Feature | Done when |
|---|---|---|
| F0 | Repo + packwiz + dev instance (official 1.8.4 + KubeJS + FTB Quests) | Instance launches; logs readable; repo committed |
| **F1** | **Stage advancements + legendary tier locks** (catching and wild battles, admin bypass) | Legends catchable or blocked per stage, verified in game with `/advancement grant` |
| F2 | Level cap via RCT: Radical Red series for everyone, tier stages per the parity rule | New world starts in Radical Red with cap 15; over-cap party refused by trainers; EXP stops at the cap |
| F3 | F3a: gimmick enablers + held-back items as per-player stage finds with Lootr (done). F3b: Only Bottle Caps + ball/cap use-locks, Master Ball recipe removed (done). Create ball chain deferred to when Create is added | Locked balls/caps refuse to be used below their stage; enablers have no crafting recipe |
| F4 | Stage-aware loot tables | Early chests give no top-tier items |
| F5 | Gym wins grant stages via RCT's `rctmod:defeat_count` trigger (done). Quest book skeleton: one FTB Quests chapter per stage, generated once by `tools/gen_quests.py`, then edited in game (Cobblemon Quests Reloaded for Pokémon tasks) | Beating Brock grants Stage 1; quests auto-complete from stage/found advancements |
| F6 | Remaining addons, compatibility-tested in batches. Mega Showdown + ZA Megas first; batch 1 (Cobblemon content + QoL, 15 mods) done; worldgen (Terralith, Tectonic, Incendium, Nullscape, YUNG's, Dungeons Arise) done; batch 2 (SimpleTMs, Extra Structures, Ultra Wormholes, CobbleDollars) added; next, batch 3 (tech) | Clean launch with every chosen mod; `tools/check_deps.py` reports 0 missing |
| F7 | Mechanic/raid/TM/breeding gating. TMs done in F6; raid star tiers by stage; breeding left open | Per the §4.6 table |
| F8 | Economy shops gated | No above-stage purchases |
| F9 | ~~Tech gating~~ Dropped: tech is open from the start (§4.7) | |
| F10 | Release pipeline + server + friend onboarding. Prism instance zip + server starter built by CI per tag (no `.mrpack`, §7.2) | A friend updates by pressing Play |

## 10. Open questions (not blocking F0/F1)

1. ~~Pack name~~ Decided: Campfiremons (`campfiremons`).
2. Which rented host (see the requirements in §8).
3. Final cap numbers and the T4 list, after we see RCT's trainer levels.
4. ~~Should Master Ball be the S9 reward only, or also a rare raid ★7 drop?~~ S9 reward only (plus the Battle Tower shop at 200 BP); Raid Dens has no ★7 bosses and its rewards hold no Master Balls.
8. ~~Gym cap: scale or refuse?~~ Decided by RCT: it refuses (§4.2).
9. After F6: is boxing over-cap Pokémon annoying enough to justify a companion mod for scaling (§4.2)?
5. Who builds the hub town (you, or a schematic)?
6. Does anyone actually need the CurseForge app?
7. Do we keep FTB Chunks/Essentials/Ultimine? They're useful on a server, but not chosen yet.
10. Distant Horizons on the server too (it would generate distant LODs for everyone), once we know how much CPU the host has spare?

## 11. Risks to verify early

- **FTB Quests via packwiz:** it's CurseForge-only. If its authors disallow third-party downloads, packwiz-installer would make friends download it by hand. Check in F0.
- **1.7-era addons on Cobblemon 1.8.4** (the ⚠️ rows): test in batches in F6, starting with the ones F1 depends on (none).
- ~~Cobblemon event API in 1.8.4~~ Verified in F1 against the 1.8.4 jar and source (event classes, the subscribe overload, labels, cancel behaviour).
- **Capture flows** in Legendary Monuments may bypass ball-hit events (§4.1). Raid Dens checked in F7: no legendary bosses, and the gate is the star tier.
- ~~How a gym defeat reaches FTB Quests~~ Solved in F5: our stage advancements use RCT's own `rctmod:defeat_count` trigger, and quests watch the stage advancements.
- ~~Telling gym/League trainers apart in code~~ Not needed: RCT caps every trainer battle (§4.2).
- ~~RR trainers carry Mega Stones and Primal orbs~~ Verified with Mega Showdown 1.3.3: RR trainer data names `mega_showdown:` items with a plain-item fallback (Manectite, else Expert Belt), RCT's AI picks Mega/Tera/Z/Dynamax whenever Showdown offers it, and trainers need no Mega Bracelet. A test trainer's Manectric Mega Evolved and its Kyogre went Primal (`tools/testpacks/`).

## 12. Known upstream noise (harmless)

- Cobblemon client: `run_posable_molang` can't play `explosion`/`faint` on some battle participants (animation skipped).
- Legendary Monuments: 4 dojo *spawner* loot tables fail to parse (unused by us).
- EMI: Chipped's Workbench JEI category can't be shown through EMI's JEI bridge (277 log lines; Chipped workbench recipes just don't appear in EMI).
- Structures placing item frames/paintings/sculk sensors slightly out of place ("Block-attached entity at invalid position", "Failed to parse vibration listener").
- Dungeons Arise: 2 advancements (find_thornborn_towers, find_fishing_hut) fail to load.
- GeckoLib: Relics' animated tooltip frames aren't a multiple of the frame size.
- Connector: "Couldn't load fabric:overlays metadata".
- A structure's jigsaw processor references `minecraft:dirt_block` (not a real block); Legendary Monuments' traditional village has a missing start piece.
- EMI can't deserialize Mythic Upgrades' `charged` effect stack; FTB Library warns about Artifacts' Mimic texture.
- Recipe parse errors: Create Deco `placard`, Crafts & Additions `compat/jeed/shocking`, Create Industries `filling/standard_balls/azure_ball` (that one ball can't be filled on a Create line).
- Cobblemon: "Unable to apply dex addition cobblemon:mega_z" (Navas ZA Megas adds to a Pokédex section that doesn't exist; the Megas themselves work).
- Complete Cobblemon Collection's Galarian Koffing/Weezing spawns use an `illager_structures` preset from Myths and Legends, which we don't have; we define it ourselves in `kubejs/data/cobblemon/spawn_detail_presets/` (pillager outposts and woodland mansions).

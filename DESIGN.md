# Cobblemon Pack: Design Brief

Status: **draft v2** (2026-11-09).
- v1 came from the interview with Jack.
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
| 0 | start | 15 | none | Poké Ball, apricorn basics, Create basics, Cobbleworkers basics |
| 1 | Brock | 21 → 27 | none | Great Ball, evolution stones in loot, TRs |
| 2 | Misty | 29 → 34 | none | **Megas**, **Bottle Caps**, **Breeding** (Cobbreeding), shop tier 2, Cobblenav |
| 3 | Lt. Surge | 44 | none | **Ultra Ball** via a Create chain, Z-Moves (bonus), raids ★1–2 |
| 4 | Erika | 46 → 59 | none | Refined Storage, raids ★3–4 |
| 5 | Sabrina | 63 → 68 | **T1** sub-legends | TM crafting, Create egg incubation, specialty balls (Quick/Timer/Dusk…) |
| 6 | Koga | 73 → 76 | **T2** UB + Paradox | Beast Ball, Ultra Wormholes, Tera (bonus), Oritech |
| 7 | Blaine | 79 → 81 | **T3** mythicals + **T4** box legends | Dynamax (bonus), raids ★5–6 |
| 8 | Clair | 81 → 85 | all | **Primal orbs, Rusted Sword/Shield**, Ability Capsule/Patch, Oritech late tier, raids ★7 |
| 9 | Elite Four + Champion Terry (hub) | 100 | all | Battle Tower, one Master Ball per player (quest), endgame |

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
- Raid bosses (Raid Dens)
- Ultra Wormholes for T2
- Rare wild spawns
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
- Known gaps to check: Raid Dens, Ultra Wormholes and Legendary Monuments may run their own capture flow that skips the normal ball-hit event. Where they do, we gate access to the content (raid star tier, wormhole entry, summon item) instead.

### 4.2 Level cap: trainers and EXP (handled by RCT)

Verified in the RCT 0.19.2-beta source: RCT already does both halves, so we configure it rather than write code.
- **Trainer battle gate:** every RCT trainer refuses to battle if your party's highest-level Pokémon is above your cap ("over level cap"). It refuses; there's no scaling down.
  - This applies to **all** RCT trainers, not only gyms. The v2 idea of leaving roaming trainers uncapped isn't possible without patching RCT, and isn't needed: the EXP cap means only caught over-cap mons can trip it, and you box those first.
- **EXP stops at the current cap** (`allowOverLeveling = false`, RCT's default), with an action-bar warning.
  - Rare Candy and EXP Candy go through the same Cobblemon EXP event, so they respect the cap too, and a candy that would add nothing isn't used up.
  - Caught over-cap mons keep their level. They just can't gain more and can't battle trainers until the cap catches up.
- **Config** (shipped as `defaultconfigs/rctmod-server.toml`, copied into each new world): `initialSeries = "radicalred"`, so everyone starts in the series without visiting a Trainer Association; initial cap 15 and over-leveling off are RCT's defaults.

### 4.3 Balls & items (recipe changes via KubeJS)

- **Stage seals** [proposed]: one custom KubeJS item per badge, given as the gym quest's reward and used as an ingredient in stage-locked recipes.
  - Recipes in Minecraft are global, not per-player, so an ingredient only you can earn is the simplest per-player gate.
  - Seals can be handed to friends; that's fine under "trust the group".
  - If PokeBadges' badges can be used as **ingredients that aren't used up** (to check in KubeJS 2101), the badges themselves become the seals and we drop the extra item.
- Balls:
  - Poké → Great (S1) → Ultra, which needs Create processing (S3) → specialty balls (S5) → Beast (S6).
  - **Master Ball is never craftable or lootable.** One per player comes from the S9 quest.
  - We try *Create: Cobblemon Balls Overhaul*. If it breaks on 1.8, we write our own Create recipe chain in KubeJS.
- **Only the truly broken items are held back** [decided], each at its parity point (§3.2):
  - Mega Bracelet and Mega Stones: from S2
  - Bottle Caps: from S2
  - Primal orbs (Red/Blue Orb), Rusted Sword/Shield: from S8
  - Ability Capsule/Patch: from S8
  - Master Ball: S9 quest only
- Everything else stays craftable and lootable as normal: Rare Candy, EXP Candy, evolution stones, and competitive held items (Choice items, Life Orb, Leftovers).
  - The EXP cap stops candies from over-leveling (verified, §4.2).

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

### 4.6 Battle mechanics & side systems

| System | Gate |
|---|---|
| Megas / Z-Moves / Tera / Dynamax (Mega Showdown) | S2 / S3 / S6 / S7, by gating their key items (Mega Bracelet, Z-Ring, Tera Orb, Dynamax Band). Megas are parity; the other three are player-only bonuses |
| Primal Reversion, Crowned forms | S8 (Red/Blue Orb, Rusted Sword/Shield) |
| Raid Dens | Star tiers by stage (config or KubeJS) |
| TMs (SimpleTMs) | TRs from S1, TM crafting at S5 |
| Breeding (Cobbreeding) [decided] | Basic breeding S2; Create-driven incubation S5 (a KubeJS recipe/machine tie-in) |
| Cobblenav | Craftable from S2 |
| Battle Tower | S9 |

### 4.7 Tech (light gating) [decided: Create + friends]

- **Create 6** + a couple of addons from S0. It's the backbone for ball, egg and candy production chains.
- **Refined Storage 2** from S4 (the controller recipe needs a stage seal).
- **Oritech** from S6, as the late automation tier.
- No Mekanism, no AE2. One storage mod, not two.

## 5. Mod list

Additions on top of the official pack. "1.8?" shows whether the addon's latest NeoForge 1.21.1 build explicitly supports Cobblemon 1.8:
- ✅ explicitly supports 1.8
- 🟡 recent build that doesn't say
- ⚠️ last updated in the 1.7 era, so test it and drop or replace it if it breaks

### 5.1 Chosen

| Mod | Why | 1.8? |
|---|---|---|
| KubeJS + Rhino | All our gating logic | ✅ |
| FTB Quests / Library / Teams | Quest book, stage rewards | CurseForge-only, check packwiz download permission |
| Cobblemon Quests Reloaded 2.0.2 | FTB Quests tasks for catch/defeat/evolve (replaces the 1.7-only "Cobblemon Quests") | ✅ |
| Radical Cobblemon Trainers 0.19.2 + RCT API 0.16.2 | Trainers, gym leaders, League | 🟡 |
| Radical Gyms & Structures 0.7 | World gyms 5–8 | ✅ |
| Mega Showdown 1.3.3 | Megas, Z, Tera, Dynamax | ✅ |
| Navas ZA Megas 1.8.2 | Legends Z-A megas; adds Accessories, owo-lib and Architectury. Kept if it launches cleanly with Mega Showdown 1.3.3 | 🟡 |
| PokeBadges 2.0 | Physical badges + Badge Box; quests hand them out by command; may double as the stage seals (§4.3) | 🟡 |
| Cobblemon Capture XP | EXP for catching | ✅ |
| Cobblemon Spawn Notification | Server-wide legendary/shiny spawn broadcast | ✅ |
| Cobblemon: SafePastures | Pastured mons can't die (Cobbleworkers) | ✅ |
| Catch Rate Display | Client-only catch-chance UI | ✅ |
| Cobblemon Battle Extras | Battle UI QoL | 🟡 |
| Cobblemon Raid Dens 0.13.5 | Co-op raids, legendary source | 🟡 |
| SimpleTMs 2.3.3 | TMs/TRs | ⚠️ |
| Cobblemon Battle Tower 1.11 | Endgame | 🟡 |
| Legendary Monuments 8.2 | Shrines/summoning | ✅ (says 1.8.1) |
| Cobbleloots 2.5.0-alpha | Loot balls (we retune) | 🟡 |
| Cobblemon Extra Structures 1.3.0 | Exploration | ⚠️ |
| Cobblemon Ultra Wormholes 1.1.1 | T2 source | ⚠️ |
| Cobbleworkers 2.0.7 | Pokémon-powered automation | ✅ |
| Create: Cobblemon Balls Overhaul 0.0.4 | Create ball recipes | ⚠️ (fallback: our own KubeJS recipes) |
| Cobblenav 2.4.2 | Pokénav / spawn finder | 🟡 |
| Cobblemon Utility+ 1.8.0, MoreCobblemonTweaks | QoL | 🟡 |
| Cobbreeding 2.4.1 | Breeding | ✅ (needs ≥ 1.8.2) |
| CobbleDollars 2.0.0-beta | Economy | ⚠️ (last build July 2026) |
| Create 6.0.10 | Tech backbone | n/a |
| Refined Storage 2.0.9 | Mid-game storage | n/a |
| Oritech 1.2.13 | Late tech | n/a |

### 5.2 Remaining candidates (not in unless you say so)

| Mod | My take |
|---|---|
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
  DESIGN.md README.md CHANGELOG.md
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
| Friends on **Modrinth App** | `.mrpack` from GitHub Releases, built by CI | Re-import per release |
| Friends on **CurseForge app** | CF zip export is possible, but Modrinth-only mods complicate it | Not supported by default. Ask them to switch to Prism |
| **Rented server** | Same bootstrap with `-s server` in the startup command, so it updates on restart. Fallback: CI builds a server zip and you upload it over SFTP | One restart |

### 7.3 Branches & release flow

- `main` holds work in progress; your dev instance tracks it.
- `release` is what friends and the server pull.
- To ship: merge to `release` and tag `vX.Y.Z`. CI builds the `.mrpack` and server zip into a GitHub Release, and `CHANGELOG.md` gets a line.
- Friends never see half-finished work.

### 7.4 Dev loop (your machine)

- A separate Prism instance runs the pack from the repo.
- `kubejs/` and `config/` are linked into the instance so edits land straight in git, and the FTB Quests editor saves into the repo.
- I read `logs/kubejs/startup.log`, `logs/kubejs/server.log` and `logs/latest.log` in the instance after each launch (KubeJS 2101 writes its logs there, not under `kubejs/logs/`).
- The details (symlink vs `packwiz serve`, keeping hashes in sync with `packwiz refresh`) get settled in setup.

## 8. Multiplayer / server

- The host needs:
  - NeoForge 21.1.264
  - **8–10 GB RAM** (Create + Oritech + about 110 mods)
  - SFTP access
  - an **editable startup command** for auto-updates (most Pterodactyl-based hosts allow this)
  - automatic backups
- Everyone keeps **solo FTB Teams**. Joining a party shares quest progress, which would break "per-player unlocks".
- Jack is op, with a whitelist.
- Client-only mods (Sodium, Iris, shaders, etc.) are marked client-side in packwiz so the server never downloads them.
- The base pack includes **Sinytra Connector** (it runs Fabric mods on NeoForge). We keep it because the official pack depends on it, but prefer native NeoForge builds for everything we add.

## 9. Roadmap (small, testable steps)

| # | Feature | Done when |
|---|---|---|
| F0 | Repo + packwiz + dev instance (official 1.8.4 + KubeJS + FTB Quests) | Instance launches; logs readable; repo committed |
| **F1** | **Stage advancements + legendary tier locks** (catching and wild battles, admin bypass) | Legends catchable or blocked per stage, verified in game with `/advancement grant` |
| F2 | Level cap via RCT: Radical Red series for everyone, tier stages per the parity rule | New world starts in Radical Red with cap 15; over-cap party refused by trainers; EXP stops at the cap |
| F3 | Stage seals + ball/item recipe gating + Create ball chain | Recipes show seals in EMI/JEI |
| F4 | Stage-aware loot tables | Early chests give no top-tier items |
| F5 | Quest chapters 0–2 + gym-defeat → stage hookup | Beating Gym 1 grants stage 1 |
| F6 | Remaining addons, compatibility-tested in batches. **Mega Showdown first**: RR trainers use Megas from Lt. Surge (gym 3) | Clean launch with every chosen mod |
| F7 | Mechanic/raid/TM/breeding gating | Per the §4.6 table |
| F8 | Economy shops gated | No above-stage purchases |
| F9 | Tech gating (RS, Oritech) | |
| F10 | Release pipeline + server + friend onboarding | A friend updates by pressing Play |

## 10. Open questions (not blocking F0/F1)

1. ~~Pack name~~ Decided: Campfiremons (`campfiremons`).
2. Which rented host (see the requirements in §8).
3. Final cap numbers and the T4 list, after we see RCT's trainer levels.
4. Should Master Ball be the S9 reward only, or also a rare raid ★7 drop?
8. ~~Gym cap: scale or refuse?~~ Decided by RCT: it refuses (§4.2).
5. Who builds the hub town (you, or a schematic)?
6. Does anyone actually need the CurseForge app?
7. Do we keep FTB Chunks/Essentials/Ultimine? They're useful on a server, but not chosen yet.

## 11. Risks to verify early

- **FTB Quests via packwiz:** it's CurseForge-only. If its authors disallow third-party downloads, packwiz-installer would make friends download it by hand. Check in F0.
- **1.7-era addons on Cobblemon 1.8.4** (the ⚠️ rows): test in batches in F6, starting with the ones F1 depends on (none).
- ~~Cobblemon event API in 1.8.4~~ Verified in F1 against the 1.8.4 jar and source (event classes, the subscribe overload, labels, cancel behaviour).
- **Capture flows** in Raid Dens, Ultra Wormholes and Legendary Monuments may bypass ball-hit events (§4.1).
- **How a gym defeat reaches FTB Quests:** RCT ships an advancement per key trainer (e.g. `rctmod:trainers/defeat_leader_brock`, titled "Boulder Badge"), which an FTB Quests advancement task can watch. Confirm in F5.
- ~~Telling gym/League trainers apart in code~~ Not needed: RCT caps every trainer battle (§4.2).
- **RR trainers carry Mega Stones and Primal orbs.** Without Mega Showdown installed it's unverified what RCT does with them. Install and test Mega Showdown before anyone reaches Lt. Surge.

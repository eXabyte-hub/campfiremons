# Changelog

Each `## vX.Y.Z` section becomes that version's GitHub Release notes (`tools/release/build.py`).

## v0.1.14

Already playing? Just press Play: the pack updates itself.

- **Quest book fixes.** "Tools & Weapons", "Home & Building", "Mods & Gear" and a few quest titles no longer show
  "Invalid formatting!". The Master Balls quest now opens once you're Champion (holding one earlier no longer
  completes it) and rewards one Master Ball instead of four.

## v0.1.13

Already playing? Just press Play: the pack updates itself.

- **Rare Pokémon are rarer.** Rare, ultra-rare and Alpha spawns (Ditto, starters and their evolutions, Alpha herds
  and more) turn up about a quarter as often in the wild. Fishing and Poké Snacks are unchanged.
- **No Master Balls from loot balls.** The Master Loot Ball no longer gives Master Balls; the rest of its loot is the same.

## v0.1.12

Nothing to do: just press Play as usual.

- **Discord link:** the server can now share its chat with our Discord: messages both ways, plus joins, deaths and
  advancements. It's all on the server, so there's nothing to install.

## v0.1.11

Already playing? Just press Play: the pack updates itself. Quests from before v0.1.10 keep their progress; quests
in v0.1.10's new chapters may need ticking off again.

- **The quest book works again.** Since v0.1.10 every quest and chapter showed up untitled, and about half of the
  new quests lost their links and their place in the book on every server start. Names, text and links are back.
- **One map to Brock.** New players got two maps to the first gym; now it's one.
- **Right-click harvesting:** right-click a grown crop to pick it; it replants itself.

## v0.1.10

Already playing? Just press Play: the pack updates itself. Your quest progress carries over.

- **A new quest book.** Every chapter is now a map around one big quest, with banners and art:
  - **Guide:** Getting Started, Evolution (every stone and held item), Poké Balls (which balls each gym unlocks),
    Battle Gimmicks (Mega, Z-Moves, Tera, Dynamax), Training (candy, vitamins, mints, Bottle Caps, TMs), Raid Dens
    and Gotta Find 'Em All (Pokédex milestones, fossils, fishing).
  - **Legends:** a catch checklist for every legendary, mythical, Ultra Beast and Paradox Pokémon, with their
    models as icons.
  - **Gym Challenge:** each stage's quests around its badge, with up-to-date directions to every gym.
  - **Mods & Gear:** Tools & Weapons, Armor, Artifacts, Relics, Storage, Home & Building, Create and Oritech.
  - 21 quests that showed no title or text (the Welcome quest among them) have their text back.
- **Graves:** when you die, your items wait in a grave where you fell.

## v0.1.9

Nothing changes in game: just press Play as usual.

- For whoever runs the server: the server starter also works on hosts that start NeoForge themselves (PebbleHost):
  add `-javaagent:campfiremons-server.jar` to the host's startup flags, and it pulls the latest pack before every
  start.

## v0.1.8

Already playing? Just press Play: the pack updates itself.

- Much quieter chat: only legendaries, mythicals, Ultra Beasts and Paradox Pokémon are announced when they spawn,
  and nothing is announced when it despawns or faints. Catches still are: everyone sees when someone catches a
  legendary, a shiny, an ultra-rare, an Alpha and so on (or hatches or revives one). Spawn rates haven't changed:
  they were always Cobblemon's normal ones.

## v0.1.7

Nothing changes in game: just press Play as usual.

- For whoever runs the server: **Chunky** is on the server now, to generate the land around spawn ahead of time so
  exploring doesn't lag. In the console: `chunky spawn`, `chunky radius 3000`, `chunky start` (`chunky progress`
  to check, `chunky continue` after a restart). Best run while nobody's on.

## v0.1.6

Already playing? Just press Play: the pack updates itself.

- The Kanto cities' gym leaders are now the Radical Red ones: talk to Brock in Pewter (or any city gym leader) and
  you're straight into the badge challenge, with no second Brock appearing next to him. Cities you've already
  visited get the change the next time you go there.

## v0.1.5

Already playing? Just press Play: the pack updates itself. This update asks once about an optional download (the
Pokémon music, below). New cities only show up in parts of the world you haven't explored yet.

**Out in the world**
- **Kanto cities:** Pallet, Viridian, Pewter, Cerulean, Vermilion, Lavender, Celadon, Saffron, Fuchsia, Cinnabar and
  the Indigo Plateau, with landmark buildings, shops, trainers and townsfolk.
- Talk to a city's gym leader to challenge them. It's the same badge battle as at the Radical Red gyms, so you can
  win each badge at whichever gym you find first. The city's Kanto advancements tick off with your badges.
- Fixed the Pokémon towns from v0.1.4: their Pokécenters and Pokémarts no longer turn up on their own outside a town,
  towns no longer generate twice, and a Lentimas chest has its loot again.

**Sounds**
- Pokémon battle themes for wild, trainer and PvP battles, the games' cries, and Pokémon jingles for advancements and
  level-ups (CobbleSounds).
- Pokémon music for every biome, the title screen, the Nether and the End. It's a 418 MB download, so the updater
  asks first: leave **CobbleSounds Soundtrack** ticked to get it, or untick it to keep Minecraft's music.

**Looks**
- About 200 Pokémon have new idle, walking and attack animations (CobbleMotion), and walk at speeds that
  match. Wigglytuff can now fly and Togepi can ride on your shoulder.
- Villagers look like people from the Pokémon games, Nurse Joy included (CobbleFolk).
- **Distant Horizons** draws terrain far past your render distance. On a weaker PC, turn it down or off with its
  button in **Options → Video Settings**.

If you already play, turn on the **CobbleSounds** packs, **CobbleFolk Skin Pack** and **Cobblemotion** in
**Options → Resource Packs** (new installs get them on automatically).

## v0.1.4

Already playing? Just press Play: the pack updates itself. A few things below only show up in a **new world**.

**Getting around**
- New worlds start you in **Pallet Town**, and that's where you come back to without a bed.
- **Gym maps:** you get a map to your next gym when you first join and after every gym win, with the distance and
  direction in chat. Lost it? Type `/gymmap`.
- **Brock's gym** (Pewter) now generates far more often and in any land biome, so the first gym is usually a short
  trip away.
- **Waystones** for fast travel between the ones you've found, and **Ping Wheel** to mark a spot or a Pokémon for
  your friends.

**Out in the world**
- Seven **Pokémon towns** (Pallet, Lavender, Cherrygrove, Pacifidlog, Twinleaf, Floaroma, Lentimas) with their own
  Pokécenters, Pokémarts and Pokémon.
- Pokémon in a pasture now produce items (wool, eggs and more), and wild Pokémon show whether you've already caught
  their species.
- Your PC has 60 boxes (new PCs).

**Storage and sorting**
- Sorting now comes from the Sophisticated mods: search, sort and transfer buttons on every chest and your own
  inventory, and the Sophisticated sort key. Inventory Profiles Next is gone.
- **Sophisticated Storage**: tiered chests, barrels and shulker boxes with upgrades, also on minecarts, boats and
  Create contraptions (backpacks too). New keys can highlight nearby chests that hold an item and deposit into or
  restock from them.

**Looks and performance**
- **Faithful 32x** replaces Stay True, plus connected glass and a matching AppleSkin overlay.
- Gym stage-ups and stage finds now show as a big Cobblemon-styled banner.
- Faster loading and rendering (ModernFix, ImmediatelyFast), and the server is protected from a few crash and
  disconnect bugs.
- Fixed crashes when some Pokémon (Lucario and about 50 others) played certain animations.

If you already play, update your resource packs in **Options → Resource Packs**: Stay True is gone, so turn on
**Faithful 32x**, **FFC Default Glass**, **Faithful 32x AppleSkin** (confirm the "incompatible" prompt) and
**Cobblemon Advancement Plaques**, keeping them below Better Leaves. Check **Options → Controls → Key Binds**
(search "sophisticated") for the new sorting and storage keys.

## v0.1.3

Nothing changes in game: just press Play as usual.

- For whoever runs the server: the server starter now works on hosts that only let you choose the server jar. Set
  it to `campfiremons-server.jar` (Java 21); on every start it installs NeoForge if needed, pulls the latest pack and
  starts the server. `start.sh` still works on hosts that take a startup command.

## v0.1.2

Already playing? Just press Play: the pack updates itself.

- Structures no longer pile up on top of each other. Most surface structures now share one layout, with at least
  about 175 blocks between neighbours, and there are fewer of them in crowded biomes like deserts and oceans.
  Pokécenters, PokéStops and Poké Labs are spaced out the same way. Areas you've already explored keep theirs.
- Brock's, Lt. Surge's, Erika's, Sabrina's and Koga's gyms can now generate in Terralith's biomes too, so they're
  usually closer.
- Tom's Simple Storage: connect your chests to a terminal and reach everything from one screen (it works on Create
  contraptions too), with Cobblemon-style textures.
- New resource packs: Stay True (a refreshed take on the vanilla textures) and Cobblemon Pasture Enhanced (see at a
  glance when a pasture has an egg). New installs get them on automatically; if you already play, turn on Stay True,
  Cobblemon Pasture Enhanced and Tom's Cobblemoned in **Options → Resource Packs**.
- Inventory Profiles Next's extra buttons no longer cover other parts of the screen.

## v0.1.1

Already playing? Just press Play: the pack updates itself.

- Pokécenters and PokéStops out in the world, with a healing machine and a PC. Rare Poké Labs have extra loot
  (including stage finds).
- Sophisticated Backpacks, with Cobblemon upgrades: open your PC, heal your party (on a cooldown) or cook on the go.
- Pokémon show as icons on the minimap.
- Structures are spread out: about half as many on the surface, and a quarter as many When Dungeons Arise
  dungeons. Areas you've already explored keep theirs.
- Terralith's welcome message is gone.

## v0.1.0

First release for the group.

- Cobblemon Official Modpack 1.8.4 base on NeoForge 21.1.264, plus our additions (DESIGN.md §5).
- Radical Red gym run through Radical Cobblemon Trainers: beating each gym leader grants the next stage, and the
  level cap follows your next key fight.
- Legendary tiers unlock by stage (sub-legends S5, Ultra Beasts and Paradox S6, mythicals and box legends S7).
- Power items are stage finds in structure chests, rolled per player. Balls, Bottle Caps, TMs/TRs and Cobblenav
  are use-locked by stage.
- Raid Dens open by star tier, the Battle Tower at Stage 4, Ultra Space at Stage 6. Breeding is open from the start.
- Quest book with one chapter per stage.
- Vanilla passive mobs removed (frogs and bees stay); defeated Pokémon drop their materials instead.
- Every Pokémon has a model (Complete Cobblemon Collection), and all 1,559 trainers have their own skin.
- Shaders (Complementary Reimagined) and the mods' extra texture packs are on by default.
- Quality of life: Mouse Tweaks, Jade, Controlling, Inventory Profiles Next (sort key) and Zume (zoom).

Install with Prism: see the [README](https://github.com/eXabyte-hub/campfiremons#installing).

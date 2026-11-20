# Quest book builder

Rebuilds `config/ftbquests/quests/` from the original v0.1.9 book (commit 8b5548e): hub layouts, banners and the
topic chapters (DESIGN.md, FTB Quests row). Run `tools/quest_book/rebuild.sh`; it validates the result (IDs, items,
textures, links, overlaps). `python3 tools/quest_book/preview.py [chapter...]` renders layout previews into
`previews/` (git-ignored). Both read item models and textures from the mod jars of your Campfiremons Prism instance
(the one with the most jars), or from the folder in `$MODS`.

All quest, chapter and group text ends up in one table, `lang/en_us.snbt`: the only layout FTB Quests 2101 loads.
The builder still reads the original book's per-chapter `lang/en_us/` files and merges them at the end.

- `build_book.py`: the book (Getting Started, stage hubs, Evolution, Gotta Find 'Em All, Poké Balls, Battle
  Gimmicks, Legends, Artifacts, groups and titles). Keeps every quest ID from the original book.
- `mods_chapters.py`: the mod chapters (Create, Oritech, Storage, Relics, Training, Home & Building, Tools &
  Weapons, Armor, Raid Dens), mostly through `branch_chapter()`.
- `data/`: item IDs per mod (`all_items.json`, from the dev instance's jars), weapon/armor stats and creative tabs
  (`dump.txt`, from a KubeJS dump on a test server) and species labels (`species_labels.json`). Refresh them after
  updating the mods involved.
- Art: `tools/gen_quest_art.py` (banners and backgrounds).
- `add_mythic_armor.py`: added the Mythic Upgrades armour sets to the live Armor chapter (v0.1.20), which `armor()`
  skipped because the dump gives their material as "?". It edits the book in place and does nothing once they're in.
- `type_tooltips.py`: hover text for every type icon (`tera_types` images), from a type chart, written as `image.<id>.title` in `lang/en_us.snbt` (FTB shows an image's title as its tooltip), plus a Bulbapedia link as each icon's click action: FTB ignores the mouse over images without one, so their tooltips never show. Re-run after adding type icons; safe to run on the live book (it only touches those keys).
- `rewards.py`: the rewards overhaul (v0.1.35). Every quest keeps its XP and gets items from its own mod's pool
  (`POOLS`, picked by the quest's item tasks, else the chapter), sized by its XP (1, 2-3, 4-6, 7+), plus
  CobbleDollars on medium and bigger quests (a `command` reward, `/cobbledollars give @s N` at permission level 2,
  titled through `reward.<id>.title`). Existing item rewards are kept and doubled, except the one-offs in
  `KEEP_COUNT` (the Master Ball, the trainer card). It gives every reward a new ID, which re-opens all claims while
  keeping progress, so it refuses to run again unless you pass `--again`. To change rewards later, edit the book
  in place, or extend the script to keep IDs.

New quest IDs are random on every rebuild, and in-game edits made after a rebuild are lost on the next one: port
them into the builder first. Since v0.1.10 is live, a rebuild would also reset players' progress on every quest added
in v0.1.10, so `rebuild.sh` refuses to run without `--new-ids`. To extend the book, edit `config/ftbquests/quests/`
in place (or in game), or first teach the builder to reuse the IDs already in the book.

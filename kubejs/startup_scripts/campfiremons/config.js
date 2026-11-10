// Campfiremons gating config (DESIGN.md §3–4). Edit, then `/kubejs reload startup` in game.
// Lives in startup_scripts because KubeJS only lets startup scripts write to `global`.
// Read at event time by the other campfiremons scripts, so file load order doesn't matter.

global.campfiremonsConfig = {
  // A player's stage is the highest campfiremons:stage/N advancement they have (0 if none).
  maxStage: 9,

  // Legendary tiers and the stage that unlocks each one (parity rule, DESIGN.md §3.2: Radical Red trainers use
  // every tier from Giovanni's 3rd team and Clair onward, which you face at Stage 7; T1/T2 ramp in earlier).
  tiers: {
    sub_legendary: { name: 'Sub-legendary', stage: 5 },
    beast_paradox: { name: 'Ultra Beast / Paradox', stage: 6 },
    mythical: { name: 'Mythical', stage: 7 },
    restricted: { name: 'Box legend', stage: 7 },
  },

  // Species are sorted into tiers by their Cobblemon labels; the first matching rule wins.
  // ('restricted' must come before 'legendary': box legends carry both labels.)
  labelRules: [
    { label: 'restricted', tier: 'restricted' },
    { label: 'mythical', tier: 'mythical' },
    { label: 'ultra_beast', tier: 'beast_paradox' },
    { label: 'paradox', tier: 'beast_paradox' },
    { label: 'legendary', tier: 'sub_legendary' },
  ],

  // Per-species exceptions: Cobblemon species id (e.g. 'hooh', 'tapukoko') -> tier id, or null to never lock it.
  overrides: {
    arceus: 'restricted', // labelled mythical, but it belongs with the box legends
  },

  // Use-locks (DESIGN.md §4.3, server_scripts/campfiremons/item_locks.js): crafting stays free, but throwing or using
  // one of these below its stage is refused. Balls follow Cobblemon's own material tiers (tier_N_poke_ball_materials);
  // tier 1 balls (Poké, Premier, Heal, Safari, apricorn colour balls) are never locked.
  itemLocks: {
    1: [ // tier 2 balls (+ their Hisuian "ancient" equivalents)
      'cobblemon:great_ball', 'cobblemon:net_ball', 'cobblemon:dive_ball', 'cobblemon:nest_ball', 'cobblemon:level_ball',
      'cobblemon:lure_ball', 'cobblemon:heavy_ball', 'cobblemon:moon_ball', 'cobblemon:friend_ball', 'cobblemon:fast_ball',
      'cobblemon:sport_ball', 'cobblemon:park_ball',
      'cobblemon:ancient_great_ball', 'cobblemon:ancient_wing_ball', 'cobblemon:ancient_leaden_ball',
    ],
    2: [ // Bottle Caps (parity: Radical Red trainers have perfect IVs); Withered caps lower IVs and stay free
      'obc:bottle_cap', 'obc:bottle_cap_hp', 'obc:bottle_cap_attack', 'obc:bottle_cap_defence',
      'obc:bottle_cap_special_attack', 'obc:bottle_cap_special_defence', 'obc:bottle_cap_speed', 'obc:bottle_cap_gold',
      // Cobblenav's spawn finders
      'cobblenav:pokenav_item', 'cobblenav:pokenav_item_old', 'cobblenav:pokefinder_item', 'cobblenav:fishingnav_item',
    ],
    3: [ // tier 3 balls (+ ancient equivalents)
      'cobblemon:ultra_ball', 'cobblemon:quick_ball', 'cobblemon:dusk_ball', 'cobblemon:timer_ball',
      'cobblemon:repeat_ball', 'cobblemon:luxury_ball', 'cobblemon:love_ball',
      'cobblemon:ancient_ultra_ball', 'cobblemon:ancient_jet_ball', 'cobblemon:ancient_gigaton_ball',
    ],
    6: ['cobblemon:dream_ball', 'cobblemon:beast_ball'], // tier 4 balls
    // Stage 8 finds, but Cobbleloots, Raid Dens and Legendary Monuments loot can drop them earlier
    8: ['cobblemon:ability_capsule', 'cobblemon:ability_patch'],
    // The Champion's reward; its recipe is removed, but Cobbleloots and the (post-game) Battle Tower shop have them.
    // The Hisuian Origin Ball is the same guaranteed catch.
    9: ['cobblemon:master_ball', 'cobblemon:ancient_origin_ball'],
  },
  // Same use-locks by item tag (for mods that register an item per move, like SimpleTMs)
  itemTagLocks: {
    1: ['simpletms:tr_items'], // single-use TRs
    5: ['simpletms:tm_items'], // reusable TMs
  },

  // Vanilla animals that never appear (Pokémon cover their drops; frogs and bees stay for Froglights and pollination).
  // server_scripts/campfiremons/removed_mobs.js cancels them joining the world (structure pens, village cats,
  // trader llamas, spawn eggs); KEEP IN SYNC with kubejs/data/campfiremons/neoforge/biome_modifier/
  // remove_passive_mobs.json, which stops their natural spawns.
  removedMobs: [
    'minecraft:cow', 'minecraft:pig', 'minecraft:sheep', 'minecraft:chicken', 'minecraft:rabbit', 'minecraft:mooshroom',
    'minecraft:horse', 'minecraft:donkey', 'minecraft:mule', 'minecraft:llama', 'minecraft:trader_llama',
    'minecraft:camel', 'minecraft:wolf', 'minecraft:cat', 'minecraft:ocelot', 'minecraft:fox', 'minecraft:parrot',
    'minecraft:squid', 'minecraft:glow_squid', 'minecraft:cod', 'minecraft:salmon', 'minecraft:tropical_fish',
    'minecraft:pufferfish', 'minecraft:dolphin', 'minecraft:turtle', 'minecraft:axolotl',
    'minecraft:goat', 'minecraft:panda', 'minecraft:polar_bear', 'minecraft:armadillo', 'minecraft:sniffer',
    'minecraft:bat',
  ],

  // Held-item locks (tier_locks.js, at battle start): these work just by being held, so a use-lock can't stop them.
  // A battle is refused while a party Pokémon holds one above your stage. Stage 8 finds, but Legendary Monuments
  // has its own chests and recipes for them.
  heldItemLocks: {
    8: ['mega_showdown:red_orb', 'mega_showdown:blue_orb', 'mega_showdown:rusted_sword', 'mega_showdown:rusted_shield'],
  },
}

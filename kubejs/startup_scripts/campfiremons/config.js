// Campfiremons gating config (DESIGN.md §3–4). Edit, then `/kubejs reload startup` in game.
// Lives in startup_scripts because KubeJS only lets startup scripts write to `global`.
// Read at event time by the other campfiremons scripts, so file load order doesn't matter.

global.campfiremonsConfig = {
  // A player's stage is the highest campfiremons:stage/N advancement they have (0 if none).
  maxStage: 9,

  // Legendary tiers and the stage that unlocks each one.
  tiers: {
    sub_legendary: { name: 'Sub-legendary', stage: 4 },
    beast_paradox: { name: 'Ultra Beast / Paradox', stage: 6 },
    mythical: { name: 'Mythical', stage: 8 },
    restricted: { name: 'Box legend', stage: 9 },
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
}

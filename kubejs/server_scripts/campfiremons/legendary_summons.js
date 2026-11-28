// Using a summon item (startup_scripts/campfiremons/legendary_items.js) brings its legendary out as a wild Pokémon a
// few blocks in front of you, to battle and catch like any other (asked for on 2026-11-28). Below the Pokémon's tier
// stage the item is refused and kept, the same stages as the tier locks: a wild one couldn't be caught yet anyway.

const LEGENDARY_SUMMONS = {
  'campfiremons:soul_heart': { pokemon: 'magearna level=70', name: 'Magearna', stage: 7 },
  'campfiremons:genesect_drive': { pokemon: 'genesect level=70', name: 'Genesect', stage: 7 },
  'campfiremons:poisoned_mochi': { pokemon: 'pecharunt level=70', name: 'Pecharunt', stage: 7 },
  'campfiremons:beast_memory': { pokemon: 'typenull level=60', name: 'Type: Null', stage: 5 },
  // Rayquaza (asked for on 2026-11-28: the most sought-after, so the hardest): only on the roof of an End City in the
  // outer End, the same place its rare wild spawn needs (tools/gen_legend_spawns.py)
  // Even there it answers only 1 time in 4 (asked for on 2026-11-28); the orb is used up either way
  'campfiremons:jade_orb': { pokemon: 'rayquaza level=75', name: 'Rayquaza', stage: 7, where: jadeOrbPlace,
    elsewhere: 'The Jade Orb stays dark. Rayquaza answers only from high in the outer End, on the roof of an End City.',
    chance: 0.25, unanswered: 'The Jade Orb flares and crumbles to dust. Rayquaza did not answer this time.' },
}
const SUMMON_DISTANCE = 3
const JADE_ORB_MIN_Y = 110
const JADE_ORB_BIOMES = ['minecraft:end_highlands', 'minecraft:end_midlands']
const JADE_ORB_BLOCKS = ['minecraft:purpur_block', 'minecraft:purpur_pillar', 'minecraft:purpur_stairs', 'minecraft:purpur_slab']
const JADE_ORB_REACH = 3 // blocks around and below the player searched for purpur

// Standing high in the outer End with purpur under or beside you: an End City roof
function jadeOrbPlace(player) {
  let level = player.level
  if (String(level.dimension) != 'minecraft:the_end' || player.y < JADE_ORB_MIN_Y) return false
  let biome = String(level.getBiome(player.blockPosition()).unwrapKey().get().location())
  if (JADE_ORB_BIOMES.indexOf(biome) < 0) return false
  let base = player.blockPosition()
  for (let dx = -JADE_ORB_REACH; dx <= JADE_ORB_REACH; dx++) {
    for (let dz = -JADE_ORB_REACH; dz <= JADE_ORB_REACH; dz++) {
      for (let dy = -JADE_ORB_REACH; dy <= 1; dy++) {
        if (JADE_ORB_BLOCKS.indexOf(String(level.getBlock(base.offset(dx, dy, dz)).id)) >= 0) return true
      }
    }
  }
  return false
}

Object.keys(LEGENDARY_SUMMONS).forEach(id => {
  ItemEvents.rightClicked(id, event => {
    let player = event.player
    let summon = LEGENDARY_SUMMONS[id]
    let helpers = global.campfiremons
    if (!helpers.isBypassed(player) && helpers.playerStage(player) < summon.stage) {
      helpers.deny(player, Text.red(`${summon.name} answers only from Stage ${summon.stage}.`))
      event.cancel()
      return
    }
    if (summon.where && !summon.where(player)) {
      helpers.deny(player, Text.gray(summon.elsewhere))
      event.cancel()
      return
    }
    if (summon.chance && Math.random() >= summon.chance) {
      if (!player.isCreative()) event.item.shrink(1)
      player.tell(Text.gray(summon.unanswered))
      console.info(`[campfiremons] ${player.username} used ${id}: no ${summon.name} this time`)
      event.cancel()
      return
    }
    let look = player.getLookAngle()
    let x = player.x + look.x() * SUMMON_DISTANCE
    let z = player.z + look.z() * SUMMON_DISTANCE
    let dimension = String(player.level.dimension)
    event.server.runCommandSilent(`execute in ${dimension} positioned ${x.toFixed(2)} ${player.y.toFixed(2)} ${z.toFixed(2)} run pokespawn ${summon.pokemon}`)
    if (!player.isCreative()) event.item.shrink(1)
    player.tell(Text.gold(`${summon.name} appears!`))
    console.info(`[campfiremons] ${player.username} summoned ${summon.name} with ${id}`)
    event.cancel()
  })
})

ServerEvents.recipes(event => {
  // Every part takes a boss or the outer End: Dragon's Breath from a (respawned) Ender Dragon, the Dragon Head and the
  // Elytra from End ships, the Nether Star from the Wither
  event.shaped('campfiremons:jade_orb', ['DHD', 'ENE', 'DLD'], {
    D: 'minecraft:dragon_breath',
    H: 'minecraft:dragon_head',
    E: 'minecraft:emerald_block',
    N: 'minecraft:nether_star',
    L: 'minecraft:elytra',
  }).id('campfiremons:crafting/jade_orb')

  event.custom({
    type: 'create:mechanical_crafting',
    pattern: ['  G  ', ' BPB ', 'GPHPG', ' BPB ', '  G  '],
    key: {
      G: { item: 'minecraft:gold_block' },
      B: { item: 'create:brass_block' },
      P: { item: 'create:precision_mechanism' },
      H: { item: 'minecraft:heart_of_the_sea' },
    },
    result: { id: 'campfiremons:soul_heart', count: 1 },
    accept_mirrored: false,
  }).id('campfiremons:mechanical_crafting/soul_heart')

  event.custom({
    type: 'create:mechanical_crafting',
    pattern: ['T T', 'PNP', 'TET'],
    key: {
      T: { item: 'create:electron_tube' },
      P: { item: 'create:precision_mechanism' },
      N: { item: 'minecraft:netherite_ingot' },
      E: { item: 'minecraft:ender_eye' },
    },
    result: { id: 'campfiremons:genesect_drive', count: 1 },
    accept_mirrored: false,
  }).id('campfiremons:mechanical_crafting/genesect_drive')

  event.custom({
    type: 'create:mixing',
    heat_requirement: 'heated',
    ingredients: [{ item: 'cobblemon:potato_mochi' }, { item: 'minecraft:poisonous_potato' }, { item: 'minecraft:fermented_spider_eye' }],
    results: [{ id: 'campfiremons:poisoned_mochi', count: 1 }],
  }).id('campfiremons:mixing/poisoned_mochi')
})

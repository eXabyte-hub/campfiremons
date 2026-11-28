// Using a summon item (startup_scripts/campfiremons/legendary_items.js) brings its legendary out as a wild Pokémon a
// few blocks in front of you, to battle and catch like any other (asked for on 2026-11-28). Below the Pokémon's tier
// stage the item is refused and kept, the same stages as the tier locks: a wild one couldn't be caught yet anyway.

const LEGENDARY_SUMMONS = {
  'campfiremons:soul_heart': { pokemon: 'magearna level=70', name: 'Magearna', stage: 7 },
  'campfiremons:genesect_drive': { pokemon: 'genesect level=70', name: 'Genesect', stage: 7 },
  'campfiremons:poisoned_mochi': { pokemon: 'pecharunt level=70', name: 'Pecharunt', stage: 7 },
  'campfiremons:beast_memory': { pokemon: 'typenull level=60', name: 'Type: Null', stage: 5 },
}
const SUMMON_DISTANCE = 3

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

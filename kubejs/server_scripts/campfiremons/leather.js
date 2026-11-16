// Rotten flesh cooks into leather (asked for on 2026-11-16). The pack has no cows (config.js `removedMobs`), so
// leather otherwise only drops from beating Tauros, Miltank, Ponyta and a dozen other Pokémon. Furnace, smoker and
// campfire, one flesh for one leather, like many packs do; the campfire is the slow, fuel-free one.

ServerEvents.recipes(event => {
  event.smelting('minecraft:leather', 'minecraft:rotten_flesh').xp(0.1).id('campfiremons:leather_from_rotten_flesh')
  event.smoking('minecraft:leather', 'minecraft:rotten_flesh').xp(0.1).id('campfiremons:leather_from_rotten_flesh_smoking')
  event.campfireCooking('minecraft:leather', 'minecraft:rotten_flesh').cookingTime(600).id('campfiremons:leather_from_rotten_flesh_campfire')
})

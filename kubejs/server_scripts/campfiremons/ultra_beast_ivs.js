// No Ultra Beast comes with six perfect IVs (asked for on 2026-11-27). CobbleSafari's Ultra Warp Ride gives every reward a
// fixed number of perfect IVs by portal rank (rewards.ivPerfectCount [3, 4, 5, 6] in its ultra_warp_ride/difficulty.json),
// and at rank 3 half its rewards are Ultra Beasts from its reward pool, so it handed out 6-IV Ultra Beasts. The table is
// left alone (other rank-3 rewards keep their six); instead, when a wild Ultra Beast with all six IVs at 31 joins the
// world, one of them is rerolled to 0-30. That covers any other source too (Ultra Space wormhole ones have random IVs
// anyway). Bottle Caps can still perfect one after it's caught.

const $UbIvStats = Java.loadClass('com.cobblemon.mod.common.api.pokemon.stats.Stats')
const UB_IV_STATS = ['HP', 'ATTACK', 'DEFENCE', 'SPECIAL_ATTACK', 'SPECIAL_DEFENCE', 'SPEED']

// The stat rerolled, or null if this Pokémon is left as it is.
function capUltraBeastIvs(pokemon) {
  if (!pokemon.species.labels.contains('ultra_beast')) return null
  let stats = UB_IV_STATS.map(name => $UbIvStats[name])
  if (!stats.every(stat => pokemon.getIvs().get(stat) == 31)) return null
  let stat = stats[Math.floor(Math.random() * stats.length)]
  pokemon.setIV(stat, Math.floor(Math.random() * 31))
  return stat
}

EntityEvents.spawned('cobblemon:pokemon', event => {
  let pokemon = event.entity.getPokemon()
  if (!pokemon || !pokemon.isWild()) return
  let stat = capUltraBeastIvs(pokemon)
  if (stat) console.info(`[campfiremons] wild ${pokemon.species.name} had six perfect IVs; ${stat} rerolled to ${pokemon.getIvs().get(stat)}`)
})

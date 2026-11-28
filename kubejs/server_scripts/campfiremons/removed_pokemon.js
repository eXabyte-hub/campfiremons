// Pokémon the server takes back, by UUID (asked for on 2026-11-27 and 2026-11-28): a Lv 78 Poipole with six perfect IVs
// that the Ultra Warp Ride handed out before ultra_beast_ivs.js, and a shiny six-perfect-IV Xerneas revived from a
// CobbleSafari fossil before fossils.js. Whoever holds one loses it from their party or PC when they next log in.
// A Pokémon's UUID stays the same through evolution and trades, and nothing else shares it.

const $RemovedCobblemon = Java.loadClass('com.cobblemon.mod.common.Cobblemon')

const REMOVED_POKEMON = {
  '57278ff4-dd74-434e-ba26-54b73b9f4b37': 'a Lv 78 Poipole with six perfect IVs from the Ultra Warp Ride',
  'f6408dd1-3516-4e87-89d9-ed49afe3ce2f': 'a shiny Lv 1 Xerneas with six perfect IVs revived from a fossil',
}

// What was removed from this player, as descriptions.
function removeTakenBackPokemon(player) {
  let storage = $RemovedCobblemon.INSTANCE.storage
  let removed = []
  ;[storage.getParty(player), storage.getPC(player)].forEach(store => {
    let found = []
    store.forEach(pokemon => { if (String(pokemon.getUuid()) in REMOVED_POKEMON) found.push(pokemon) })
    found.forEach(pokemon => {
      if (store.remove(pokemon)) removed.push(REMOVED_POKEMON[String(pokemon.getUuid())] + ` (now ${pokemon.species.name})`)
    })
  })
  return removed
}

PlayerEvents.loggedIn(event => {
  removeTakenBackPokemon(event.player).forEach(what => console.info(`[campfiremons] took back ${what} from ${event.player.username}`))
})

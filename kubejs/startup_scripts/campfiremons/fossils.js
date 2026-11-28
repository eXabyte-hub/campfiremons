// Fossil revivals (asked for on 2026-11-28). CobbleSafari's Underground fossils revive a random species: the Random,
// Shiny, Hidden Ability, Max IV and Perfect Fossils use Cobblemon's "random" property, which picks from every species,
// legendaries included, and a revived Pokémon goes straight to its owner, past the tier locks. The Max IV and Perfect
// Fossils also gave six perfect IVs, which made the Underground a faster route to perfect IVs than breeding.
// So when any fossil is revived:
//   - a tier-locked species (legendary, mythical, Ultra Beast, Paradox; tier_locks.js tierOf) becomes a random species
//     that isn't, keeping a hidden ability and shininess if it had them;
//   - six perfect IVs become high but random ones (FOSSIL_IV_MIN to 31 each). A natural six-31 roll is 1 in ~10^9.
// Ordinary fossils (Dome, Helix, ...) revive their own species, which is never tier-locked, so they're untouched.
// Events arrive via cobblemon_hooks.js. The Shiny Fossil's Underground weight is cut in
// kubejs/data/cobblesafari/underground_treasure/fossilshiny.json.

const $FossilSpecies = Java.loadClass('com.cobblemon.mod.common.api.pokemon.PokemonSpecies')
const $FossilProperties = Java.loadClass('com.cobblemon.mod.common.api.pokemon.PokemonProperties')
const $FossilStats = Java.loadClass('com.cobblemon.mod.common.api.pokemon.stats.Stats')
const $FossilPriority = Java.loadClass('com.cobblemon.mod.common.api.Priority')

const FOSSIL_IV_MIN = 20
const FOSSIL_IV_STATS = ['HP', 'ATTACK', 'DEFENCE', 'SPECIAL_ATTACK', 'SPECIAL_DEFENCE', 'SPEED']

// Species a fossil may turn into: implemented and not tier-locked. Built on first use (species load after startup).
let fossilPool = null
function fossilSpeciesPool() {
  if (fossilPool) return fossilPool
  fossilPool = []
  $FossilSpecies.INSTANCE.getImplemented().forEach(species => {
    if (!global.campfiremons.tierOf(species)) fossilPool.push(species)
  })
  return fossilPool
}

// What changed, as text for the log and for tests ('' if nothing).
function fixRevivedPokemon(pokemon) {
  let changes = []
  if (global.campfiremons.tierOf(pokemon.species)) {
    let before = String(pokemon.species.name)
    let hidden = pokemon.ability && pokemon.ability.priority == $FossilPriority.LOW
    let pool = fossilSpeciesPool()
    let species = pool[Math.floor(Math.random() * pool.length)]
    $FossilProperties.Companion.parse(String(species.resourceIdentifier.path) + (hidden ? ' hiddenability' : '')).apply(pokemon)
    if (!hidden) pokemon.rollAbility()
    changes.push(`${before} became ${pokemon.species.name}${hidden ? ' (hidden ability kept)' : ''}`)
  }
  let stats = FOSSIL_IV_STATS.map(name => $FossilStats[name])
  if (stats.every(stat => pokemon.getIvs().get(stat) == 31)) {
    stats.forEach(stat => pokemon.setIV(stat, FOSSIL_IV_MIN + Math.floor(Math.random() * (32 - FOSSIL_IV_MIN))))
    changes.push('six perfect IVs became ' + stats.map(stat => pokemon.getIvs().get(stat)).join('/'))
  }
  return changes.join('; ')
}

global.campfiremons = global.campfiremons || {}
global.campfiremons.fixRevivedPokemon = fixRevivedPokemon
global.campfiremons.onFossilRevived = event => {
  let what = fixRevivedPokemon(event.pokemon)
  let player = event.player
  if (what) console.info(`[campfiremons] fossil revived for ${player ? player.gameProfile.name : 'nobody'}: ${what}`)
}

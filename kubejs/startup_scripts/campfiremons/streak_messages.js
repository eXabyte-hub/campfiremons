// Tells a player in chat when their catch streak reaches a shiny step (asked for on 2026-11-25): at 10, 20 and 40 of a
// species in a row, with the odds it unlocked. Counter's own message (config/cobbled_counter.json) shows the running
// streak above the hotbar on every catch; this one stays readable in chat. The steps and extra rolls are read from
// Unchained's wild spawn booster (config/unchained/spawn/shinySpawnBooster.json), so they always match the real odds.
// cobblemon_hooks.js forwards Counter's RECORD_POST (a catch, KO, hatch... counted) to onStreakRecorded.

const $StreakCobblemon = Java.loadClass('com.cobblemon.mod.common.Cobblemon')
const $StreakPlayers = Java.loadClass('com.cobblemon.mod.common.util.PlayerExtensionsKt') // UUID -> online player

// [1 in N] for this many catches in a row if it is exactly a step, else 0
function streakOdds(count) {
  let booster = Java.loadClass('us.timinc.mc.cobblemon.unchained.Unchained').INSTANCE.getShinySpawnBooster()
  if (!booster.getEnabled()) return 0
  let extra = 0
  booster.getThresholds().forEach((step, rolls) => {
    if (Number(step) == count) extra = Number(rolls)
  })
  return extra > 0 ? Math.round($StreakCobblemon.INSTANCE.getConfig().getShinyRate() / (1 + extra)) : 0
}

// "Pawniard catch streak: 10!" + " Shiny odds are now 1 in 4096 for you."
function streakMessage(pokemon, form, count, odds) {
  let name = Text.of(pokemon.getSpecies().getTranslatedName())
  if (form != 'Normal' && form != 'untracked') name.append(` (${form})`)
  return Text.gold(name.append(` catch streak: ${count}!`)).append(Text.yellow(` Shiny odds are now 1 in ${odds} for you.`))
}

global.campfiremons = global.campfiremons || {}
global.campfiremons.streakOdds = streakOdds
global.campfiremons.streakMessage = streakMessage

global.campfiremons.onStreakRecorded = event => {
  if (String(event.getCounterType().getType()) != 'capture') return
  let count = event.getManager().getStreak(event.getCounterType()).getCount()
  let odds = streakOdds(count)
  if (odds == 0) return
  let uuid = event.getManager().getUuid()
  let player = $StreakPlayers.getPlayer(uuid)
  console.info(`[campfiremons] catch streak ${count} of ${event.getSpeciesId()} for ${player ? player.username : uuid}, shiny 1 in ${odds}`)
  if (player) player.tell(streakMessage(event.getPokemon(), String(event.getFormName()), count, odds))
}

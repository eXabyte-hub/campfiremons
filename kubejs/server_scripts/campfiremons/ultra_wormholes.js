// Ultra Space wormholes open for Stage 6+ players only, and often enough to matter (asked for on 2026-11-26).
// Cobblemon Ultra-Beasts' own spawner rolls 1 in WORMHOLE_SPAWN_CHANCE every TRY_SPAWN_INTERVAL ticks and opens the one
// wormhole next to a random overworld player of any stage: at its default 1 in 2000 per 20 s, about one every 11 hours,
// and often next to someone ultra_space.js turns away. config/cobblemon_ultrabeast/main.json sets its chance to 1 in a
// billion, and this does the rolling instead: every WORMHOLE_ATTEMPT_TICKS, if a Stage 6+ player is in the overworld
// and no wormhole is open and nobody is in Ultra Space, 1 in WORMHOLE_ODDS opens one next to one of them, through the
// mod's own forceSpawnToPlayer (its /ultrabeasts wormhole spawn). Entering still takes a right-click.
// 1 in 90 every 20 s averages one about every 30 minutes while someone eligible is on.

const $UbWormhole = Java.loadClass('dev.darcosse.ultrabeasts.entity.WormholeEntity')
const $UbSession = Java.loadClass('dev.darcosse.ultrabeasts.handler.UltraSpaceSession')

const WORMHOLE_ATTEMPT_TICKS = 400
const WORMHOLE_ODDS = 90

function wormholeEligible(player) {
  if (player.isSpectator() || player.isCreative()) return false
  return global.campfiremons.playerStage(player) >= global.campfiremonsConfig.tiers.beast_paradox.stage
}

ServerEvents.tick(event => {
  let server = event.server
  if (server.tickCount % WORMHOLE_ATTEMPT_TICKS != 0) return
  let overworld = server.overworld()
  let eligible = []
  server.getPlayerList().getPlayers().forEach(p => {
    if (String(p.level.dimension) == 'minecraft:overworld' && wormholeEligible(p)) eligible.push(p)
  })
  if (eligible.length == 0) return
  if ($UbWormhole.hasActiveWormhole(overworld) || $UbSession.isOccupied(server)) return
  if (Math.random() * WORMHOLE_ODDS >= 1) return
  let player = eligible[Math.floor(Math.random() * eligible.length)]
  if ($UbWormhole.forceSpawnToPlayer(overworld, player, null)) {
    console.info(`[campfiremons] Ultra Space wormhole opened next to ${player.username}`)
  }
})

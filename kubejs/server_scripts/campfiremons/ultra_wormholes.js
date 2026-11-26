// Ultra Space wormholes open for Stage 6+ players only, at random times (asked for on 2026-11-26 and 2026-11-27).
// Cobblemon Ultra-Beasts' own spawner rolls 1 in WORMHOLE_SPAWN_CHANCE every TRY_SPAWN_INTERVAL ticks and opens the one
// wormhole next to a random overworld player of any stage: at its default 1 in 2000 per 20 s, about one every 11 hours,
// and often next to someone ultra_space.js turns away. config/cobblemon_ultrabeast/main.json sets its chance to 1 in a
// billion, and this opens them instead, through the mod's own forceSpawnToPlayer (its /ultrabeasts wormhole spawn),
// next to a Stage 6+ player in the overworld. Entering still takes a right-click.
//
// v0.1.50 rolled 1 in 90 every 20 s (about 30 minutes on average), which can open three in half an hour (it did, on
// 2026-11-26). Now each wormhole is followed by a random wait of WORMHOLE_GAP_MIN to WORMHOLE_GAP_MAX minutes, an hour on
// average. The wait only counts down while a Stage 6+ player is in the overworld, no wormhole is open and nobody is in
// Ultra Space, and it's kept in the server's persistent data, so restarts don't reset it.

const $UbWormhole = Java.loadClass('dev.darcosse.ultrabeasts.entity.WormholeEntity')
const $UbSession = Java.loadClass('dev.darcosse.ultrabeasts.handler.UltraSpaceSession')

const WORMHOLE_CHECK_TICKS = 400 // 20 s
const WORMHOLE_GAP_MIN = 30 // minutes
const WORMHOLE_GAP_MAX = 90
const WORMHOLE_WAIT_KEY = 'campfiremonsWormholeWait' // ticks left

function wormholeEligible(player) {
  if (player.isSpectator() || player.isCreative()) return false
  return global.campfiremons.playerStage(player) >= global.campfiremonsConfig.tiers.beast_paradox.stage
}

function nextWormholeWait() {
  return Math.round((WORMHOLE_GAP_MIN + Math.random() * (WORMHOLE_GAP_MAX - WORMHOLE_GAP_MIN)) * 60 * 20)
}

// One check with these eligible players; returns what happened, for the log and for tests.
function ultraWormholeStep(server, eligible) {
  let overworld = server.overworld()
  if ($UbWormhole.hasActiveWormhole(overworld) || $UbSession.isOccupied(server)) return 'busy'
  let data = server.persistentData
  if (!data.contains(WORMHOLE_WAIT_KEY)) {
    data.putInt(WORMHOLE_WAIT_KEY, nextWormholeWait())
    console.info(`[campfiremons] first Ultra Space wormhole in ${Math.round(data.getInt(WORMHOLE_WAIT_KEY) / 1200)} min of Stage 6+ play`)
  }
  let left = data.getInt(WORMHOLE_WAIT_KEY) - WORMHOLE_CHECK_TICKS
  if (left > 0) {
    data.putInt(WORMHOLE_WAIT_KEY, left)
    return 'waiting'
  }
  let player = eligible[Math.floor(Math.random() * eligible.length)]
  if (!$UbWormhole.forceSpawnToPlayer(overworld, player, null)) {
    data.putInt(WORMHOLE_WAIT_KEY, 0) // try again next check
    return 'failed'
  }
  data.putInt(WORMHOLE_WAIT_KEY, nextWormholeWait())
  console.info(`[campfiremons] Ultra Space wormhole opened next to ${player.username}; the next in ${Math.round(data.getInt(WORMHOLE_WAIT_KEY) / 1200)} min of Stage 6+ play`)
  return 'opened'
}

ServerEvents.tick(event => {
  let server = event.server
  if (server.tickCount % WORMHOLE_CHECK_TICKS != 0) return
  let eligible = []
  server.getPlayerList().getPlayers().forEach(p => {
    if (String(p.level.dimension) == 'minecraft:overworld' && wormholeEligible(p)) eligible.push(p)
  })
  if (eligible.length > 0) ultraWormholeStep(server, eligible)
})

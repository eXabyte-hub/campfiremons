// Ultra Space (Cobblemon Ultra-Beasts) is Stage 6+ (DESIGN.md §3.4), the stage that unlocks Ultra Beasts. A wormhole
// can open near any player, so one below that stage who steps through is dropped below the mod's void limit: its own
// void-fall return then sends them home, tears the structure down and frees Ultra Space for the next wormhole.
// (Cancelling the teleport instead would leave the mod's claim on Ultra Space dangling.)

const ULTRA_SPACE = 'cobblemon_ultrabeast:ultra_space'
const BELOW_VOID_LIMIT_Y = -110 // Ultra Space's floor is y -64; damage is cancelled in that dimension

PlayerEvents.tick(event => {
  let player = event.player
  if (player.tickCount % 20 !== 0) return
  if (String(player.level.dimension) !== ULTRA_SPACE) return // KubeJS gives the dimension id, not a ResourceKey
  let helpers = global.campfiremons
  let stage = global.campfiremonsConfig.tiers.beast_paradox.stage
  if (helpers.isBypassed(player) || helpers.playerStage(player) >= stage) return
  helpers.deny(player, Text.red(`Ultra Space rejects you: Ultra Beasts unlock at Stage ${stage}.`))
  player.teleportTo(player.x, BELOW_VOID_LIMIT_Y, player.z)
})

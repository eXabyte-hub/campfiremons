// Bug types in a pasture pollinate (asked for on 2026-11-27): crops, berries and apricorns within POLLINATE_RADIUS blocks
// of a Pasture Block holding a Bug-type Pokémon grow about twice as fast. Cobbleworkers jobs can only set a block property
// to a fixed value (no "one growth step", no bone meal), so this is a script rather than a job file; Bug types keep their
// Cobbleworkers job (Apricorn Pickers) as well.
// Every POLLINATE_TICKS, each such pasture gives every plant in range a chance of one extra random tick. Vanilla random-ticks
// a block randomTickSpeed / 4096 times a game tick (about once a minute at the default 3), so a chance of
// POLLINATE_TICKS * randomTickSpeed / 4096 doubles that; wet farmland and light still matter as usual. More Bug types, or
// overlapping pastures, don't add more. Like vanilla random ticks, it only happens with a player within 128 blocks.

const $PolTagKey = Java.loadClass('net.minecraft.tags.TagKey')
const $PolRegistries = Java.loadClass('net.minecraft.core.registries.Registries')
const $PolRL = Java.loadClass('net.minecraft.resources.ResourceLocation')
const $PolBlockPos = Java.loadClass('net.minecraft.core.BlockPos')
const $PolGameRules = Java.loadClass('net.minecraft.world.level.GameRules')
const $PolParticles = Java.loadClass('net.minecraft.core.particles.ParticleTypes')
const $PolElementalTypes = Java.loadClass('com.cobblemon.mod.common.api.types.ElementalTypes')

const POLLINATE_TICKS = 400 // 20 s
const POLLINATE_RADIUS = 8 // blocks around the pasture, as Cobbleworkers' own jobs search (areaScanRadius)
const POLLINATE_HEIGHT = 2 // blocks above and below the pasture
const POLLINATE_TAGS = ['cobbleworkers:crops', 'cobblemon:crops', 'cobblemon:berries', 'cobblemon:apricorns']
  .map(id => $PolTagKey.create($PolRegistries.BLOCK, $PolRL.parse(id)))

function isPollinator(entity) {
  if (String(entity.type) != 'cobblemon:pokemon' || !entity.getTethering()) return false
  let pokemon = entity.getPokemon() // type names are capitalised ("Bug"), so compare with Cobblemon's own type
  return pokemon.getPrimaryType() == $PolElementalTypes.BUG || pokemon.getSecondaryType() == $PolElementalTypes.BUG
}

// Vanilla only random-ticks chunks with a (non-spectator) player within 128 blocks.
function pollinatorPlayerNear(level, pos) {
  let near = false
  level.getServer().getPlayerList().getPlayers().forEach(player => {
    if (near || player.level != level || player.isSpectator()) return
    let dx = player.x - pos.x, dz = player.z - pos.z
    if (dx * dx + dz * dz <= 128 * 128) near = true
  })
  return near
}

// One round for this level; returns how many pastures pollinated and how many plants grew.
function pollinate(level) {
  let pastures = {}
  level.getEntities().forEach(entity => {
    if (!isPollinator(entity)) return
    let pos = entity.getTethering().getPasturePos()
    if (pollinatorPlayerNear(level, pos)) pastures[pos.x + ',' + pos.y + ',' + pos.z] = pos
  })
  let keys = Object.keys(pastures)
  if (keys.length == 0) return { pastures: 0, grew: 0 }
  let chance = Math.min(1, POLLINATE_TICKS * level.getGameRules().getInt($PolGameRules.RULE_RANDOMTICKING) / 4096)
  let random = level.getRandom()
  let done = {}, grew = 0
  keys.forEach(key => {
    let centre = pastures[key]
    for (let dx = -POLLINATE_RADIUS; dx <= POLLINATE_RADIUS; dx++) {
      for (let dz = -POLLINATE_RADIUS; dz <= POLLINATE_RADIUS; dz++) {
        for (let dy = -POLLINATE_HEIGHT; dy <= POLLINATE_HEIGHT; dy++) {
          let pos = new $PolBlockPos(centre.x + dx, centre.y + dy, centre.z + dz)
          let id = pos.x + ',' + pos.y + ',' + pos.z
          if (done[id]) continue
          let state = level.getBlockState(pos)
          if (!state.isRandomlyTicking() || !POLLINATE_TAGS.some(tag => state['is(net.minecraft.tags.TagKey)'](tag))) continue
          done[id] = true
          if (Math.random() >= chance) continue
          state.randomTick(level, pos, random)
          if (level.getBlockState(pos) != state) {
            grew++
            level.sendParticles($PolParticles.HAPPY_VILLAGER, pos.x + 0.5, pos.y + 0.5, pos.z + 0.5, 3, 0.3, 0.3, 0.3, 0)
          }
        }
      }
    }
  })
  return { pastures: keys.length, grew: grew }
}

ServerEvents.tick(event => {
  let server = event.server
  if (server.tickCount % POLLINATE_TICKS != 0) return
  server.getAllLevels().forEach(level => pollinate(level))
})

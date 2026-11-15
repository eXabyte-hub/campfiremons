// Gym maps (DESIGN.md §3.1): directions to your next gym, so nobody wanders for kilometres looking for one.
// Given on first login, after every stage-up, and on demand with /gymmap. Overworld gyms come as an explorer map
// (loot table campfiremons:gym_map/<id>, the game's own map code) plus distance and direction in chat; gyms in the
// Nether or the End get chat directions once you're in that dimension. The gyms are on their own structure grids
// (tools/gen_structure_spacing.py), so finding one doesn't stall the server. Gym list: config.js `nextGym`.

const $TagKey = Java.loadClass('net.minecraft.tags.TagKey')
const $Registries = Java.loadClass('net.minecraft.core.registries.Registries')
const $ResourceLocation = Java.loadClass('net.minecraft.resources.ResourceLocation')

const GYM_SEARCH_RADIUS = 100 // structure grid cells (about 60 chunks each for the gyms)
const GYM_MAP_COOLDOWN_MS = 30 * 1000
const DIRECTIONS = ['north', 'north-east', 'east', 'south-east', 'south', 'south-west', 'west', 'north-west']

function gymTag(id) {
  return $TagKey.create($Registries.STRUCTURE, $ResourceLocation.parse(`campfiremons:gym/${id}`))
}

function describeOffset(dx, dz) {
  let blocks = String(Math.round(Math.sqrt(dx * dx + dz * dz) / 10) * 10).replace(/\B(?=(\d{3})+(?!\d))/g, ',')
  let angle = (Math.atan2(dx, -dz) * 180 / Math.PI + 360) % 360
  return { blocks: blocks, direction: DIRECTIONS[Math.round(angle / 45) % 8] }
}

// Tells the player where their next gym is; gives the explorer map when `withMap` and the gym is in this dimension
function giveGymDirections(player, withMap) {
  let gyms = global.campfiremonsConfig.nextGym
  let stage = global.campfiremons.playerStage(player)
  if (stage >= gyms.length) {
    player.tell(Text.gold("You're the Champion: there are no gyms left to find."))
    return
  }
  let gym = gyms[stage]
  let dimension = gym.dimension || 'minecraft:overworld'
  let level = player.level
  if (String(level.dimension).indexOf(dimension) < 0) {
    player.tell(Text.gold(`Next: ${gym.leader} at ${gym.place}, in ${gym.where}. Use /gymmap there for directions.`))
    return
  }
  let found = level.findNearestMapStructure(gymTag(gym.id), player.blockPosition(), GYM_SEARCH_RADIUS, false)
  if (!found) {
    player.tell(Text.red(`No ${gym.place} found within range. Ask an admin to check the world.`))
    return
  }
  let offset = describeOffset(found.x - player.x, found.z - player.z)
  player.tell(Text.gold(`Next: ${gym.leader} at ${gym.place}, about ${offset.blocks} blocks ` +
    `${offset.direction} (x ${found.x}, z ${found.z}).`))
  if (withMap && dimension === 'minecraft:overworld') {
    player.server.runCommandSilent(`execute as ${player.username} at @s run loot give @s loot campfiremons:gym_map/${gym.id}`)
  }
}

// First login: directions to Brock
PlayerEvents.loggedIn(event => {
  let player = event.player
  if (player.persistentData.getBoolean('campfiremonsFirstGymMap')) return
  player.persistentData.putBoolean('campfiremonsFirstGymMap', true)
  player.server.scheduleInTicks(100, () => giveGymDirections(player, true))
})

// Every stage-up: directions to the next gym, once the battle has wrapped up
PlayerEvents.advancement(event => {
  let advancement = event.advancement
  let id = String(typeof advancement.id === 'function' ? advancement.id() : advancement.id)
  if (!/^campfiremons:stage\/\d+$/.test(id)) return // not the tree's root, which everyone gets on their first tick
  let player = event.player
  player.server.scheduleInTicks(100, () => giveGymDirections(player, true))
})

// /gymmap: a fresh map, at most every 30 seconds
ServerEvents.commandRegistry(event => {
  let Commands = event.commands
  event.register(Commands.literal('gymmap').executes(ctx => {
    let player = ctx.source.playerOrException
    let now = Date.now()
    let last = player.persistentData.getLong('campfiremonsGymMapAt')
    if (now - last < GYM_MAP_COOLDOWN_MS) {
      player.tell(Text.red('You just got one. Try again in a few seconds.'))
      return 0
    }
    player.persistentData.putLong('campfiremonsGymMapAt', now)
    giveGymDirections(player, true)
    return 1
  }))
})

// Spawn town (DESIGN.md §3.1): a new world's spawn moves to the nearest Pallet Town (CobbleTowns), so every player
// starts, and respawns without a bed, in Pallet. Runs once per world, on its first load; a world that has already been
// played (older than SPAWN_TOWN_MAX_AGE ticks when this first runs) keeps its spawn. The town is whatever the
// structure tag campfiremons:spawn_town lists; if none is found, the vanilla spawn stays.

const $SpawnTagKey = Java.loadClass('net.minecraft.tags.TagKey')
const $SpawnRegistries = Java.loadClass('net.minecraft.core.registries.Registries')
const $SpawnResourceLocation = Java.loadClass('net.minecraft.resources.ResourceLocation')
const $SpawnBlockPos = Java.loadClass('net.minecraft.core.BlockPos')
const $SpawnHeightmapTypes = Java.loadClass('net.minecraft.world.level.levelgen.Heightmap$Types')

const SPAWN_TOWN_TAG = 'campfiremons:spawn_town'
const SPAWN_TOWN_MAX_AGE = 1200 // ticks: a world younger than a minute counts as new
const SPAWN_TOWN_SEARCH_RADIUS = 100 // shared-grid cells (20 chunks each)

ServerEvents.loaded(event => {
  let server = event.server
  let data = server.persistentData
  if (data.getBoolean('campfiremonsSpawnTownChecked')) return
  data.putBoolean('campfiremonsSpawnTownChecked', true)

  let level = server.overworld()
  if (level.getLevelData().getGameTime() > SPAWN_TOWN_MAX_AGE) {  // KubeJS hides Level.getGameTime()
    console.info('[campfiremons] spawn town: existing world, spawn left where it is')
    return
  }
  let old = level.sharedSpawnPos
  let tag = $SpawnTagKey.create($SpawnRegistries.STRUCTURE, $SpawnResourceLocation.parse(SPAWN_TOWN_TAG))
  let found = level.findNearestMapStructure(tag, old, SPAWN_TOWN_SEARCH_RADIUS, false)
  if (!found) {
    console.warn('[campfiremons] spawn town: none found, keeping the vanilla spawn')
    return
  }

  // The locate position is the town's starting chunk; spawn in the middle of the town's actual bounds
  let structures = server.registryAccess().registryOrThrow($SpawnRegistries.STRUCTURE)
  let chunk = level.getChunk(found.x >> 4, found.z >> 4)
  let center = null
  structures.getTag(tag).ifPresent(set => set.forEach(holder => {
    let start = chunk.getStartForStructure(holder.value())
    if (!center && start && start.isValid()) center = start.boundingBox.center
  }))
  let x = center ? center.x : found.x
  let z = center ? center.z : found.z
  level.getChunk(x >> 4, z >> 4)
  let spawn = new $SpawnBlockPos(x, level.getHeight($SpawnHeightmapTypes.MOTION_BLOCKING_NO_LEAVES, x, z), z)
  level.setDefaultSpawnPos(spawn, 0)
  let moved = Math.round(Math.sqrt(Math.pow(x - old.x, 2) + Math.pow(z - old.z, 2)))
  console.info(`[campfiremons] spawn town: world spawn moved ${moved} blocks to ${spawn.x} ${spawn.y} ${spawn.z}`)
})

// Kanto city gym leaders (DESIGN.md §5, Cobblemon Cities & Structures). CCS stands its own NPC leader in each city
// gym, but badges come from Radical Cobblemon Trainers, and an RCT battle only starts from RCT's own trainer. So when
// a CCS leader NPC loads (a newly generated city, or an older one that still has it), it's swapped for that leader's
// RCT trainer: same spot, same facing, persistent, and held in place with Slowness as Radical Gyms does. One leader
// per gym, and talking to them starts the RCT challenge. Leader list: config.js `ccsLeaders`.

const $CcsLeaderAABB = Java.loadClass('net.minecraft.world.phys.AABB')
const CCS_LEADER_TAG = 'campfiremons_ccs_leader' // on the RCT trainers placed here

EntityEvents.spawned('cobblemon:npc', event => {
  let npc = event.entity
  let nbt = npc.nbt
  let id = nbt ? String(nbt.getString('ForcedResourceIdentifier')) : ''
  let trainer = global.campfiremonsConfig.ccsLeaders[id]
  if (!trainer) return
  let yaw = nbt.getList('Rotation', 5).getFloat(0) // Rhino hides getYRot()
  // Entities are joining the world mid chunk load: swap once the gym's chunks are running
  let level = event.level
  level.server.scheduleInTicks(20, () => swapCcsLeader(level, npc, id, trainer, yaw, 0, false))
})

// Persistent RCT trainers with this id within `range` blocks of the NPC, tagged as a placed leader or not
function ccsLeaderTrainers(level, npc, trainer, range, tagged) {
  let box = new $CcsLeaderAABB(npc.x - range, npc.y - range, npc.z - range, npc.x + range, npc.y + range, npc.z + range)
  let found = []
  level.getEntities(npc, box).forEach(e => {
    if (String(e.type) != 'rctmod:trainer' || !e.isPersistenceRequired()) return
    if (String(e.getTrainerId()) == trainer && e.getTags().contains(CCS_LEADER_TAG) == tagged) found.push(e)
  })
  return found
}

const CCS_LEADER_RETRIES = 15 // one second apart

function swapCcsLeader(level, npc, id, trainer, yaw, attempt, summoned) {
  if (!npc.isAlive() || !level.isLoaded(npc.blockPosition())) return // left for the next time the gym loads
  let server = level.server
  let retry = () => {
    if (attempt < CCS_LEADER_RETRIES) {
      server.scheduleInTicks(20, () => swapCcsLeader(level, npc, id, trainer, yaw, attempt + 1, summoned))
    } else {
      console.warn(`[campfiremons] CCS leader ${id}: couldn't place ${trainer}, keeping the CCS NPC`)
    }
  }
  // Until its chunk is running, a new trainer exists but no entity search can see it yet
  if (!level.isPositionEntityTicking(npc.blockPosition())) return retry()
  let key = level.dimension // KubeJS exposes it as a property (ResourceLocation); vanilla's is a ResourceKey
  let dimension = String(key.location ? key.location() : key)
  let at = `execute in ${dimension} positioned ${npc.x} ${npc.y} ${npc.z}`
  if (ccsLeaderTrainers(level, npc, trainer, 3, true).length == 0) {
    // RCT moves a summoned trainer to a spot it likes (sometimes 30 blocks off), so find it wherever it landed
    let placed = ccsLeaderTrainers(level, npc, trainer, 48, false)
    if (placed.length == 0 && !summoned) {
      let pos = npc.blockPosition()
      server.runCommandSilent(`${at} run rctmod trainer summon_persistent ${trainer} ${pos.x} ${pos.y} ${pos.z}`)
      summoned = true
      placed = ccsLeaderTrainers(level, npc, trainer, 48, false)
    }
    if (placed.length == 0) return retry()
    placed[0].addTag(CCS_LEADER_TAG) // RCT keeps persistence its own way, so only a tag lets a selector find it
    let leader = `@e[type=rctmod:trainer,tag=${CCS_LEADER_TAG},distance=..48,limit=1,sort=nearest]`
    server.runCommandSilent(`${at} run tp ${leader} ${npc.x} ${npc.y} ${npc.z} ${yaw} 0`)
    server.runCommandSilent(`${at} run effect give ${leader} minecraft:slowness infinite 100 true`)
  }
  npc.discard()
  console.info(`[campfiremons] CCS leader ${id} swapped for RCT ${trainer} at ${Math.round(npc.x)} ${Math.round(npc.y)} ${Math.round(npc.z)}`)
}

// Kanto city gym leaders (DESIGN.md §5, Cobblemon Cities & Structures). CCS stands its own NPC leader in each city
// gym, but badges come from Radical Cobblemon Trainers, and an RCT battle only starts from RCT's own trainer. So when
// a CCS leader NPC loads (a newly generated city, or an older one that still has it), it's swapped for that leader's
// RCT trainer: same spot, same facing, persistent, and held in place with Slowness as Radical Gyms does. One leader
// per gym, and talking to them starts the RCT challenge. Leader list: config.js `ccsLeaders`.
//
// v0.1.19 rework (players found two leaders in a gym, or none): entities load out to view-distance (10 on the server)
// but only run within simulation-distance (8), and the swap used to give up after 15 s of waiting for the gym to run,
// leaving CCS's own leader in place, often next to an RCT one from an earlier attempt. Now it waits for as long as
// the NPC stays loaded, freezes the NPC meanwhile so it can't wander off its spot, summons the leader already tagged,
// and keeps exactly one tagged leader per gym, removing any extras whenever a gym loads.

const $CcsLeaderAABB = Java.loadClass('net.minecraft.world.phys.AABB')
const $CcsLeaderEffects = Java.loadClass('net.minecraft.world.effect.MobEffects')
const CCS_LEADER_TAG = 'campfiremons_ccs_leader' // on the RCT trainers placed here
const CCS_LEADER_MOVING = 'campfiremons_ccs_leader_moving' // briefly, on the one leader a tp should move
const CCS_GYM_RADIUS = 32 // a gym's leaders are within this many blocks of where CCS put its NPC
const CCS_WAIT_TICKS = 40

EntityEvents.spawned('cobblemon:npc', event => {
  let npc = event.entity
  let nbt = npc.nbt
  let id = nbt ? String(nbt.getString('ForcedResourceIdentifier')) : ''
  let trainer = global.campfiremonsConfig.ccsLeaders[id]
  if (!trainer) return
  let yaw = nbt.getList('Rotation', 5).getFloat(0) // Rhino hides getYRot()
  try {
    npc.setNoAi(true) // stand still on CCS's spot until swapped (it's discarded after)
  } catch (e) {
    console.warn(`[campfiremons] CCS leader ${id}: couldn't freeze the NPC: ${e}`)
  }
  let level = event.level
  level.server.scheduleInTicks(20, () => swapCcsLeader(level, npc, id, trainer, yaw))
})

// A placed leader loading (its gym came back into range): if an earlier swap left two, keep one
EntityEvents.spawned('rctmod:trainer', event => {
  let leader = event.entity
  if (!leader.getTags().contains(CCS_LEADER_TAG)) return
  let level = event.level
  level.server.scheduleInTicks(20, () => dedupeCcsLeaders(level, leader))
})

function ccsBox(at, range) {
  return new $CcsLeaderAABB(at.x - range, at.y - range, at.z - range, at.x + range, at.y + range, at.z + range)
}

// Persistent RCT trainers with this id within CCS_GYM_RADIUS of `at`, tagged as a placed leader or not
function ccsLeaderTrainers(level, at, trainer, tagged) {
  let found = []
  level.getEntities(null, ccsBox(at, CCS_GYM_RADIUS)).forEach(e => {
    if (String(e.type) != 'rctmod:trainer' || !e.isAlive() || !e.isPersistenceRequired()) return
    if (String(e.getTrainerId()) == trainer && e.getTags().contains(CCS_LEADER_TAG) == tagged) found.push(e)
  })
  // nearest first; ties (two on one spot) by entity id, so every caller keeps the same one
  found.sort((a, b) => (a.distanceToSqr(at.x, at.y, at.z) - b.distanceToSqr(at.x, at.y, at.z)) || (a.getId() - b.getId()))
  return found
}

function removeExtraCcsLeaders(extras, trainer, at) {
  extras.forEach(e => e.discard()) // RCT's remove() unregisters it (persistent record and chunk ticket)
  if (extras.length > 0) {
    console.info(`[campfiremons] CCS gym at ${Math.round(at.x)} ${Math.round(at.y)} ${Math.round(at.z)}: removed ${extras.length} extra ${trainer}`)
  }
}

function swapCcsLeader(level, npc, id, trainer, yaw) {
  if (!npc.isAlive() || !level.isLoaded(npc.blockPosition())) return // unloaded: its next load starts over
  let server = level.server
  // Loaded but not running yet (between simulation and view distance): a new trainer would be invisible to entity
  // searches, so wait, for as long as the gym stays loaded
  if (!level.isPositionEntityTicking(npc.blockPosition())) {
    server.scheduleInTicks(CCS_WAIT_TICKS, () => swapCcsLeader(level, npc, id, trainer, yaw))
    return
  }
  let key = level.dimension // KubeJS exposes it as a property (ResourceLocation); vanilla's is a ResourceKey
  let at = `execute in ${String(key.location ? key.location() : key)} positioned ${npc.x} ${npc.y} ${npc.z}`
  let leaders = ccsLeaderTrainers(level, npc, trainer, true)
  if (leaders.length == 0) {
    // A persistent trainer of this leader that an older version summoned but never tagged
    let strays = ccsLeaderTrainers(level, npc, trainer, false)
    if (strays.length > 0) {
      strays[0].addTag(CCS_LEADER_TAG)
      leaders = [strays[0]]
    }
  }
  if (leaders.length == 0) {
    let pos = npc.blockPosition()
    server.runCommandSilent(`${at} run rctmod trainer summon_persistent ${trainer} ${pos.x} ${pos.y} ${pos.z} {Tags:["${CCS_LEADER_TAG}"]}`)
    leaders = ccsLeaderTrainers(level, npc, trainer, true)
  }
  if (leaders.length == 0) {
    console.warn(`[campfiremons] CCS leader ${id}: summoning ${trainer} at ${Math.round(npc.x)} ${Math.round(npc.y)} ${Math.round(npc.z)} failed, trying again in 10 s`)
    server.scheduleInTicks(200, () => swapCcsLeader(level, npc, id, trainer, yaw))
    return
  }
  // Extras: more tagged leaders, and untagged ones an older version summoned on a failed swap
  removeExtraCcsLeaders(leaders.slice(1).concat(ccsLeaderTrainers(level, npc, trainer, false)), trainer, npc)
  let leader = leaders[0]
  leader.addTag(CCS_LEADER_MOVING) // a selector for this one trainer; removed straight after
  let it = `@e[type=rctmod:trainer,tag=${CCS_LEADER_MOVING},limit=1]`
  server.runCommandSilent(`${at} run tp ${it} ${npc.x} ${npc.y} ${npc.z} ${yaw} 0`)
  server.runCommandSilent(`${at} run effect give ${it} minecraft:slowness infinite 100 true`)
  leader.removeTag(CCS_LEADER_MOVING)
  npc.discard()
  console.info(`[campfiremons] CCS leader ${id} swapped for RCT ${trainer} at ${Math.round(npc.x)} ${Math.round(npc.y)} ${Math.round(npc.z)}`)
}

function dedupeCcsLeaders(level, leader) {
  if (!leader.isAlive() || !level.isLoaded(leader.blockPosition())) return
  if (!level.isPositionEntityTicking(leader.blockPosition())) {
    level.server.scheduleInTicks(CCS_WAIT_TICKS, () => dedupeCcsLeaders(level, leader))
    return
  }
  let trainer = String(leader.getTrainerId())
  // Without the NPC there's no gym spot to measure from: keep a leader that was put in place (it has the Slowness
  // hold), lowest entity id among those, so every duplicate's own check picks the same one
  let placed = e => e.hasEffect($CcsLeaderEffects.MOVEMENT_SLOWDOWN) ? 0 : 1
  let leaders = ccsLeaderTrainers(level, leader, trainer, true).sort((a, b) => (placed(a) - placed(b)) || (a.getId() - b.getId()))
  removeExtraCcsLeaders(leaders.slice(1).concat(ccsLeaderTrainers(level, leader, trainer, false)), trainer, leader)
}

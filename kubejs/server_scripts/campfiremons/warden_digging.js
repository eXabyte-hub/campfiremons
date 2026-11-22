// Wardens dig back down once no player has been near them for a minute (asked for on 2026-11-22).
// Vanilla wardens dig down after 60 s without a disturbance, but every footstep of a wild Pokémon in the deep dark is
// a vibration, so they kept getting disturbed and never left. Here only players count: a warden with no player
// (spectators aside) within WARDEN_PLAYER_RANGE blocks for WARDEN_IDLE_TICKS plays the vanilla dig animation and
// sound and is removed when it ends, as vanilla's own dig does. Named wardens are left alone. The time a player was
// last near is kept on the warden, so one that sat in an unloaded chunk digs soon after its chunk loads again, unless
// a player is close.

const $WardenPose = Java.loadClass('net.minecraft.world.entity.Pose')
const $WardenEntityType = Java.loadClass('net.minecraft.world.entity.EntityType')
const $WardenSounds = Java.loadClass('net.minecraft.sounds.SoundEvents')

const WARDEN_CHECK_TICKS = 100
const WARDEN_PLAYER_RANGE = 32
const WARDEN_IDLE_TICKS = 1200
const WARDEN_DIG_TICKS = 100 // vanilla's dig takes 5 s
const WARDEN_SEEN_KEY = 'campfiremonsPlayerNear'
const WARDEN_DIG_KEY = 'campfiremonsDigStart'

// The world's game time (saved, so it carries over restarts). KubeJS doesn't expose Level.getGameTime() itself.
function wardenGameTime(level) {
  return level.getLevelData().getGameTime()
}

ServerEvents.tick(event => {
  let server = event.server
  if (wardenGameTime(server.overworld()) % WARDEN_CHECK_TICKS != 0) return
  server.getAllLevels().forEach(level => {
    let wardens = level.getEntities($WardenEntityType.WARDEN, w => w.isAlive())
    if (wardens.isEmpty()) return
    let time = wardenGameTime(level)
    wardens.forEach(warden => checkWarden(server, level, warden, time))
  })
})

function checkWarden(server, level, warden, time) {
  if (warden.hasCustomName()) return
  let data = warden.persistentData
  if (data.contains(WARDEN_DIG_KEY)) {
    // Ours is digging; the scheduled removal is lost if the server stopped meanwhile
    if (time - data.getLong(WARDEN_DIG_KEY) >= WARDEN_DIG_TICKS) warden.discard()
    return
  }
  if (warden.getPose() == $WardenPose.DIGGING || warden.getPose() == $WardenPose.EMERGING) return
  if (level.getNearestPlayer(warden, WARDEN_PLAYER_RANGE) != null || !data.contains(WARDEN_SEEN_KEY)) {
    data.putLong(WARDEN_SEEN_KEY, time)
    return
  }
  if (time - data.getLong(WARDEN_SEEN_KEY) < WARDEN_IDLE_TICKS || !warden.onGround()) return
  // Vanilla's Digging behaviour: digging pose and sound, removed when the animation ends. No AI meanwhile, so
  // nothing (a roar, a sniff) changes the pose back.
  warden.setNoAi(true)
  warden.getNavigation().stop()
  warden.setPose($WardenPose.DIGGING)
  warden.playSound($WardenSounds.WARDEN_DIG, 5.0, 1.0)
  data.putLong(WARDEN_DIG_KEY, time)
  server.scheduleInTicks(WARDEN_DIG_TICKS, () => {
    if (warden.isAlive()) warden.discard()
  })
}

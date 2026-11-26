// No phantoms (asked for on 2026-11-26). Vanilla spawns them over players who haven't slept for three in-game days;
// turning the doInsomnia game rule off stops those spawn attempts in every world the pack runs (the server and
// single-player). Any phantom from another source (spawn eggs, other mods) is cancelled by removed_mobs.js, which has
// minecraft:phantom in config.js `removedMobs`.

const $PhantomGameRules = Java.loadClass('net.minecraft.world.level.GameRules')

ServerEvents.loaded(event => {
  let rule = event.server.getGameRules().getRule($PhantomGameRules.RULE_DOINSOMNIA)
  if (rule.get()) {
    rule.set(false, event.server)
    console.info('[campfiremons] doInsomnia turned off: no phantoms')
  }
})

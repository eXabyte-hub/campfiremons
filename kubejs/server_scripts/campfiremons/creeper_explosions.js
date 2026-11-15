// Creeper explosions don't break blocks (asked for on 2026-11-15). They still go off, hurt and knock back whoever is
// close, so creepers stay a threat; only the terrain is spared. This is narrower than the mobGriefing gamerule, which
// would also stop villagers farming, Endermen carrying blocks and other mods' mobs. TNT, beds in the Nether, End
// crystals and other explosions still break blocks.

LevelEvents.afterExplosion(event => {
  let exploder = event.exploder
  if (exploder && String(exploder.getEncodeId()) === 'minecraft:creeper') event.removeAllAffectedBlocks()
})

// Removed vanilla animals (DESIGN.md §4.8, list in config.js `removedMobs`). Natural spawns are already stopped by the
// biome modifier in data/campfiremons/neoforge/biome_modifier/; this catches the rest: animals placed by structures
// (village pens, village cats), wandering traders' llamas, spawn eggs and breeding.

let removedMobs = global.campfiremonsConfig.removedMobs
removedMobs.forEach(id => {
  EntityEvents.spawned(id, event => event.cancel())
})

console.info(`[campfiremons] removed mobs filter loaded (${removedMobs.length} types)`)

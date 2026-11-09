// Use-locks (DESIGN.md §4.3): balls and Bottle Caps can be crafted (and automated) freely, but throwing a ball or
// using a cap above your stage is refused and the item isn't used up. The list is config.js `itemLocks`; stage and
// message helpers come from startup_scripts/campfiremons/tier_locks.js.

const LOCKED_AT = {}
let itemLocks = global.campfiremonsConfig.itemLocks
Object.keys(itemLocks).forEach(stage => {
  itemLocks[stage].forEach(id => { LOCKED_AT[id] = parseInt(stage) })
})

function refuseIfLocked(event) {
  let player = event.entity
  let stage = LOCKED_AT[String(event.item.id)]
  let helpers = global.campfiremons
  if (helpers.isBypassed(player) || helpers.playerStage(player) >= stage) return
  helpers.deny(player, Text.red(event.item.hoverName.copy().append(` unlocks at Stage ${stage}.`)))
  event.cancel()
}

// Balls are thrown by using the item; caps are used in the air (party screen) or on a Pokémon
Object.keys(LOCKED_AT).forEach(id => {
  ItemEvents.rightClicked(id, refuseIfLocked)
  ItemEvents.entityInteracted(id, refuseIfLocked)
})

console.info(`[campfiremons] item locks loaded (${Object.keys(LOCKED_AT).length} items)`)

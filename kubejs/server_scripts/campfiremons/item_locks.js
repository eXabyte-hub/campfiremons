// Use-locks (DESIGN.md §4.3): balls, Bottle Caps, TMs and other items can be crafted (and automated) freely, but
// throwing or using one above your stage is refused and the item isn't used up. The lists are config.js
// `itemLocks` (by id) and `itemTagLocks` (by item tag); stage and message helpers come from
// startup_scripts/campfiremons/tier_locks.js.

const LOCKED_AT = {}
let itemLocks = global.campfiremonsConfig.itemLocks
Object.keys(itemLocks).forEach(stage => {
  itemLocks[stage].forEach(id => { LOCKED_AT[id] = parseInt(stage) })
})
const TAG_LOCKS = []
let itemTagLocks = global.campfiremonsConfig.itemTagLocks
Object.keys(itemTagLocks).forEach(stage => {
  itemTagLocks[stage].forEach(tag => TAG_LOCKS.push({ tag: tag, stage: parseInt(stage) }))
})

function lockedStage(item) {
  let stage = LOCKED_AT[String(item.id)]
  if (stage) return stage
  for (let i = 0; i < TAG_LOCKS.length; i++) {
    if (item.hasTag(TAG_LOCKS[i].tag)) return TAG_LOCKS[i].stage
  }
  return 0
}

// Refuses (and cancels) the event if the player is below the stage; name is what they tried to use
function refuseBelow(event, stage, name) {
  let player = event.entity
  let helpers = global.campfiremons
  if (helpers.isBypassed(player) || helpers.playerStage(player) >= stage) return
  helpers.deny(player, Text.red(name.copy().append(` unlocks at Stage ${stage}.`)))
  event.cancel()
}

function refuseIfLocked(event) {
  let stage = lockedStage(event.item)
  if (stage) refuseBelow(event, stage, event.item.hoverName)
}

// Balls are thrown by using the item; caps and TMs are used in the air (party screen) or on a Pokémon.
// Untargeted so item-tag locks work too; the checks above are a map lookup plus a few tag checks.
ItemEvents.rightClicked(refuseIfLocked)
ItemEvents.entityInteracted(refuseIfLocked)

// Blocks (config.js `blockLocks`), e.g. the Battle Tower
let blockLocks = global.campfiremonsConfig.blockLocks
let lockedBlocks = 0
Object.keys(blockLocks).forEach(stage => {
  blockLocks[stage].forEach(id => {
    BlockEvents.rightClicked(id, event => refuseBelow(event, parseInt(stage), event.block.block.name))
    lockedBlocks++
  })
})

console.info(`[campfiremons] use-locks loaded (${Object.keys(LOCKED_AT).length} items, ${TAG_LOCKS.length} tags, ${lockedBlocks} blocks)`)

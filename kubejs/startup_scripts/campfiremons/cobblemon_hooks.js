// Subscribes to Cobblemon's own event bus once at game start and forwards each event to a handler on
// global.campfiremons (set by tier_locks.js). Handlers are looked up per event, so `/kubejs reload startup`
// swaps in new logic without re-subscribing or restarting.

const $CobblemonEvents = Java.loadClass('com.cobblemon.mod.common.api.events.CobblemonEvents')
const $Priority = Java.loadClass('com.cobblemon.mod.common.api.Priority')

// subscribe(Priority, handler) is overloaded (Kotlin Function1 vs Java Consumer), which Rhino can't pick
// between for a JS function, so name the Consumer overload explicitly.
const SUBSCRIBE = 'subscribe(com.cobblemon.mod.common.api.Priority,java.util.function.Consumer)'

function forward(observable, handlerName) {
  observable[SUBSCRIBE]($Priority.LOWEST, event => {
    let handlers = global.campfiremons
    if (!handlers || !handlers[handlerName]) return
    try {
      handlers[handlerName](event)
    } catch (e) {
      // Never let a script error propagate into Cobblemon's ball/battle code
      console.error(`[campfiremons] ${handlerName} failed: ${e}`)
    }
  })
}

StartupEvents.postInit(event => {
  if (global.campfiremonsHooked) return // startup scripts can be reloaded; never subscribe twice
  forward($CobblemonEvents.THROWN_POKEBALL_HIT, 'onPokeballHit')
  forward($CobblemonEvents.BATTLE_STARTED_PRE, 'onBattleStartPre')
  global.campfiremonsHooked = true
  console.info('[campfiremons] Cobblemon event hooks registered')
})

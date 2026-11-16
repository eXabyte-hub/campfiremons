// Poké Balls come from vendors and Create, not the crafting table (asked for on 2026-11-16). The CobbleDollars shop
// sells every ball except the two guaranteed catches (tools/gen_shop.py), and Cobblemon Create Industries and Create:
// Klinks 'n' Klangs make every ball by sequenced assembly or a spout, so none goes missing. This removes the crafting
// recipes of everything in #cobblemon:poke_balls: Cobblemon's 47 and Legendary Monuments' Origin Ball (a guaranteed
// catch, the Champion's to give). Mechanical Crafters, the vanilla Crafter and crafting upgrades use the same recipes,
// so they can't make balls either. The Light, Smoke and Iron Balls are held items, not in the tag, and keep theirs.

ServerEvents.recipes(event => {
  event.remove({ output: '#cobblemon:poke_balls', type: 'minecraft:crafting_shaped' })
  event.remove({ output: '#cobblemon:poke_balls', type: 'minecraft:crafting_shapeless' })
})

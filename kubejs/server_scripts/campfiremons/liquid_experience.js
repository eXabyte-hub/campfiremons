// One liquid experience for Create (asked for on 2026-11-27). The pack has two real XP fluids: Create: Enchantment
// Industry's Liquid Experience (1 mB per XP point), which its Blaze Enchanter and Blaze Forger insist on, and
// Sophisticated Core's Experience (20 mB per point), which the backpack and storage XP Pump Upgrades make (Supplementaries'
// XP jars count as it too). They can't simply be made one fluid: Sophisticated's pump reads anything in #c:experience at
// 20 mB a point, so tagging Liquid Experience would turn 1 XP into 20. Enchantment Industry already reads Sophisticated's
// at the right rate (its Experience Hatch takes either); this mixes it into Liquid Experience at the same 20 to 1, unheated,
// so it can feed everything else. One way only, so a basin doesn't convert back and forth.

ServerEvents.recipes(event => {
  event.custom({
    type: 'create:mixing',
    ingredients: [{ type: 'fluid_stack', fluid: 'sophisticatedcore:xp_still', amount: 100 }],
    results: [{ id: 'create_enchantment_industry:experience', amount: 5 }]
  }).id('campfiremons:mixing/liquid_experience_from_sophisticated')
})

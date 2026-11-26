// One Medicinal Brew on Create (asked for on 2026-11-27). Create: Cobblemon Integrations and Create: Klinks 'n' Klangs
// both mix Medicinal Leeks into a Medicinal Brew fluid of their own, then mix that with berries into Cobblemon's
// medicines. This keeps Klinks 'n' Klangs' brew (heated mixer: a leek and 1000 mB of water make 1000 mB) and takes out
// Cobblemon Integrations' (no heat: a leek and 250 mB of water make 250 mB), its bottling, and the 12 mixes that only its
// brew feeds; Klinks 'n' Klangs makes every one of those medicines from its own brew. Cobblemon Integrations' bottle
// emptying and filling and its Max mixes stay: they work from emptied bottles, not from the brew.

const CCI_BREW_RECIPES = ['mixing/medicinal_brew', 'filling/medicinal_brew_bottle', 'mixing/antidote', 'mixing/awakening',
  'mixing/burn_heal', 'mixing/cobblemon_potion', 'mixing/elixir', 'mixing/ether', 'mixing/full_heal',
  'mixing/hyper_potion', 'mixing/ice_heal', 'mixing/paralyze_heal', 'mixing/pp_up', 'mixing/super_potion']

ServerEvents.recipes(event => {
  CCI_BREW_RECIPES.forEach(id => event.remove({ id: `createcobblemonintegrations:${id}` }))
})

// Summon items for four legendaries nothing else in the pack gives (asked for on 2026-11-28). Use one and the Pokémon
// appears in front of you as a wild Pokémon to battle and catch (server_scripts/campfiremons/legendary_summons.js,
// which also holds the recipes). They're registered here because items have to exist on both client and server.
//   Soul-Heart      -> Magearna   (Create mechanical crafting: a machine-made Pokémon for a tech pack)
//   Genesect Drive  -> Genesect   (Create mechanical crafting)
//   Poisoned Mochi  -> Pecharunt  (Create heated mixing from Potato Mochi; mochi is Pecharunt's own gimmick)
//   Beast Memory    -> Type: Null (Battle Tower BP shop; Silvally evolves from it)
// Textures reuse vanilla and Cobblemon item art.

StartupEvents.registry('item', event => {
  event.create('campfiremons:soul_heart').displayName('Soul-Heart').maxStackSize(1).rarity('epic')
    .texture('minecraft:item/heart_of_the_sea')
  event.create('campfiremons:genesect_drive').displayName('Genesect Drive').maxStackSize(1).rarity('epic')
    .texture('minecraft:item/recovery_compass_16')
  event.create('campfiremons:poisoned_mochi').displayName('Poisoned Mochi').maxStackSize(1).rarity('epic')
    .texture('cobblemon:item/food/potato_mochi')
  event.create('campfiremons:beast_memory').displayName('Beast Memory').maxStackSize(1).rarity('rare')
    .texture('minecraft:item/music_disc_11')
})

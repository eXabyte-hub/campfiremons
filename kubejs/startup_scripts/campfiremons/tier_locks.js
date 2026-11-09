// Legendary tier locks (DESIGN.md §4.1): a wild legendary/mythical/UB/paradox Pokémon can't be caught or
// battled until the player's stage unlocks its tier. Owned or traded ones are never checked ("trust the group").
// Events arrive via cobblemon_hooks.js. Edit, then `/kubejs reload startup` in game.

const $SoundEvents = Java.loadClass('net.minecraft.sounds.SoundEvents')
const $SoundSource = Java.loadClass('net.minecraft.sounds.SoundSource')
const $Cobblemon = Java.loadClass('com.cobblemon.mod.common.Cobblemon')

const STAGE_PREFIX = 'campfiremons:stage/'
const BYPASS = 'campfiremons:bypass'

function playerStage(player) {
  for (let n = global.campfiremonsConfig.maxStage; n >= 1; n--) {
    if (player.isAdvancementDone(STAGE_PREFIX + n)) return n
  }
  return 0
}

// Tier id for a species, or null if it isn't locked at all.
function tierOf(species) {
  let cfg = global.campfiremonsConfig
  let id = String(species.resourceIdentifier.path)
  if (id in cfg.overrides) return cfg.overrides[id]
  let labels = species.labels
  for (let i = 0; i < cfg.labelRules.length; i++) {
    if (labels.contains(cfg.labelRules[i].label)) return cfg.labelRules[i].tier
  }
  return null
}

function isBypassed(player) {
  return player.isAdvancementDone(BYPASS)
}

// The tier that stops this player from catching/battling this Pokémon, or null if they may.
function lockingTier(player, pokemon) {
  let tierId = tierOf(pokemon.species)
  if (!tierId) return null
  if (isBypassed(player)) return null
  let tier = global.campfiremonsConfig.tiers[tierId]
  return playerStage(player) >= tier.stage ? null : tier
}

function lockedMessage(pokemon, tier) {
  return Text.red(pokemon.species.translatedName.copy()
    .append(` is a ${tier.name} Pokémon. It unlocks at Stage ${tier.stage}.`))
}

// Held-item locks (config.js heldItemLocks): the first party Pokémon holding an item above its owner's stage.
function heldItemBlock(players) {
  let locks = global.campfiremonsConfig.heldItemLocks
  let lockedAt = {}
  Object.keys(locks).forEach(stage => locks[stage].forEach(id => { lockedAt[id] = parseInt(stage) }))

  let blocked = null
  players.forEach(player => {
    if (blocked || isBypassed(player)) return
    let stage = playerStage(player)
    $Cobblemon.INSTANCE.storage.getParty(player).forEach(pokemon => {
      let held = pokemon.heldItem()
      let need = lockedAt[String(held.id)]
      if (blocked || !need || stage >= need) return
      blocked = {
        player: player,
        message: Text.red(pokemon.species.translatedName.copy().append("'s ").append(held.hoverName)
          .append(` works from Stage ${need}. Take it off to battle.`)),
      }
    })
  })
  return blocked
}

function deny(player, message) {
  player.setStatusMessage(message)
  player.playNotifySound($SoundEvents.VILLAGER_NO, $SoundSource.PLAYERS, 1.0, 1.0)
}

global.campfiremons = global.campfiremons || {}

// Shared with server scripts (they can read `global` but not write it), e.g. item_locks.js
global.campfiremons.playerStage = playerStage
global.campfiremons.isBypassed = isBypassed
global.campfiremons.deny = deny

// A ball hitting a wild Pokémon. Cancelled hits drop the ball back as an item (Cobblemon behaviour).
// Battles against locked Pokémon are blocked at battle start, so this mainly covers overworld throws.
global.campfiremons.onPokeballHit = event => {
  if (event.isCanceled()) return
  let player = event.pokeBall.owner
  if (!player || !player.isPlayer()) return
  let pokemon = event.pokemon.pokemon
  if (!pokemon.isWild()) return
  let tier = lockingTier(player, pokemon)
  if (!tier) return
  event.cancel()
  deny(player, lockedMessage(pokemon, tier))
}

// Any battle with a wild Pokémon: every player in it must have that Pokémon's tier unlocked.
// Any battle at all: no player's party may hold a held-item-locked item above their stage.
global.campfiremons.onBattleStartPre = event => {
  if (event.isCanceled()) return
  let battle = event.battle
  let players = battle.players
  if (players.isEmpty()) return

  let blocked = null
  battle.actors.forEach(actor => {
    if (blocked || String(actor.type) !== 'WILD') return
    actor.pokemonList.forEach(battlePokemon => {
      let pokemon = battlePokemon.originalPokemon
      players.forEach(player => {
        if (blocked) return
        let tier = lockingTier(player, pokemon)
        if (tier) blocked = { player: player, message: lockedMessage(pokemon, tier) }
      })
    })
  })
  if (!blocked) blocked = heldItemBlock(players)
  if (!blocked) return

  event.cancel()
  event.reason = blocked.message // Cobblemon shows this to the battle's participants
  deny(blocked.player, blocked.message)
}

console.info('[campfiremons] tier locks loaded')

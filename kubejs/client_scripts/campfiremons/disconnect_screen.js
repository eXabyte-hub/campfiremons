// Keeps the "Failed to connect" / "Disconnected" screen usable when its message is huge.
//
// Microsoft's sign-in service sometimes answers a join with a whole error web page instead of JSON, and Minecraft
// shows that page's source as the reason. The text runs off the screen, the Back button with it, and this screen
// ignores Esc, so players had to restart the game (seen 2026-11-15 to 17). On that screen this script:
//   - swaps a web-page reason for a short explanation,
//   - cuts any other reason that wouldn't fit to a few lines,
//   - and re-centres the title, reason and buttons so the buttons are always on screen.
// Every other screen is left alone, and any error here leaves the vanilla screen as it was.

const $DisconnectedScreen = Java.loadClass('net.minecraft.client.gui.screens.DisconnectedScreen')
const $MultiLineTextWidget = Java.loadClass('net.minecraft.client.gui.components.MultiLineTextWidget')
const $AbstractButton = Java.loadClass('net.minecraft.client.gui.components.AbstractButton')
const $Component = Java.loadClass('net.minecraft.network.chat.Component')
const $ScreenInitPost = Java.loadClass('net.neoforged.neoforge.client.event.ScreenEvent$Init$Post')

const DISCONNECT_GAP = 12 // pixels between title, reason and buttons
const DISCONNECT_MAX_CHARS = 400 // longer non-web-page reasons are cut to this
const DISCONNECT_WEB_PAGE = 'Failed to log in: Microsoft\'s sign-in service sent back an error page instead of an ' +
  'answer. That\'s a hiccup on their side, not the server: wait a few seconds and join again. If it keeps happening, ' +
  'restart the game (in Prism: Accounts, then refresh your Microsoft account).'

function looksLikeWebPage(text) {
  let t = text.toLowerCase()
  return t.indexOf('<!doctype') >= 0 || t.indexOf('<html') >= 0 || t.indexOf('#errorref') >= 0 ||
    t.indexOf('</') >= 0 && t.indexOf('{') >= 0
}

NativeEvents.onEvent($ScreenInitPost, event => {
  try {
    let screen = event.getScreen()
    if (!(screen instanceof $DisconnectedScreen)) return
    let widgets = event.getListenersList()
    let stack = [] // the screen's widgets top to bottom, as vanilla lays them out
    let reason = null
    let lastButton = null
    for (let i = 0; i < widgets.size(); i++) {
      let w = widgets.get(i)
      if (!w.getHeight || !w.setY) continue
      stack.push(w)
      if (w instanceof $MultiLineTextWidget && reason === null) reason = w
      if (w instanceof $AbstractButton) lastButton = w
    }
    if (reason === null || lastButton === null) return

    let changed = false
    let text = String(reason.getMessage().getString())
    if (looksLikeWebPage(text)) {
      reason.setMessage($Component.literal(DISCONNECT_WEB_PAGE))
      changed = true
    } else if (lastButton.getY() + lastButton.getHeight() > screen.height || reason.getHeight() > screen.height / 2) {
      reason.setMessage($Component.literal(text.substring(0, DISCONNECT_MAX_CHARS) + '...'))
      changed = true
    }
    if (!changed && lastButton.getY() + lastButton.getHeight() <= screen.height) return

    let total = 0
    stack.forEach((w, i) => { total += w.getHeight() + (i > 0 ? DISCONNECT_GAP : 0) })
    let y = Math.max(4, Math.floor((screen.height - total) / 2))
    // On a very small window, start high enough that the last button still fits
    y = Math.min(y, Math.max(0, screen.height - 4 - total))
    stack.forEach(w => {
      w.setX(Math.floor((screen.width - w.getWidth()) / 2))
      w.setY(y)
      y += w.getHeight() + DISCONNECT_GAP
    })
  } catch (e) {
    console.warn('[campfiremons] disconnect screen fix failed: ' + e)
  }
})

#!/bin/sh
# Copy the local test datapacks (tools/testpacks/*, never shipped) into a dev-instance world.
# Copied, not symlinked: Minecraft rejects symlinked datapacks unless allowed_symlinks.txt lists them.
# Re-run after editing a pack. Usage: sh tools/install-testpack.sh ["<world folder name>"]  (default: newest world)
# Then in game: /datapack list, enable/disable with /datapack enable|disable "file/<pack>", and /reload.
set -eu
REPO="$(cd "$(dirname "$0")/.." && pwd)"
PRISM="${PRISM_DATA:-$HOME/.local/share/PrismLauncher}"
INSTANCE="${INSTANCE:-Campfiremons Dev}"
SAVES="$PRISM/instances/$INSTANCE/minecraft/saves"
WORLD="$SAVES/${1:-$(ls -t "$SAVES" | head -1)}"

[ -d "$WORLD" ] || { echo "No such world: $WORLD" >&2; exit 1; }
mkdir -p "$WORLD/datapacks"
for pack in "$REPO"/tools/testpacks/*/; do
    name="$(basename "$pack")"
    rm -rf "$WORLD/datapacks/$name"
    cp -r "$pack" "$WORLD/datapacks/$name"
    echo "Copied $name into $WORLD/datapacks/"
done

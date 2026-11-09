#!/bin/sh
# Copy the local test datapack (tools/testpacks/campfiremons-test, never shipped) into a dev-instance world.
# Copied, not symlinked: Minecraft rejects symlinked datapacks unless allowed_symlinks.txt lists them.
# Re-run after editing the pack. Usage: sh tools/install-testpack.sh "<world folder name>"
# Then in game: /datapack enable "file/campfiremons-test" (if not already listed as enabled) and /reload.
set -eu
REPO="$(cd "$(dirname "$0")/.." && pwd)"
PRISM="${PRISM_DATA:-$HOME/.local/share/PrismLauncher}"
INSTANCE="${INSTANCE:-Campfiremons Dev}"
WORLD="$PRISM/instances/$INSTANCE/minecraft/saves/${1:?world folder name required}"

[ -d "$WORLD" ] || { echo "No such world: $WORLD" >&2; exit 1; }
mkdir -p "$WORLD/datapacks"
rm -rf "$WORLD/datapacks/campfiremons-test"
cp -r "$REPO/tools/testpacks/campfiremons-test" "$WORLD/datapacks/campfiremons-test"
echo "Copied test pack into $WORLD/datapacks/"

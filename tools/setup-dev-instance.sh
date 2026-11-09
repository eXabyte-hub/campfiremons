#!/bin/sh
# Create the "Campfiremons Dev" Prism instance wired to this repo.
#  - mods/configs are synced from the repo by packwiz-installer on every launch (tools/dev-prelaunch.sh)
#  - kubejs/ and config/ftbquests/ are symlinks into the repo, so script edits and the in-game quest editor
#    write straight into git
set -eu
REPO="$(cd "$(dirname "$0")/.." && pwd)"
PRISM="${PRISM_DATA:-$HOME/.local/share/PrismLauncher}"
NAME="${1:-Campfiremons Dev}"
INST="$PRISM/instances/$NAME"
MC="$INST/minecraft"
NEOFORGE="$(sed -n 's/^neoforge = "\(.*\)"/\1/p' "$REPO/pack.toml")"
MINECRAFT="$(sed -n 's/^minecraft = "\(.*\)"/\1/p' "$REPO/pack.toml")"
BOOTSTRAP_URL=https://github.com/packwiz/packwiz-installer-bootstrap/releases/download/v0.0.3/packwiz-installer-bootstrap.jar
BOOTSTRAP_SHA256=a8fbb24dc604278e97f4688e82d3d91a318b98efc08d5dbfcbcbcab6443d116c

if [ -e "$INST" ]; then
    echo "Instance already exists: $INST (delete it in Prism first to recreate)" >&2
    exit 1
fi
mkdir -p "$MC/config"

cat > "$INST/instance.cfg" <<EOF
[General]
ConfigVersion=1.3
InstanceType=OneSix
name=$NAME
iconKey=default
OverrideCommands=true
PreLaunchCommand=sh "$REPO/tools/dev-prelaunch.sh"
notes=Dev instance for $REPO. Mods sync from the repo on every launch; kubejs/ and config/ftbquests/ are symlinks into it.
EOF

cat > "$INST/mmc-pack.json" <<EOF
{
    "components": [
        { "uid": "net.minecraft", "version": "$MINECRAFT", "important": true },
        { "uid": "net.neoforged", "version": "$NEOFORGE" }
    ],
    "formatVersion": 1
}
EOF

curl -sSL -o "$MC/packwiz-installer-bootstrap.jar" "$BOOTSTRAP_URL"
echo "$BOOTSTRAP_SHA256  $MC/packwiz-installer-bootstrap.jar" | sha256sum -c -

ln -s "$REPO/kubejs" "$MC/kubejs"
ln -s "$REPO/config/ftbquests" "$MC/config/ftbquests"

echo "Created $INST (Minecraft $MINECRAFT, NeoForge $NEOFORGE)"

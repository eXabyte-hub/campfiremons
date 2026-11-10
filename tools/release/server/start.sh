#!/bin/sh
# Campfiremons server start (shipped in the server starter zip, see README.md "Running the server").
# On every start it:
#   1. installs the NeoForge server, once per NeoForge version (checksum-verified),
#   2. syncs mods and configs from the pack's release branch (packwiz-installer, server-side files only),
#   3. starts the server.
# Startup command on the host: `sh start.sh`. MEMORY (default 10G) is the Java heap; keep it 1-2 GB below the
# plan's RAM. `sh start.sh --sync-only` stops after step 2, to prepare a folder for hosts without a custom startup.
set -eu
cd "$(dirname "$0")"

PACK_URL="${PACK_URL:-https://raw.githubusercontent.com/eXabyte-hub/campfiremons/release/pack.toml}"
MEMORY="${MEMORY:-10G}"
JAVA="${JAVA:-java}"
# Keep in step with pack.toml; tools/release/build.py refuses to build if they differ
NEOFORGE_VERSION=21.1.264
NEOFORGE_SHA256=d7c035dd5436a7c524dfbad6df191b0ef34179fd3edfee9dc99262af3b80239b

ARGS_FILE="libraries/net/neoforged/neoforge/$NEOFORGE_VERSION/unix_args.txt"
if [ ! -f "$ARGS_FILE" ]; then
    echo "[campfiremons] Installing the NeoForge $NEOFORGE_VERSION server"
    installer="neoforge-$NEOFORGE_VERSION-installer.jar"
    curl -fsSL -o "$installer" "https://maven.neoforged.net/releases/net/neoforged/neoforge/$NEOFORGE_VERSION/$installer"
    echo "$NEOFORGE_SHA256  $installer" | sha256sum -c -
    "$JAVA" -jar "$installer" --installServer
    rm -f "$installer" "$installer.log"
fi

echo "[campfiremons] Syncing the pack from $PACK_URL"
"$JAVA" -jar packwiz-installer-bootstrap.jar -g -s server "$PACK_URL"

if [ "${1:-}" = "--sync-only" ]; then
    exit 0
fi
exec "$JAVA" "-Xmx$MEMORY" @user_jvm_args.txt "@$ARGS_FILE" nogui

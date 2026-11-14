#!/bin/sh
# Campfiremons server start, for hosts that take a startup script and for VPSes (DEVELOPMENT.md "Running the server").
# It runs campfiremons-server.jar, the same jar a host without a startup script is set to start. On every start that
#   1. installs the NeoForge server, once per NeoForge version (checksum-verified),
#   2. syncs mods and configs from the pack's release branch (packwiz-installer, server-side files only),
#   3. starts the server in the same JVM.
# MEMORY (default 10G) is the Java heap; keep it 1-2 GB below the plan's RAM. `sh start.sh --sync-only` stops after
# step 2. PACK_URL points the sync at another pack.toml (for testing).
set -eu
cd "$(dirname "$0")"
exec "${JAVA:-java}" "-Xmx${MEMORY:-10G}" -jar campfiremons-server.jar "$@"

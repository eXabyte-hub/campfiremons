#!/bin/sh
# Prism pre-launch hook for the local dev instance: re-index the repo, then sync the instance from it.
# Prism runs this with INST_MC_DIR / INST_JAVA set (see instance.cfg written by setup-dev-instance.sh).
set -eu
REPO="$(cd "$(dirname "$0")/.." && pwd)"
PACKWIZ="${PACKWIZ:-$HOME/go/bin/packwiz}"

(cd "$REPO" && "$PACKWIZ" refresh)
cd "$INST_MC_DIR"
exec "$INST_JAVA" -jar packwiz-installer-bootstrap.jar ${PACKWIZ_INSTALLER_ARGS:-} "file://$REPO/pack.toml"

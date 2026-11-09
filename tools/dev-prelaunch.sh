#!/bin/sh
# Prism pre-launch hook for the local dev instance: re-index the repo, then sync the instance from it.
# Prism runs this with INST_MC_DIR / INST_JAVA set (see instance.cfg written by setup-dev-instance.sh).
set -eu
REPO="$(cd "$(dirname "$0")/.." && pwd)"
PACKWIZ="${PACKWIZ:-$HOME/go/bin/packwiz}"

# With Java on auto-detect (global JavaPath empty), Prism sets INST_JAVA to its data folder, not a java binary.
# Fall back to Prism's bundled Java 21 runtime, then any bundled runtime, then java on PATH.
JAVA="${INST_JAVA:-}"
if [ ! -f "$JAVA" ] || [ ! -x "$JAVA" ]; then
    PRISM_DIR="$(cd "$INST_MC_DIR/../../.." && pwd)"
    for candidate in "$PRISM_DIR"/java/java-runtime-delta/bin/java "$PRISM_DIR"/java/*/bin/java "$(command -v java || true)"; do
        if [ -f "$candidate" ] && [ -x "$candidate" ]; then JAVA="$candidate"; break; fi
    done
fi
if [ ! -f "$JAVA" ] || [ ! -x "$JAVA" ]; then
    echo "dev-prelaunch: no Java found (INST_JAVA='${INST_JAVA:-}')" >&2
    exit 1
fi

(cd "$REPO" && "$PACKWIZ" refresh)
cd "$INST_MC_DIR"
exec "$JAVA" -jar packwiz-installer-bootstrap.jar ${PACKWIZ_INSTALLER_ARGS:-} "file://$REPO/pack.toml"

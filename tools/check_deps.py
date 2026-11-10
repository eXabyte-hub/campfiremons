"""List required mod dependencies that no installed jar provides (NeoForge only checks this at launch).

    python -I tools/check_deps.py [--server] [path/to/mods]

Reads META-INF/neoforge.mods.toml from every jar (and jars nested via JarJar), collects provided mod ids and
`type = "required"` dependencies, and prints anything missing. Run after `packwiz mr add`, before launching.
With --server, dependencies a dedicated server doesn't enforce (`side = "CLIENT"`) are skipped: point it at a
server mods folder, e.g. one prepared with `start.sh --sync-only`.
"""
import glob
import io
import os
import sys
import tomllib
import zipfile

DEFAULT = os.path.expanduser("~/.local/share/PrismLauncher/instances/Campfiremons Dev/minecraft/mods")
BUILTIN = {"minecraft", "neoforge", "forge", "java"}


def read_jar(data, name, provided, required, server):
    try:
        z = zipfile.ZipFile(io.BytesIO(data))
    except zipfile.BadZipFile:
        return
    for nested in (n for n in z.namelist() if n.startswith("META-INF/jarjar/") and n.endswith(".jar")):
        read_jar(z.read(nested), name, provided, required, server)
    if "META-INF/neoforge.mods.toml" not in z.namelist():
        return
    try:
        toml = tomllib.loads(z.read("META-INF/neoforge.mods.toml").decode("utf-8", "replace"))
    except tomllib.TOMLDecodeError:
        return
    for mod in toml.get("mods", []):
        provided.add(mod.get("modId", ""))
    for owner, deps in toml.get("dependencies", {}).items():
        for dep in deps if isinstance(deps, list) else []:
            if server and dep.get("side", "BOTH").upper() == "CLIENT":
                continue
            if dep.get("type", "required" if dep.get("mandatory", False) else "optional") == "required":
                required.append((owner, dep.get("modId"), dep.get("versionRange", ""), name))


def main():
    args = [a for a in sys.argv[1:] if a != "--server"]
    server = "--server" in sys.argv[1:]
    moddir = args[0] if args else DEFAULT
    provided, required = set(BUILTIN), []
    for path in sorted(glob.glob(os.path.join(moddir, "*.jar"))):
        read_jar(open(path, "rb").read(), os.path.basename(path), provided, required, server)
    missing = [(o, d, v, j) for o, d, v, j in required if d not in provided]
    for owner, dep, versions, jar in missing:
        print(f"MISSING {dep} {versions}  (required by {owner}, {jar})")
    print(f"{len(provided)} mod ids provided, {len(required)} required deps, {len(missing)} missing")
    sys.exit(1 if missing else 0)


if __name__ == "__main__":
    main()

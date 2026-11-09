"""Check that every Modrinth-sourced file in the pack is a build for our Minecraft version and loader.

packwiz sometimes picks a newer build tagged only for later versions (e.g. Terralith 2.5.8 is 1.21.2-1.21.4 only).

    python -I tools/check_versions.py
"""
import json
import re
import sys
import tomllib
import urllib.parse
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
UA = {"User-Agent": "campfiremons-version-check/0.1"}


def main():
    pack = tomllib.loads((REPO / "pack.toml").read_text())
    mc, loader = pack["versions"]["minecraft"], next(k for k in pack["versions"] if k != "minecraft")
    files = {}
    for p in REPO.glob("*/*.pw.toml"):
        meta = tomllib.loads(p.read_text())
        mr = meta.get("update", {}).get("modrinth")
        if mr:
            files[mr["version"]] = (p.relative_to(REPO), meta.get("filename", ""))
    ids = list(files)
    bad, connector = [], []
    for i in range(0, len(ids), 100):
        q = urllib.parse.urlencode({"ids": json.dumps(ids[i:i + 100])})
        for v in json.load(urllib.request.urlopen(urllib.request.Request(f"https://api.modrinth.com/v2/versions?{q}", headers=UA))):
            path, filename = files[v["id"]]
            if path.parts[0] != "mods":
                continue  # resource/shader packs aren't loader-specific
            if mc not in v["game_versions"]:
                bad.append(f"{path}: {filename} is for {v['game_versions']}")
            elif loader not in v["loaders"] and "datapack" not in v["loaders"]:
                # The official base pack runs a few Fabric-only mods through Sinytra Connector on purpose
                (connector if "fabric" in v["loaders"] else bad).append(f"{path}: {filename} ({v['loaders']})")
    for c in connector:
        print("via Connector", c)
    for b in bad:
        print("WRONG BUILD", b)
    print(f"{len(ids)} Modrinth files checked against Minecraft {mc} / {loader}: {len(bad)} wrong, "
          f"{len(connector)} Fabric-only via Connector")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()

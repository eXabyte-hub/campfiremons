"""Builds the release files into dist/ (CI runs this for every vX.Y.Z tag, see .github/workflows/release.yml):

  campfiremons-<version>-prism.zip    Prism instance for players; on every Play it syncs the pack from the release branch
  campfiremons-<version>-server.zip   server starter: start.sh installs NeoForge once, syncs the pack, then starts
  release-notes.md                    this version's CHANGELOG.md section, for the GitHub Release

Neither zip holds mod jars: packwiz-installer downloads them from Modrinth and CurseForge, so nothing is rehosted
(9 mods are CurseForge-only, which is why there is no .mrpack; DESIGN.md §7.2).

Usage: python3 tools/release/build.py
"""
import hashlib
import json
import os
import re
import sys
import tomllib
import urllib.request
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SERVER_FILES = Path(__file__).resolve().parent / "server"
DIST = REPO / "dist"

PACK_URL = "https://raw.githubusercontent.com/eXabyte-hub/campfiremons/release/pack.toml"
BOOTSTRAP_URL = ("https://github.com/packwiz/packwiz-installer-bootstrap/releases/download/v0.0.3/"
                 "packwiz-installer-bootstrap.jar")
BOOTSTRAP_SHA256 = "a8fbb24dc604278e97f4688e82d3d91a318b98efc08d5dbfcbcbcab6443d116c"


def fail(msg):
    sys.exit(f"build.py: {msg}")


def download_bootstrap():
    with urllib.request.urlopen(BOOTSTRAP_URL) as resp:
        data = resp.read()
    if hashlib.sha256(data).hexdigest() != BOOTSTRAP_SHA256:
        fail("packwiz-installer-bootstrap.jar doesn't match its pinned sha256")
    return data


def prism_files(versions, bootstrap):
    # $INST_JAVA is the instance's Java; Prism runs the command from the instance's minecraft/ folder
    instance_cfg = "\n".join([
        "[General]",
        "ConfigVersion=1.3",
        "InstanceType=OneSix",
        "name=Campfiremons",
        "iconKey=default",
        "AutomaticJava=true",
        "OverrideMemory=true",
        "MinMemAlloc=2048",
        "MaxMemAlloc=8192",
        "OverrideCommands=true",
        f'PreLaunchCommand="$INST_JAVA" -jar packwiz-installer-bootstrap.jar {PACK_URL}',
        "notes=Campfiremons updates itself from GitHub every time you press Play.",
        "",
    ])
    mmc_pack = {
        "components": [
            {"uid": "net.minecraft", "version": versions["minecraft"], "important": True},
            {"uid": "net.neoforged", "version": versions["neoforge"]},
        ],
        "formatVersion": 1,
    }
    return {
        "instance.cfg": (instance_cfg.encode(), 0o644),
        "mmc-pack.json": ((json.dumps(mmc_pack, indent=4) + "\n").encode(), 0o644),
        "minecraft/packwiz-installer-bootstrap.jar": (bootstrap, 0o644),
    }


def server_files(versions, bootstrap):
    start = (SERVER_FILES / "start.sh").read_text()
    pinned = re.search(r"^NEOFORGE_VERSION=(\S+)$", start, re.M).group(1)
    if pinned != versions["neoforge"]:
        fail(f"start.sh pins NeoForge {pinned} but pack.toml says {versions['neoforge']}; "
             "update NEOFORGE_VERSION and NEOFORGE_SHA256 in tools/release/server/start.sh")
    return {
        "start.sh": (start.encode(), 0o755),
        "server.properties": ((SERVER_FILES / "server.properties").read_bytes(), 0o644),
        "packwiz-installer-bootstrap.jar": (bootstrap, 0o644),
    }


def write_zip(path, files):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zf:
        for name, (data, mode) in sorted(files.items()):
            info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.external_attr = (0o100000 | mode) << 16  # regular file + permissions, so start.sh stays executable
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, data)
    print(f"  {path.relative_to(REPO)}")


def release_notes(version):
    changelog = (REPO / "CHANGELOG.md").read_text()
    match = re.search(rf"^## v{re.escape(version)}\b.*?$(.*?)(?=^## |\Z)", changelog, re.M | re.S)
    if not match:
        fail(f"CHANGELOG.md has no '## v{version}' section")
    return match.group(1).strip() + "\n"


def main():
    pack = tomllib.loads((REPO / "pack.toml").read_text())
    version, versions = pack["version"], pack["versions"]
    tag = os.environ.get("GITHUB_REF_NAME", "")
    if tag.startswith("v") and tag != f"v{version}":
        fail(f"tag {tag} doesn't match pack.toml version {version}")

    bootstrap = download_bootstrap()
    DIST.mkdir(exist_ok=True)
    print(f"Campfiremons {version} (Minecraft {versions['minecraft']}, NeoForge {versions['neoforge']}):")
    write_zip(DIST / f"campfiremons-{version}-prism.zip", prism_files(versions, bootstrap))
    write_zip(DIST / f"campfiremons-{version}-server.zip", server_files(versions, bootstrap))
    (DIST / "release-notes.md").write_text(release_notes(version))
    print("  dist/release-notes.md")


if __name__ == "__main__":
    main()

"""Builds the release files into dist/ (CI runs this for every vX.Y.Z tag, see .github/workflows/release.yml):

  Campfiremons.zip                    Prism instance for players; on every Play it syncs the pack from the release branch.
                                      No version in the name: Prism names the instance after the zip, and players see that
                                      name (also in their Discord status via CraftPresence) long after the version changes
  campfiremons-<version>-server.zip   server starter: campfiremons-server.jar (the jar a host starts) installs NeoForge
                                      once, syncs the pack, then starts the server; start.sh runs the same jar
  release-notes.md                    this version's CHANGELOG.md section, for the GitHub Release

Neither zip holds mod jars: packwiz-installer downloads them from Modrinth and CurseForge, so nothing is rehosted
(9 mods are CurseForge-only, which is why there is no .mrpack; DESIGN.md §7.2).

Usage: python3 tools/release/build.py
"""
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
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
# NeoForged's same-process starter (LGPL-2.1, shipped unmodified inside the launcher jar)
SERVERSTARTER_VERSION = "0.1.35"
SERVERSTARTER_URL = f"https://github.com/neoforged/ServerStarterJar/releases/download/{SERVERSTARTER_VERSION}/server.jar"
SERVERSTARTER_SHA256 = "d019d815868d451e57bdb965174b8443ec361336e84e9c41abc41a6c627bacd1"
# NeoForge server installer checksums; add the new version here when pack.toml's neoforge changes
NEOFORGE_SHA256 = {
    "21.1.264": "d7c035dd5436a7c524dfbad6df191b0ef34179fd3edfee9dc99262af3b80239b",
}


def fail(msg):
    sys.exit(f"build.py: {msg}")


def download(url, sha256, name):
    with urllib.request.urlopen(url) as resp:
        data = resp.read()
    if hashlib.sha256(data).hexdigest() != sha256:
        fail(f"{name} doesn't match its pinned sha256")
    return data


def download_bootstrap():
    return download(BOOTSTRAP_URL, BOOTSTRAP_SHA256, "packwiz-installer-bootstrap.jar")


def javac():
    for home in (os.environ.get("JAVA_HOME"),):
        if home and (Path(home) / "bin" / "javac").exists():
            return str(Path(home) / "bin" / "javac")
    found = shutil.which("javac")
    if not found:
        fail("no javac found: install a JDK 21 or set JAVA_HOME")
    return found


def launcher_jar(versions):
    """campfiremons-server.jar: tools/release/server/launcher/Launcher.java, its settings, and ServerStarterJar."""
    neoforge = versions["neoforge"]
    if neoforge not in NEOFORGE_SHA256:
        fail(f"no installer checksum for NeoForge {neoforge}: add it to NEOFORGE_SHA256 in tools/release/build.py")
    starter = download(SERVERSTARTER_URL, SERVERSTARTER_SHA256, "ServerStarterJar")
    with tempfile.TemporaryDirectory() as out:
        subprocess.run([javac(), "--release", "21", "-d", out, str(SERVER_FILES / "launcher" / "Launcher.java")],
                       check=True)
        classes = {p.relative_to(out).as_posix(): p.read_bytes() for p in Path(out).rglob("*.class")}
    settings = "\n".join([
        f"pack.url={PACK_URL}",
        f"neoforge.version={neoforge}",
        f"neoforge.sha256={NEOFORGE_SHA256[neoforge]}",
        f"bootstrap.url={BOOTSTRAP_URL}",
        f"bootstrap.sha256={BOOTSTRAP_SHA256}",
        f"serverstarter.version={SERVERSTARTER_VERSION}",
        "",
    ])
    manifest = "\r\n".join([
        "Manifest-Version: 1.0",
        "Main-Class: campfiremons.Launcher",
        "Launcher-Agent-Class: campfiremons.Launcher",
        "Premain-Class: campfiremons.Launcher",
        "", "",
    ])
    notice = (f"campfiremons/serverstarter.jar is NeoForged's ServerStarterJar {SERVERSTARTER_VERSION}, unmodified, "
              "licensed under the GNU LGPL 2.1.\nSource: https://github.com/neoforged/ServerStarterJar\n")
    files = {
        "META-INF/MANIFEST.MF": manifest.encode(),
        "campfiremons/launcher.properties": settings.encode(),
        "campfiremons/serverstarter.jar": starter,
        "campfiremons/THIRD-PARTY-NOTICE.txt": notice.encode(),
        **classes,
    }
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for name in ["META-INF/MANIFEST.MF"] + sorted(n for n in files if n != "META-INF/MANIFEST.MF"):
            zf.writestr(zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0)), files[name], zipfile.ZIP_DEFLATED)
    return buf.getvalue(), notice


def ini_string(value):
    # instance.cfg is read with Qt's INI rules: a value with quotes in it must be quoted as a whole, inner quotes
    # escaped. Written bare, `"$INST_JAVA" -jar` loses the space after the quote and becomes `<java>-jar`.
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def prism_files(versions, bootstrap):
    # $INST_JAVA is the instance's Java (quoted for paths with spaces); Prism runs the command from minecraft/
    pre_launch = f'"$INST_JAVA" -jar packwiz-installer-bootstrap.jar {PACK_URL}'
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
        f"PreLaunchCommand={ini_string(pre_launch)}",
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
    launcher, notice = launcher_jar(versions)
    return {
        "campfiremons-server.jar": (launcher, 0o644),
        "THIRD-PARTY-NOTICE.txt": (notice.encode(), 0o644),
        "start.sh": ((SERVER_FILES / "start.sh").read_bytes(), 0o755),
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
    write_zip(DIST / "Campfiremons.zip", prism_files(versions, bootstrap))
    write_zip(DIST / f"campfiremons-{version}-server.zip", server_files(versions, bootstrap))
    (DIST / "release-notes.md").write_text(release_notes(version))
    print("  dist/release-notes.md")


if __name__ == "__main__":
    main()

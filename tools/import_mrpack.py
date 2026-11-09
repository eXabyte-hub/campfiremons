"""Import the files of a Modrinth .mrpack into this packwiz pack at their exact versions.

packwiz has no `modrinth import`, so this writes one .pw.toml per file from the
pack's modrinth.index.json (URL, sha512, side), then you run `packwiz refresh`.
Overrides are NOT copied; pick what you want by hand (see README).

Usage: python -I tools/import_mrpack.py <pack.mrpack> [--dry-run]
"""
import json
import sys
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path

UA = {"User-Agent": "campfiremons-packwiz-import/0.1"}
REPO = Path(__file__).resolve().parent.parent
CLIENT_ONLY_DIRS = {"resourcepacks", "shaderpacks"}


def side_of(path, env):
    if path.split("/")[0] in CLIENT_ONLY_DIRS:
        return "client"
    client, server = env.get("client", "required"), env.get("server", "required")
    if server == "unsupported":
        return "client"
    if client == "unsupported":
        return "server"
    return "both"


def toml_str(s):
    return json.dumps(s)  # JSON string escaping is valid TOML basic-string escaping


def main():
    mrpack, dry = sys.argv[1], "--dry-run" in sys.argv
    idx = json.loads(zipfile.ZipFile(mrpack).read("modrinth.index.json"))
    entries = []
    for f in idx["files"]:
        url = next(u for u in f["downloads"] if "cdn.modrinth.com/data/" in u)
        parts = urllib.parse.urlparse(url).path.split("/")  # /data/<project>/versions/<version>/<file>
        entries.append((f, url, parts[2], parts[4]))

    ids = json.dumps(sorted({e[2] for e in entries}))
    q = urllib.parse.urlencode({"ids": ids})
    req = urllib.request.Request(f"https://api.modrinth.com/v2/projects?{q}", headers=UA)
    projects = {p["id"]: p for p in json.load(urllib.request.urlopen(req))}

    for f, url, project_id, version_id in entries:
        folder, filename = f["path"].rsplit("/", 1)
        proj = projects[project_id]
        out = REPO / folder / f"{proj['slug']}.pw.toml"
        body = "\n".join([
            f"name = {toml_str(proj['title'])}",
            f"filename = {toml_str(filename)}",
            f"side = {toml_str(side_of(f['path'], f.get('env', {})))}",
            "",
            "[download]",
            f"url = {toml_str(url)}",
            'hash-format = "sha512"',
            f"hash = {toml_str(f['hashes']['sha512'])}",
            "",
            "[update]",
            "[update.modrinth]",
            f"mod-id = {toml_str(project_id)}",
            f"version = {toml_str(version_id)}",
            "",
        ])
        if out.exists():
            print(f"skip (exists): {out.relative_to(REPO)}")
            continue
        print(f"{'would write' if dry else 'write'}: {out.relative_to(REPO)}  [{side_of(f['path'], f.get('env', {}))}]")
        if not dry:
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(body)


if __name__ == "__main__":
    main()

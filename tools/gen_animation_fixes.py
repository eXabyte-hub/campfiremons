"""Generate Cobblemon animation fixes into kubejs/assets/ (DESIGN.md §5, Cobblemon models).

Several mods replace Cobblemon's Pokémon files: Complete Cobblemon Collection (CCC) replaces some animation files,
Mega Showdown replaces some pose files. The game takes each file from the highest-priority source, so it can end up
with one mod's pose file and another's animations. When a pose asks for an animation its group doesn't have, the
client crashes the moment that animation plays (e.g. "Animation animation.lucario.sleep_quirk not found in animation
group lucario" when a Lucario fell asleep).

Cobblemon keys an animation group by file name (lucario.animation.json is group `lucario`) and keeps one file per
name. This tool rebuilds the winning file of every group a winning pose file asks too much of: the winning
animations plus each missing one, taken from a lower-priority copy of the same group (usually Cobblemon's own) or,
if no source has it at all, an empty placeholder so it plays nothing instead of crashing. The result goes in
kubejs/assets/, which ranks above every mod and resource pack.

Resource order comes from the dev instance's latest.log ("Reloading ResourceManager: ..."), so launch the dev
instance once after changing any Pokémon model mod, then re-run:
    python -I tools/gen_animation_fixes.py
"""
import json
import re
import shutil
import sys
import tomllib
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "kubejs" / "assets" / "cobblemon" / "bedrock" / "pokemon" / "animations"
INSTANCE = Path.home() / ".local/share/PrismLauncher/instances/Campfiremons Dev/minecraft"
POSERS, ANIMATIONS = "assets/cobblemon/bedrock/pokemon/posers/", "/animations/"
PLACEHOLDER = {"animation_length": 0.05, "bones": {}}
REFERENCE = re.compile(r"q\.bedrock(?:_quirk|_stateful|_primary)?\(\s*'([^']+)'\s*,\s*(?:q\.array\(([^)]*)\)|'([^']+)')")


def resource_order():
    """Mod ids and resource pack files from lowest to highest priority, as the client last loaded them."""
    log = (INSTANCE / "logs" / "latest.log").read_text(errors="replace")
    line = re.search(r"Reloading ResourceManager: (.*)", log)
    if not line:
        sys.exit("no resource order in the dev instance's latest.log: launch the dev instance once first")
    return [p.strip() for p in line.group(1).split(",")]


def mod_id(jar):
    try:
        toml = zipfile.ZipFile(jar).read("META-INF/neoforge.mods.toml").decode("utf-8", "replace")
    except KeyError:
        return None
    found = re.search(r'^\s*modId\s*=\s*"([^"]+)"', toml, re.M)
    return found.group(1) if found else None


def sources():
    """(name, {path: bytes}) for every shipped jar and resource pack with Cobblemon poses or animations, lowest first."""
    shipped = {}
    for folder, kind in (("mods", "mod"), ("resourcepacks", "file")):
        for meta in sorted((REPO / folder).glob("*.pw.toml")):
            path = INSTANCE / folder / tomllib.loads(meta.read_text())["filename"]
            if not path.exists():
                sys.exit(f"{path} is missing: sync the dev instance first")
            key = f"mod/{mod_id(path)}" if kind == "mod" else f"file/{path.name}"
            shipped[key] = path
    out = []
    for key in resource_order():
        if key not in shipped:
            continue
        with zipfile.ZipFile(shipped[key]) as z:
            files = {n: z.read(n) for n in z.namelist() if n.endswith(".json") and n.startswith("assets/cobblemon/bedrock/")
                     and (n.startswith(POSERS) or ANIMATIONS in n)}
        if files:
            out.append((key, files))
    return out


def references(raw):
    found = set()
    for group, array, single in REFERENCE.findall(raw.decode("utf-8", "replace")):
        names = re.findall(r"'([^']+)'", array) if array else [single]
        found |= {(group, name) for name in names}
    return found


def animations(raw):
    try:
        return json.loads(raw.decode("utf-8-sig"))
    except ValueError:
        return {"animations": {}}


def resolve(stack):
    """What the game ends up with: winning file per path, every copy per path, group -> winning file, and the
    animations winning poses ask for that their group lacks (group -> names)."""
    winner = {}  # path -> (source, bytes), highest priority last
    copies = {}  # path -> every source's copy, lowest first
    for name, files in stack:
        for path, raw in files.items():
            winner[path] = (name, raw)
            copies.setdefault(path, []).append((name, raw))
    # Cobblemon reads every animation file in path order and keeps the last one per file name
    groups = {}
    for path in sorted(p for p in winner if ANIMATIONS in p):
        groups[path.rsplit("/", 1)[1].removesuffix(".animation.json")] = path
    missing = {}
    for path in (p for p in winner if p.startswith(POSERS)):
        for group, name in references(winner[path][1]):
            file = groups.get(group)
            have = animations(winner[file][1]).get("animations", {}) if file else {}
            if f"animation.{group}.{name}" not in have:
                missing.setdefault(group, set()).add(name)
    return winner, copies, groups, missing


def ours():
    """Our generated files as a resource source (kubejs/assets ranks above every mod and pack)."""
    return ("kubejs/assets", {f"assets/cobblemon/bedrock/pokemon/animations/{p.relative_to(OUT).as_posix()}": p.read_bytes()
                              for p in OUT.rglob("*.json")})


def main():
    stack = sources()
    winner, copies, groups, missing = resolve(stack)

    shutil.rmtree(OUT, ignore_errors=True)
    restored = placeholders = 0
    for group, names in sorted(missing.items()):
        file = groups.get(group)
        if not file:  # no source ships this group at all: a file of placeholders under its name
            target = OUT / "campfiremons_placeholders" / f"{group}.animation.json"
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(json.dumps({"format_version": "1.8.0", "animations": {
                f"animation.{group}.{name}": PLACEHOLDER for name in sorted(names)}}, indent=1) + "\n")
            placeholders += len(names)
            print(f"  {group:28} (no file anywhere, placeholders): {', '.join(sorted(names))}")
            continue
        fixed = animations(winner[file][1])
        fixed.setdefault("animations", {})
        for name in sorted(names):
            key = f"animation.{group}.{name}"
            donors = [animations(raw).get("animations", {}) for _, raw in reversed(copies[file])]
            donors += [animations(raw).get("animations", {}) for _, files in reversed(stack)
                       for path, raw in files.items() if ANIMATIONS in path]
            found = next((d[key] for d in donors if key in d), None)
            fixed["animations"][key] = found if found is not None else PLACEHOLDER
            restored += found is not None
            placeholders += found is None
        target = OUT / file.split("/bedrock/pokemon/animations/", 1)[1]
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(fixed, indent=1) + "\n")
        print(f"  {group:28} (winning file from {winner[file][0]}): {', '.join(sorted(names))}")
    print(f"{len(missing)} animation groups fixed: {restored} animations restored, {placeholders} empty placeholders")
    left = resolve(stack + [ours()])[3]
    if left:
        sys.exit(f"still missing after the fixes: {left}")
    print("verified: with the fixes on top, every animation a winning pose asks for exists")


if __name__ == "__main__":
    main()

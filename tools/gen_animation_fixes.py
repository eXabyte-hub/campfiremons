"""Generate Cobblemon animation fixes into kubejs/assets/ (DESIGN.md §5, Cobblemon models).

Several mods and packs replace Cobblemon's Pokémon files: Complete Cobblemon Collection (CCC) replaces some animation
files, Mega Showdown some pose files, CobbleMotion both. Cobblemon keys animation groups and posers by file name
(lucario.animation.json is group `lucario`, posers/0448_lucario/lucario.json is poser `cobblemon:lucario`), reads
them in path order and keeps the last one per name, so it can end up with one source's pose file and another's
animations. When a pose asks for an animation its group doesn't have, the client crashes the moment that animation
plays (e.g. "Animation animation.lucario.sleep_quirk not found in animation group lucario" when a Lucario fell asleep).

This tool rebuilds the winning file of every group a winning pose asks too much of: the winning animations plus each
missing one, taken from a lower-priority copy of the same group (usually Cobblemon's own) or, if no source has it at
all, an empty placeholder so it plays nothing instead of crashing. The result goes in kubejs/assets/, which ranks
above every mod and resource pack.

Sources in NO_COPY don't allow copying their files (All Rights Reserved), so nothing of theirs is ever written here.
When one of their groups is the broken one, the Pokémon goes back to the files it had without them instead: the
previous group and the posers that use it, copied from the next source, at the NO_COPY paths so they win.

Mods' resource order comes from the dev instance's latest.log ("Reloading ResourceManager: ..."), resource packs'
from the default options, so sync the dev instance (launch it once after adding a mod), then re-run:
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
ASSETS = REPO / "kubejs" / "assets"
OUT = ASSETS / "cobblemon" / "bedrock" / "pokemon" / "animations"
POSER_OUT = ASSETS / "cobblemon" / "bedrock" / "pokemon" / "posers"
INSTANCE = Path.home() / ".local/share/PrismLauncher/instances/Campfiremons Dev/minecraft"
POSERS, ANIMATIONS = "assets/cobblemon/bedrock/pokemon/posers/", "/animations/"
# Posers a mod's resolver names but no source ships. CCC 1.8.4 adds Hisuian Growlithe (resolver, model, textures)
# without its poser, so Cobblemon can't draw it ("No poser found for name: cobblemon:growlithe_hisuian"). Ours uses only
# Cobblemon's procedural head look and four-leg walk on CCC's bone names, so it needs no animation file. Written on
# every run, after the posers folder is cleared.
MISSING_POSERS = {
    "0058_growlithe/growlithe_hisuian.json": {
        "head": "head",
        "rootBone": "growlithe",
        "portraitScale": 2.1, "portraitTranslation": [-0.53, -0.33, 0],
        "profileScale": 0.9, "profileTranslation": [0, 0.4, 0],
        "poses": {
            "standing": {"poseTypes": ["STAND", "NONE", "FLOAT", "PORTRAIT", "PROFILE"], "animations": ["q.look('head')"]},
            "walking": {"poseTypes": ["WALK", "SWIM"], "animations": [
                "q.look('head')",
                "q.quadruped_walk(0.66, 1.4, 'left_shoulder', 'right_shoulder', 'left_thigh', 'right_thigh')"]},
        },
    },
}
PLACEHOLDER = {"animation_length": 0.05, "bones": {}}
NO_COPY = ("file/Cobblemotion",)  # resource keys (prefixes) of sources whose files we may not copy
REFERENCE = re.compile(r"q\.bedrock(?:_quirk|_stateful|_primary)?\(\s*'([^']+)'\s*,\s*(?:q\.array\(([^)]*)\)|'([^']+)')")


def resource_order():
    """Mod ids and resource pack files from lowest to highest priority. Mods follow the dev client's last load
    (latest.log); resource pack files follow config/defaultoptions/options.txt, the order every new player gets, so
    a pack the dev client hasn't loaded yet still counts (and the dev instance's own pack choices don't matter)."""
    log = (INSTANCE / "logs" / "latest.log").read_text(errors="replace")
    line = re.search(r"Reloading ResourceManager: (.*)", log)
    if not line:
        sys.exit("no resource order in the dev instance's latest.log: launch the dev instance once first")
    loaded = [p.strip() for p in line.group(1).split(",")]
    options = (REPO / "config" / "defaultoptions" / "options.txt").read_text()
    files = [p for p in json.loads(re.search(r"^resourcePacks:(.*)$", options, re.M).group(1).strip())
             if p.startswith("file/")]
    rest = [p for p in loaded if not p.startswith("file/")]
    first = next((i for i, p in enumerate(loaded) if p.startswith("file/")), len(loaded))
    at = len([p for p in loaded[:first] if not p.startswith("file/")])  # resource packs sit above mod resources
    return rest[:at] + files + rest[at:]


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


def no_copy(source):
    return source.startswith(NO_COPY)


def by_name(paths, suffix):
    """name -> path of the file Cobblemon keeps: the last one in path order."""
    names = {}
    for path in sorted(paths):
        names[path.rsplit("/", 1)[1].removesuffix(suffix)] = path
    return names


def resolve(stack):
    """What the game ends up with: winning file per path, every copy per path, group -> file, poser -> file, and the
    animations the winning posers ask for that their group lacks (group -> {name: poser source})."""
    winner = {}  # path -> (source, bytes), highest priority last
    copies = {}  # path -> every source's copy, lowest first
    for name, files in stack:
        for path, raw in files.items():
            winner[path] = (name, raw)
            copies.setdefault(path, []).append((name, raw))
    groups = by_name([p for p in winner if ANIMATIONS in p], ".animation.json")
    posers = by_name([p for p in winner if p.startswith(POSERS)], ".json")
    missing = {}
    for path in posers.values():
        for group, name in references(winner[path][1]):
            file = groups.get(group)
            have = animations(winner[file][1]).get("animations", {}) if file else {}
            if f"animation.{group}.{name}" not in have:
                missing.setdefault(group, set()).add(name)
    return winner, copies, groups, posers, missing


def previous(copies, name, suffix, kind):
    """The file `name` would come from without the NO_COPY sources: (path, bytes) or None."""
    found = None
    for path in sorted(p for p in copies if p.rsplit("/", 1)[1] == name + suffix and (kind in p)):
        for source, raw in copies[path]:
            if not no_copy(source):
                found = (path, raw)
    return found


def ours():
    """Our generated files as a resource source (kubejs/assets ranks above every mod and pack)."""
    return ("kubejs/assets", {f"assets/{p.relative_to(ASSETS).as_posix()}": p.read_bytes()
                              for folder in (OUT, POSER_OUT) for p in folder.rglob("*.json")})


def write(path, raw):
    target = ASSETS / path.removeprefix("assets/")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(raw)


def revert_no_copy(stack):
    """Send every Pokémon whose broken group comes from a NO_COPY source back to its previous files."""
    for _ in range(10):
        winner, copies, groups, posers, missing = resolve(stack + [ours()])
        bad = sorted(g for g in missing if g in groups and no_copy(winner[groups[g]][0]))
        if not bad:
            return
        for group in bad:
            before = previous(copies, group, ".animation.json", ANIMATIONS)
            if not before:
                sys.exit(f"{group}: broken in a NO_COPY source and no other source has the group to go back to")
            write(groups[group], before[1])
            users = [n for n, path in posers.items() if no_copy(winner[path][0])
                     and any(g == group for g, _ in references(winner[path][1]))]
            kept = []
            for name in users:
                old = previous(copies, name, ".json", POSERS)
                if old:
                    write(posers[name], old[1])
                else:  # replaces a poser built into Cobblemon's code: it stays, the fixes below patch the group
                    kept.append(name)
            print(f"  {group:28} broken in {winner[groups[group]][0]}: back to {before[0].split('/')[-2]}"
                  f" (posers back: {', '.join(n for n in users if n not in kept) or 'none'};"
                  f" kept: {', '.join(kept) or 'none'})")
    sys.exit("reverting NO_COPY groups didn't settle")


def fix(stack, label):
    """Patch every group the winning posers ask too much of, for one set of enabled sources. Returns (groups,
    restored, placeholders)."""
    winner, copies, groups, posers, missing = resolve(stack + [ours()])
    restored = placeholders = 0
    for group, names in sorted(missing.items()):
        file = groups.get(group)
        if not file:  # no source ships this group at all: a file of placeholders under its name
            target = OUT / "campfiremons_placeholders" / f"{group}.animation.json"
            have = json.loads(target.read_text()) if target.exists() else {"format_version": "1.8.0", "animations": {}}
            have["animations"].update({f"animation.{group}.{name}": PLACEHOLDER for name in sorted(names)})
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(json.dumps(have, indent=1) + "\n")
            placeholders += len(names)
            print(f"  {group:28} (no file anywhere, placeholders): {', '.join(sorted(names))}")
            continue
        if no_copy(winner[file][0]):
            sys.exit(f"{group}: still broken in a NO_COPY source after reverting")
        fixed = animations(winner[file][1])
        fixed.setdefault("animations", {})
        for name in sorted(names):
            key = f"animation.{group}.{name}"
            donors = [animations(raw).get("animations", {}) for source, raw in reversed(copies[file]) if not no_copy(source)]
            donors += [animations(raw).get("animations", {}) for source, files in reversed(stack) if not no_copy(source)
                       for path, raw in files.items() if ANIMATIONS in path]
            found = next((d[key] for d in donors if key in d), None)
            fixed["animations"][key] = found if found is not None else PLACEHOLDER
            restored += found is not None
            placeholders += found is None
        write(file, (json.dumps(fixed, indent=1) + "\n").encode())
        print(f"  {group:28} (winning file from {winner[file][0]}, {label}): {', '.join(sorted(names))}")
    return len(missing), restored, placeholders


def main():
    stack = sources()
    # Players can leave resource packs off, so the fixes have to hold both ways
    scenarios = [("all sources", stack), ("without resource packs", [s for s in stack if not s[0].startswith("file/")])]
    shutil.rmtree(OUT, ignore_errors=True)
    shutil.rmtree(POSER_OUT, ignore_errors=True)
    for path, poser in MISSING_POSERS.items():
        (POSER_OUT / path).parent.mkdir(parents=True, exist_ok=True)
        (POSER_OUT / path).write_text(json.dumps(poser, indent=1) + "\n")
    revert_no_copy(stack)
    total = [0, 0, 0]
    for label, part in scenarios:
        total = [a + b for a, b in zip(total, fix(part, label))]
    print(f"{total[0]} animation groups fixed: {total[1]} animations restored, {total[2]} empty placeholders")
    for label, part in scenarios:
        left = resolve(part + [ours()])[4]
        if left:
            sys.exit(f"still missing ({label}) after the fixes: {left}")
    written = [f"assets/{p.relative_to(ASSETS).as_posix()}" for folder in (OUT, POSER_OUT) for p in folder.rglob("*.json")]
    no_copy_files = {path: raw for name, files in stack if no_copy(name) for path, raw in files.items()}
    for path in written:  # nothing of a NO_COPY source in our files
        ours_raw = (ASSETS / path.removeprefix("assets/")).read_bytes()
        theirs = animations(no_copy_files[path]).get("animations", {}) if path in no_copy_files else {}
        mine = animations(ours_raw).get("animations", {})
        shared = [k for k, v in theirs.items() if mine.get(k) == v and v != PLACEHOLDER]
        if shared and not any(mine.get(k) == v for name, files in stack if not no_copy(name)
                              for f, raw in files.items() if f.endswith(path.rsplit("/", 1)[1])
                              for k, v in animations(raw).get("animations", {}).items() if k in shared):
            sys.exit(f"{path} carries animations copied from a NO_COPY source: {shared[:5]}")
    print(f"verified: every animation a winning pose asks for exists, with and without resource packs; "
          f"{len(written)} files, none copied from {', '.join(NO_COPY)}")


if __name__ == "__main__":
    main()

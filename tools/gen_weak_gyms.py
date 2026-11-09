"""Generate the local-only "weak gyms" test datapack: every stage trainer (Brock … Champion Terry) keeps its real
ID, name and series, but fields one Lv5 Magikarp that only knows Splash. Lets you test stage progression with real
RCT wins. Never shipped (tools/ is packwiz-ignored); toggle per world with /datapack enable|disable.

    python -I tools/gen_weak_gyms.py [path/to/rctmod.jar]
"""
import glob
import json
import os
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # run with `python -I`, which drops the script dir
import gen_finds  # noqa: E402  STAGE_TRAINERS: the trainers whose wins grant stages

PACK = Path(__file__).resolve().parent / "testpacks" / "campfiremons-weak-gyms"
DEFAULT_JAR = os.path.expanduser("~/.local/share/PrismLauncher/instances/Campfiremons Dev/minecraft/mods/rctmod-*.jar")

WEAK_TEAM = [{
    "species": "magikarp", "gender": "MALE", "level": 5, "nature": "hardy", "ability": "swiftswim",
    "moveset": ["splash"], "ivs": {}, "evs": {},
}]


def main():
    jar = sys.argv[1] if len(sys.argv) > 1 else sorted(glob.glob(DEFAULT_JAR))[-1]
    z = zipfile.ZipFile(jar)
    out = PACK / "data" / "rctmod" / "trainers"
    out.mkdir(parents=True, exist_ok=True)
    (PACK / "pack.mcmeta").write_text(json.dumps({"pack": {
        "pack_format": 48,
        "description": "Campfiremons TEST ONLY: stage trainers field one Lv5 Magikarp. Never shipped.",
    }}, indent=2) + "\n")
    ids = [t for trainers in gen_finds.STAGE_TRAINERS.values() for t in trainers]
    for tid in ids:
        trainer = json.loads(z.read(f"data/rctmod/trainers/{tid}.json"))
        trainer.update({"team": WEAK_TEAM, "bag": [], "battleRules": {"maxItemUses": 0}})
        (out / f"{tid}.json").write_text(json.dumps(trainer, indent=2) + "\n")
    print(f"wrote {len(ids)} weak trainers to {PACK.relative_to(PACK.parents[2])}")


if __name__ == "__main__":
    main()

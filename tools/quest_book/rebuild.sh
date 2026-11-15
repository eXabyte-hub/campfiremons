#!/bin/sh
# Rebuild the quest book from the original v0.1.9 book (commit 8b5548e), never from an already rebuilt one, then
# validate it. In-game edits made since the last rebuild are lost: port them into the builder first.
set -e
if [ "$1" != "--new-ids" ]; then
  echo "rebuild.sh gives every quest, image and chapter added since v0.1.9 a new random ID, which resets players'" >&2
  echo "progress on them now that the v0.1.10 book is live. Edit the book in place, or make build_book.py reuse the" >&2
  echo "current IDs first; pass --new-ids to rebuild anyway." >&2
  exit 1
fi
cd "$(dirname "$0")/../.."
rm -rf config/ftbquests/quests
git checkout 8b5548e -- config/ftbquests && git reset -q -- config/ftbquests
python3 tools/quest_book/build_book.py
python3 tools/quest_book/validate.py

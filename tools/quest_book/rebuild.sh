#!/bin/sh
# Rebuild the quest book from the original v0.1.9 book (commit 8b5548e), never from an already rebuilt one, then
# validate it. In-game edits made since the last rebuild are lost: port them into the builder first.
set -e
cd "$(dirname "$0")/../.."
rm -rf config/ftbquests/quests
git checkout 8b5548e -- config/ftbquests && git reset -q -- config/ftbquests
python3 tools/quest_book/build_book.py
python3 tools/quest_book/validate.py

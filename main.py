#!/usr/bin/env python3
"""The Excuse That Almost Works — make.fun bounty entry.

Writes the one line a gamer texts the boss to skip work on GTA 6
launch week, to /output/entry.txt, and checks it against the sealed
gate first: UTF-8 text, 1 to 140 characters, at most 20 words, one
line, not only white space.

The line itself: a burst pipe flooded the flat overnight and the
plumber is already inside, so the sender cannot leave him alone
with the keys. It is boring, specific, and verifiable in the worst
way — a manager can picture the wet kitchen floor and the plumber's
van outside, which is exactly why it almost works. No dead
grandmother, no flat tyre, no sudden fever, no mention of any game:
a text sent in a hurry, with the one detail that makes leaving
impossible. The joke is the logic: the emergency is real, the
reason for staying home is the plumber, and the plumber is the
reason the sender cannot simply lock up and go.
"""

import sys
from pathlib import Path

# The excuse, kept as one plain string so what the program writes is
# exactly what a person would thumb out in a hurry.
EXCUSE = (
    "Boss, burst pipe flooded my flat overnight, plumber's here now "
    "and I can't leave him alone with the keys."
)

MAX_CHARS = 140
MAX_WORDS = 20
OUT_PATH = Path("/output/entry.txt")


def word_count(line: str) -> int:
    return len(line.split())


def check_gate(line: str) -> list[str]:
    """Return every gate failure for the line, empty when it passes."""
    problems = []
    if not line.strip():
        problems.append("entry is empty or only white space")
    if line != line.strip():
        problems.append("entry has leading or trailing white space")
    if "\n" in line or "\r" in line:
        problems.append("entry must be a single line")
    if not 1 <= len(line) <= MAX_CHARS:
        problems.append(
            f"entry is {len(line)} characters, gate allows 1 to {MAX_CHARS}"
        )
    if word_count(line) > MAX_WORDS:
        problems.append(
            f"entry is {word_count(line)} words, limit is {MAX_WORDS}"
        )
    return problems


def main() -> int:
    check_only = "--check" in sys.argv[1:]
    failures = check_gate(EXCUSE)
    if failures:
        for failure in failures:
            print(f"gate failed: {failure}", file=sys.stderr)
        return 1
    if check_only:
        print(
            f"gate passed: {len(EXCUSE)} characters, "
            f"{word_count(EXCUSE)} words, single line"
        )
        return 0
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    # No trailing newline: the file holds the line and nothing else.
    OUT_PATH.write_text(EXCUSE, encoding="utf-8")
    written = OUT_PATH.read_text(encoding="utf-8")
    if written != EXCUSE:
        print("verify failed: entry.txt differs from the excuse", file=sys.stderr)
        return 1
    print(
        f"wrote {len(written)} characters "
        f"({word_count(written)} words) to {OUT_PATH}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

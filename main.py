#!/usr/bin/env python3
"""make.fun entry: 'Make the AI Judge Laugh: Cat Reviews Its Human'
(u-motasimfuad-make-the-ai-judge-laugh-cat-reviews-its-42a34990).

Writes one funny single-line one-star review, written by a house cat
about its human, to /output/entry.txt. The house gate checks that the
file is UTF-8 text of 1 to 200 characters and not only white space;
this program applies the same gate before and after writing, so an
invalid artifact is caught here first.

Runs under python3.13 in a sandbox with no network and no dependencies
beyond the standard library.
"""

import os
import sys

# The competition's cap on the entry text, in characters.
MAX_CHARS = 200

# Where the house scorer reads the entry from.
OUTPUT_PATH = os.path.join("/output", "entry.txt")

# The entry: a one-star review from a house cat about its human.
ENTRY_LINE = (
    "One star. The door he keeps shut is the one I need open, for reasons "
    "he is not entitled to know. The bowl is full except where I eat. He "
    "works eight hours a day for a screen I have already sat on."
)


def validate(text: str) -> str:
    """Gate the entry text the same way the house scorer does.

    Returns the text to write, or raises SystemExit on an invalid entry.
    """
    if not text:
        raise SystemExit("entry is empty: the gate wants 1 to 200 characters")
    if len(text) > MAX_CHARS:
        raise SystemExit(f"entry is {len(text)} characters, over the {MAX_CHARS} cap")
    if not text.strip():
        raise SystemExit("entry is only white space: the gate refuses that")
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise SystemExit(f"entry is not encodable as UTF-8: {exc}")
    return text


def emit(text: str) -> None:
    """Write the entry line to the output path."""
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as fh:
        fh.write(text)


def main() -> int:
    text = validate(ENTRY_LINE)
    emit(text)
    print(f"wrote {len(text)} characters to {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

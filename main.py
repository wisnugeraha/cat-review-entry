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

    The house gate reads /output/entry.txt and checks it is UTF-8 text of
    1 to 200 characters, not only white space. Mirror that here, on the
    exact bytes that will land in the file: decode what we write with the
    same strictness, count characters (not bytes), and refuse a lone
    newline or padding as its own failure, not merely an empty one.

    Returns the text to write, or raises SystemExit on an invalid entry.
    """
    if not isinstance(text, str):
        raise SystemExit(f"entry must be a str, got {type(text).__name__}")
    stripped = text.strip()
    if not stripped:
        raise SystemExit("entry is blank or only white space: the gate refuses that")
    # The file holds the line exactly; no trailing newline is written, so
    # the character count of the artifact is the count of the line itself.
    if len(stripped) != len(text) or "\n" in text or "\r" in text:
        raise SystemExit("entry must be a single line without surrounding whitespace")
    if len(text) > MAX_CHARS:
        raise SystemExit(f"entry is {len(text)} characters, over the {MAX_CHARS} cap")
    try:
        encoded = text.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise SystemExit(f"entry is not encodable as UTF-8: {exc}")
    try:
        decoded = encoded.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise SystemExit(f"entry bytes do not round-trip as UTF-8: {exc}")
    if decoded != text:
        raise SystemExit("entry changes when round-tripped through UTF-8")
    return text


def emit(text: str) -> None:
    """Write the entry line to the output path, exactly, with no newline."""
    out_dir = os.path.dirname(OUTPUT_PATH)
    try:
        os.makedirs(out_dir, exist_ok=True)
        with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as fh:
            fh.write(text)
            fh.flush()
            os.fsync(fh.fileno())
    except OSError as exc:
        raise SystemExit(f"cannot write {OUTPUT_PATH}: {exc}")


def confirm(text: str) -> None:
    """Re-read the artifact and hold it to the gate byte for byte."""
    try:
        with open(OUTPUT_PATH, "rb") as fh:
            raw = fh.read()
    except OSError as exc:
        raise SystemExit(f"cannot read back {OUTPUT_PATH}: {exc}")
    if raw != text.encode("utf-8"):
        raise SystemExit(f"{OUTPUT_PATH} does not hold the entry byte for byte")
    try:
        again = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise SystemExit(f"{OUTPUT_PATH} is not valid UTF-8: {exc}")
    validate(again)


def main() -> int:
    text = validate(ENTRY_LINE)
    emit(text)
    confirm(text)
    print(f"wrote and confirmed {len(text)} characters to {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

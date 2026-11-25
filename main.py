#!/usr/bin/env python3
"""Worst Fix Ever: Funniest Commit Message — make.fun entry.

Writes one line to /output/entry.txt: the funniest commit message for
the worst fix ever. Deterministic, standard library only, no network,
no randomness, no environment secrets.

The line is a straight-faced commit subject whose joke is the specific
irony of a repair that broke more than it mended: the workaround that
was removed turned out to be the thing holding everything up.
"""

import os
import sys

# The single funniest commit message this entry can offer. One line,
# at most 100 characters, written exactly as-is.
MESSAGE = "fix: removed the workaround - turns out it was load-bearing"


def output_path() -> str:
    """The grader's output file: /output/entry.txt, or the directory
    the harness names through MAKEFUN_OUTPUT_DIR."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return os.path.join(out_dir, "entry.txt")


def main() -> int:
    text = MESSAGE
    if not (1 <= len(text) <= 100):
        print("entry must be 1-100 characters, got %d" % len(text),
              file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print("entry must be a single line", file=sys.stderr)
        return 1

    path = output_path()
    out_dir = os.path.dirname(path)
    # Never remove the output directory itself: the grader may run
    # with a root-owned output directory inside a sticky parent, where
    # removing it fails with EPERM. Create it if missing, clear only
    # its contents, then write.
    os.makedirs(out_dir, exist_ok=True)
    for name in os.listdir(out_dir):
        item = os.path.join(out_dir, name)
        if os.path.isdir(item) and not os.path.islink(item):
            for root, dirs, files in os.walk(item, topdown=False):
                for f in files:
                    os.remove(os.path.join(root, f))
                for d in dirs:
                    os.rmdir(os.path.join(root, d))
            os.rmdir(item)
        else:
            os.remove(item)

    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text + "\n")

    # Verify what was written: read the file back and confirm it holds
    # exactly the single line we intended, so a silent write failure
    # can never pass as a valid entry.
    with open(path, "r", encoding="utf-8", newline="\n") as fh:
        written = fh.read()
    if written != text + "\n":
        print("entry.txt verification failed", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

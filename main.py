#!/usr/bin/env python3
"""Entry point: copy the pre-drawn front page to the grader's output path.

The image itself is built at authoring time by draw.py and shipped in this
repository as entry.png; this program only copies those exact bytes, so both
grader runs write identical output. Standard library only, no network.
"""
import os
import shutil
import sys


def run():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    run()
    sys.exit(0)

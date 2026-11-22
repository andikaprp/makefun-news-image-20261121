#!/usr/bin/env python3
"""Stdlib-only entrypoint: copy the shipped entry.png to the output dir."""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def main():
    os.makedirs(OUT, exist_ok=True)
    shutil.copyfile(os.path.join(HERE, "entry.png"), os.path.join(OUT, "entry.png"))


if __name__ == "__main__":
    main()

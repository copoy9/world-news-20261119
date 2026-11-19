#!/usr/bin/env python3
"""make.fun entry for news-image-20261119: the day in one image.

The repository holds the finished front page as ``entry.png`` (drawn by
``gen.py`` during development).  This program's whole job is to deliver
those exact bytes to the grader: it copies ``entry.png`` from beside
itself to ``entry.png`` inside the output directory.

The output directory is ``/output`` in the grader's container; outside
it, the ``MAKEFUN_OUTPUT_DIR`` environment variable stands in for
``/output``, the same convention as the kit's starter.  Standard
library only, no network, and copying a fixed file means every run
writes identical bytes.
"""

import os
import shutil
from pathlib import Path


def main() -> None:
    here = Path(__file__).resolve().parent
    source = here / "entry.png"
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, out_dir / "entry.png")


if __name__ == "__main__":
    main()

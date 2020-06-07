###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


import difflib
from pathlib import Path


def get_unified_diff(original: str, modified: str, filename: Path) -> str:
    diff = difflib.unified_diff(a=original.splitlines(keepends=True),
                                b=modified.splitlines(keepends=True),
                                fromfile=str(filename),
                                tofile=str(filename))
    return ''.join(diff)

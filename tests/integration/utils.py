###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


import re
from pathlib import Path
from typing import Optional

from cmake_tidy.__main__ import main


def execute_cmake_tidy(command: Optional[str], arguments: list) -> int:
    try:
        if command:
            main([command] + arguments)
        else:
            main(arguments)
    except SystemExit as system_exited:
        return system_exited.code


def normalize(data: str) -> str:
    return data.replace('\r\n', '\n')


def mangle_version(data: str) -> str:
    return re.sub(r'[0-9]+', 'X', data)


def get_input_file(filename: str) -> str:
    return str(Path(__file__).resolve().parent / 'input_files' / filename)

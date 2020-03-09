###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################
from pathlib import Path

from cmake_tidy.__main__ import main


def execute_cmake_tidy(command: str, arguments: list) -> int:
    try:
        main([command] + arguments)
    except SystemExit as system_exited:
        return system_exited.code


def normalize(data: str) -> str:
    return data.replace('\r\n', '\n')


def get_input_file(filename: str) -> str:
    return str(Path(__file__).resolve().parent / 'input_files' / filename)

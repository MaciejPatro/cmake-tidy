###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


from pathlib import Path
from typing import Optional

from cmake_tidy.formatting.cmake_formatter import CMakeFormatter
from cmake_tidy.formatting.settings_reader import SettingsReader


def try_read_settings(filepath: Optional[Path]) -> dict:
    return SettingsReader().try_loading_format_settings(filepath)

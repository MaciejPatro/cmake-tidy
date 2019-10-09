import json
from pathlib import Path

from cmake_tidy.formatting.cmake_formatter import CMakeFormatter


def load_format_settings() -> dict:
    settings_file = Path.cwd() / '.cmake-tidy.json'

    if settings_file.exists():
        with settings_file.open() as file:
            return json.load(file)

    return _get_default_format_settings()


def _get_default_format_settings() -> dict:
    settings = dict()
    settings['succeeding_newlines'] = 2
    settings['tabs_as_spaces'] = True
    settings['tab_size'] = 4
    return settings

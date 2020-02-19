import json
from pathlib import Path


def load_format_settings() -> dict:
    settings = _get_default_format_settings()
    settings.update(_read_settings())
    return settings


def _read_settings():
    settings_file = Path.cwd() / '.cmake-tidy.json'
    if settings_file.exists():
        with settings_file.open() as file:
            return json.load(file)
    return dict()


def _get_default_format_settings() -> dict:
    settings = dict()
    settings['succeeding_newlines'] = 2
    settings['tabs_as_spaces'] = True
    settings['tab_size'] = 4
    settings['force_command_lowercase'] = True
    settings['space_between_command_and_begin_parentheses'] = False
    settings['line_length'] = 80
    settings['wrap_short_invocations_to_single_line'] = False
    settings['closing_parentheses_in_newline_when_split'] = False
    settings['unquoted_uppercase_as_keyword'] = False
    settings['keywords'] = []
    return settings


class SettingsReader:
    @staticmethod
    def load_format_settings() -> dict:
        return load_format_settings()

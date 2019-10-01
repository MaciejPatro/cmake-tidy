from cmake_tidy.formatting.cmake_formatter import CMakeFormatter


def load_format_settings() -> dict:
    return _get_default_format_settings()


def _get_default_format_settings() -> dict:
    settings = dict()
    settings['succeeding_newlines'] = 2
    return settings

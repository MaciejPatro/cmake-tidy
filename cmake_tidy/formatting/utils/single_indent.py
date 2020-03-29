###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


def get_single_indent(settings: dict) -> str:
    if not settings['tabs_as_spaces']:
        return '\t'
    return settings['tab_size'] * ' '

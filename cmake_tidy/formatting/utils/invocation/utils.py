###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


def fix_line_comments(args: list) -> list:
    for i in range(1, len(args)):
        if args[i].startswith('#'):
            args[i - 1] = ' '
    return args

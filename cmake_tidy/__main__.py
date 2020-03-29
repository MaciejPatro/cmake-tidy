###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


import sys

from cmake_tidy.commands.format.format_command import FormatCommand
from cmake_tidy.utils.command_line_handling.command_line_parser import CommandLineParser


def main(args=sys.argv[1:]):
    parser = __init_parser()
    arguments = parser.parse(args)
    sys.exit(__execute(arguments, parser))


def __init_parser() -> CommandLineParser:
    parser = CommandLineParser()
    parser.add_command(FormatCommand)
    return parser


def __execute(arguments, parser) -> int:
    if arguments.sub_command:
        return arguments.func(arguments)
    parser.print_help()
    return 0


if __name__ == "__main__":
    main()

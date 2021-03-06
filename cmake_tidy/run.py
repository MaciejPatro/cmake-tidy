###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


import sys

from cmake_tidy.commands.analyze.analyze_command import AnalyzeCommand
from cmake_tidy.commands.format.format_command import FormatCommand
from cmake_tidy.utils import ExitCodes
from cmake_tidy.utils.command_line_handling.command_line_parser import CommandLineParser
from cmake_tidy.version import show_version


def run():
    main()


def main(args=sys.argv[1:]):
    parser = __init_parser()
    arguments = parser.parse(args)
    sys.exit(__execute(arguments, parser))


def __init_parser() -> CommandLineParser:
    parser = CommandLineParser()
    parser.add_command(FormatCommand)
    parser.add_command(AnalyzeCommand)
    return parser


def __execute(arguments, parser) -> int:
    if arguments.version:
        return show_version()
    elif arguments.sub_command:
        return arguments.func(arguments)
    parser.print_help()
    return ExitCodes.SUCCESS

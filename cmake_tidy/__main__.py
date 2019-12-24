import sys

from cmake_tidy.commands.format.format_command import FormatCommand
from cmake_tidy.utils.command_line_handling.command_line_parser import CommandLineParser


def main(args=sys.argv[1:]):
    parser = CommandLineParser()
    parser.add_command(FormatCommand)
    arguments = parser.parse(args)
    if arguments.sub_command:
        arguments.func(arguments)
    else:
        parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()

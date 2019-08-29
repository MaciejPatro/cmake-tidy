import sys

from cmake_tidy.command_line_handling.command_line_parser import CommandLineParser


def main(args=sys.argv[1:]):
    parser = CommandLineParser()
    arguments = parser.parse(args)
    if arguments.sub_command:
        arguments.func(arguments)
    else:
        parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()

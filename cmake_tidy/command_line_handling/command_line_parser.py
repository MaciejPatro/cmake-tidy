import argparse

from cmake_tidy.command_line_handling.format_command import FormatCommand


class CommandLineParser:
    def __init__(self):
        self.__parser = argparse.ArgumentParser(prog='cmake-tidy',
                                                formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        self.__sub_parser = self.__parser.add_subparsers(title='sub-commands',
                                                         dest='sub_command',
                                                         help='see "cmake-tidy <command> --help" to read more '
                                                              'about a specific sub-command.')
        self.__commands = []
        self.__commands.append(FormatCommand(self.__sub_parser))

    def parse(self, args=None):
        return self.__parser.parse_args(args)

    def print_help(self):
        self.__parser.print_help()

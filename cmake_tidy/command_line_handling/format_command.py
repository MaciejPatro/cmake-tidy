from cmake_tidy.command_line_handling import arguments
from cmake_tidy.command_line_handling.command import Command
from cmake_tidy.configuration import create_configuration
from cmake_tidy.formatting.cmake_formatter import CMakeFormatter


class FormatCommand(Command):
    def __init__(self, parser):
        description = 'format file to align it to standard'
        super().__init__(parser, 'format', description)

        arguments.input(self._command_parser)

    def execute_command(self, args):
        config = create_configuration(args)
        print(f'Command<{args.sub_command}>: ')
        formatted_data = CMakeFormatter().format(config.input)
        print(formatted_data)

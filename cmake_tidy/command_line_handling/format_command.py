from cmake_tidy.command_line_handling import arguments
from cmake_tidy.command_line_handling.command import Command


class FormatCommand(Command):
    def __init__(self, parser):
        description = 'format file to align it to standard'
        super().__init__(parser, 'format', description)

        arguments.input(self._command_parser)

    def execute_command(self, args):
        print(f'{args.sub_command}')

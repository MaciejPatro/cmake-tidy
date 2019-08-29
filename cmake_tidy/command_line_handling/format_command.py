from cmake_tidy.command_line_handling.command import Command


class FormatCommand(Command):
    __FORMAT_CMD_NAME = 'format'

    def __init__(self, parser):
        description = 'format file to align it to standard'
        super().__init__(parser, self.__FORMAT_CMD_NAME, description)

    def execute_command(self, args):
        print(f'{args.sub_command}')

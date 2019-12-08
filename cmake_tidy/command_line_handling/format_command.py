from cmake_tidy.command_line_handling import arguments, Command
from cmake_tidy.app_configuration import create_configuration
from cmake_tidy.formatting import CMakeFormatter, load_format_settings
from cmake_tidy.parsing import CMakeParser


class FormatCommand(Command):
    def __init__(self, parser):
        description = 'format file to align it to standard'
        super().__init__(parser, 'format', description)

        arguments.input_data(self._command_parser)

    def execute_command(self, args):
        config = create_configuration(args)
        print(f'Command<{args.sub_command}>: ')

        parsed_input = self.__parse_input(config.input)
        formatted_data = self.__format_data(parsed_input)
        print(formatted_data)

    @staticmethod
    def __format_data(parsed_input):
        format_settings = load_format_settings()
        return CMakeFormatter(format_settings).format(parsed_input)

    @staticmethod
    def __parse_input(input_data: str):
        return CMakeParser().parse(input_data)

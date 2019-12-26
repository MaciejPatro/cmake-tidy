import sys

from cmake_tidy.commands.format import try_create_configuration, FormatConfiguration
from cmake_tidy.formatting import CMakeFormatter, load_format_settings
from cmake_tidy.parsing import CMakeParser
from cmake_tidy.utils.app_configuration.configuration import ConfigurationError
from cmake_tidy.utils.command_line_handling import arguments
from cmake_tidy.commands.command import Command
from cmake_tidy.utils.exit_codes import ExitCodes


class FormatCommand(Command):
    def __init__(self, parser):
        description = 'format file to align it to standard'
        super().__init__(parser, 'format', description)

        arguments.dry_run(self._command_parser)
        arguments.input_data(self._command_parser)

    def execute_command(self, args) -> int:
        try:
            config = try_create_configuration(args)
        except ConfigurationError as error:
            return self.__handle_configuration_error(error)
        return self.__execute(config)

    def __execute(self, config: FormatConfiguration) -> int:
        if config.dry_run:
            return ExitCodes.SUCCESS
        return self.__format_file(config)

    def __format_file(self, config: FormatConfiguration) -> int:
        parsed_input = self.__parse_input(config.input)
        formatted_data = self.__format_input_data(parsed_input)
        print(formatted_data)
        return ExitCodes.SUCCESS

    @staticmethod
    def __format_input_data(parsed_input):
        format_settings = load_format_settings()
        return CMakeFormatter(format_settings).format(parsed_input)

    @staticmethod
    def __parse_input(input_data: str):
        return CMakeParser().parse(input_data)

    @staticmethod
    def __handle_configuration_error(error):
        print('cmake-tidy format: ' + str(error), file=sys.stderr)
        return ExitCodes.FAILURE

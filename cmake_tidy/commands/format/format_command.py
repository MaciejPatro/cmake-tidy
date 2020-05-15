###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


import json

from cmake_tidy.commands import Command
from cmake_tidy.commands.format import try_create_configuration, FormatConfiguration, OutputWriter
from cmake_tidy.formatting import try_read_settings, CMakeFormatter
from cmake_tidy.formatting.settings_reader import SchemaValidationError
from cmake_tidy.parsing import CMakeParser
from cmake_tidy.parsing.cmake_parser import ParsingError
from cmake_tidy.utils.app_configuration import ConfigurationError
from cmake_tidy.utils.command_line_handling import arguments
from cmake_tidy.utils import ExitCodes


class FormatCommand(Command):
    __DESCRIPTION = 'format file to align it to standard'

    def __init__(self, parser):
        super().__init__(parser, 'format', FormatCommand.__DESCRIPTION)

        arguments.dump_config(self._command_parser)
        arguments.inplace(self._command_parser)
        arguments.input_data(self._command_parser)

    def execute_command(self, args) -> int:
        if args.dump_config:
            return self.__dump_config()
        return self.__format(args)

    def __dump_config(self) -> int:
        try:
            print(json.dumps(try_read_settings(), indent=2))
        except SchemaValidationError as error:
            return self._handle_error(error)
        return ExitCodes.SUCCESS

    def __format(self, args) -> int:
        try:
            config = try_create_configuration(args)
            return self.__format_file(config)
        except (ConfigurationError, SchemaValidationError, ParsingError) as error:
            return self._handle_error(error)

    def __format_file(self, configuration: FormatConfiguration) -> int:
        parsed_input = self.__parse_input(configuration.input)
        formatted_data = self.__format_input_data(parsed_input)
        OutputWriter(configuration).write(formatted_data)
        return ExitCodes.SUCCESS

    @staticmethod
    def __format_input_data(parsed_input) -> str:
        format_settings = try_read_settings()
        return CMakeFormatter(format_settings).format(parsed_input)

    @staticmethod
    def __parse_input(input_data: str):
        return CMakeParser().parse(input_data)

import json
import sys

from cmake_tidy.commands import Command
from cmake_tidy.commands.format import try_create_configuration, FormatConfiguration, OutputWriter
from cmake_tidy.formatting import CMakeFormatter, SettingsReader
from cmake_tidy.parsing import CMakeParser
from cmake_tidy.utils.app_configuration import ConfigurationError
from cmake_tidy.utils.command_line_handling import arguments
from cmake_tidy.utils import ExitCodes


def _format(args) -> int:
    def __format_file(configuration: FormatConfiguration) -> int:
        parsed_input = __parse_input(configuration.input)
        formatted_data = __format_input_data(parsed_input)
        OutputWriter(configuration).write(formatted_data)
        return ExitCodes.SUCCESS

    def __format_input_data(parsed_input) -> str:
        format_settings = SettingsReader.load_format_settings()
        return CMakeFormatter(format_settings).format(parsed_input)

    def __parse_input(input_data: str):
        return CMakeParser().parse(input_data)

    def __handle_configuration_error(raised_error: ConfigurationError) -> int:
        print('cmake-tidy format: ' + str(raised_error), file=sys.stderr)
        return ExitCodes.FAILURE

    try:
        config = try_create_configuration(args)
    except ConfigurationError as error:
        return __handle_configuration_error(error)
    return __format_file(config)


def _dump_config() -> int:
    print(json.dumps(SettingsReader.load_format_settings(), indent=2))
    return ExitCodes.SUCCESS


class FormatCommand(Command):
    def __init__(self, parser):
        description = 'format file to align it to standard'
        super().__init__(parser, 'format', description)

        arguments.dump_config(self._command_parser)
        arguments.inplace(self._command_parser)
        arguments.input_data(self._command_parser)

    def execute_command(self, args) -> int:
        if args.dump_config:
            return _dump_config()
        return _format(args)

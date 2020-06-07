###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


import json
from pathlib import Path

from cmake_tidy.commands import Command
from cmake_tidy.commands.format import try_create_configuration, FormatConfiguration, OutputWriter
from cmake_tidy.formatting import try_read_settings, CMakeFormatter
from cmake_tidy.parsing import CMakeParser
from cmake_tidy.utils.command_line_handling import arguments
from cmake_tidy.utils import ExitCodes
from cmake_tidy.utils.diff import get_unified_diff


class FormatCommand(Command):
    __DESCRIPTION = 'format file to align it to standard'

    def __init__(self, parser):
        super().__init__(parser, 'format', FormatCommand.__DESCRIPTION)

        arguments.dump_config(self._command_parser)
        arguments.inplace(self._command_parser)
        arguments.input_data(self._command_parser)
        arguments.diff(self._command_parser)
        arguments.verbose(self._command_parser)

    def execute_command(self, args) -> int:
        try:
            self.__try_execute_command(args)
            return ExitCodes.SUCCESS
        except Exception as error:
            return self._handle_error(error)

    def __try_execute_command(self, args):
        if args.dump_config:
            self.__try_dump_config(args)
        else:
            config = try_create_configuration(args)
            self.__print_filename_if_needed(args, config)
            formatted_file = self.__try_format_file(config)
            if args.diff:
                print(get_unified_diff(config.input, formatted_file, config.file))
            else:
                self.__try_output_formatted_file(config, formatted_file)

    @staticmethod
    def __print_filename_if_needed(args, config):
        if args.verbose:
            print(f'Formatting file: {config.file}')

    @staticmethod
    def __try_dump_config(args):
        filepath = Path(args.input) if args.input else None
        print(json.dumps(try_read_settings(filepath), indent=2))

    @staticmethod
    def __try_format_file(configuration: FormatConfiguration) -> str:
        parsed_input = CMakeParser().parse(configuration.input)
        format_settings = try_read_settings(configuration.file)
        return CMakeFormatter(format_settings).format(parsed_input)

    @staticmethod
    def __try_output_formatted_file(configuration: FormatConfiguration, formatted_file: str) -> None:
        OutputWriter(configuration).write(formatted_file)

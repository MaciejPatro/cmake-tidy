###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


import sys
from abc import ABC, abstractmethod

from cmake_tidy.utils import ExitCodes


class Command(ABC):
    def __init__(self, parser, command_name: str, description: str):
        self._command_parser = parser.add_parser(name=command_name, help=description)
        self._command_parser.set_defaults(func=self.execute_command)
        self._command_name = command_name

    @abstractmethod
    def execute_command(self, args) -> int:
        pass

    def _handle_error(self, raised_error: Exception) -> int:
        print(f'cmake-tidy {self._command_name}: {str(raised_error)}', file=sys.stderr)
        return ExitCodes.FAILURE

from abc import ABC, abstractmethod


class Command(ABC):
    def __init__(self, parser, command_name: str, description: str):
        self._command_parser = parser.add_parser(name=command_name, help=description)
        self._command_parser.set_defaults(func=self.execute_command)

    @abstractmethod
    def execute_command(self, args):
        pass

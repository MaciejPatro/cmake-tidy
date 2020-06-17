###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


from cmake_tidy.commands import Command
from cmake_tidy.utils import ExitCodes


class AnalyzeCommand(Command):
    __DESCRIPTION = 'analyze file to find violations against selected rules'

    def __init__(self, parser):
        super().__init__(parser, 'analyze', AnalyzeCommand.__DESCRIPTION)

    def execute_command(self, args) -> int:
        return ExitCodes.SUCCESS

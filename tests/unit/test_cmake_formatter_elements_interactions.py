from tests.unit.test_cmake_formatter import TestCMakeFormatter
from tests.unit.parser_composite_elements import file, command_invocation, spaces, line_ending


class TestCMakeFormatterElementsInteractions(TestCMakeFormatter):
    def test_command_invocation_should_be_by_default_lowercase(self):
        invocation = file() \
            .add(command_invocation('abc(')) \
            .add(spaces('   \t')) \
            .add(line_ending('# a comment', 1))
        self.assertFormatting('abc() # a comment\n', invocation)

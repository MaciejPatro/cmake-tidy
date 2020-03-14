from tests.unit.test_cmake_formatter import TestCMakeFormatter
from tests.unit.parser_composite_elements import file, command_invocation, spaces, line_ending, newlines


class TestCMakeFormatterElementsInteractions(TestCMakeFormatter):
    def test_command_invocation_should_be_by_default_lowercase(self):
        invocation = file() \
            .add(command_invocation('abc(')) \
            .add(spaces('   \t')) \
            .add(line_ending('# a comment', 1))
        self.assertFormatting('abc() # a comment\n', invocation)

    def test_if_statement_with_space_while_other_invocations_are_not_affected(self):
        self.settings['space_after_loop_condition'] = True
        invocation = file() \
            .add(command_invocation('if(')) \
            .add(newlines(1)) \
            .add(command_invocation('abc(')) \
            .add(spaces('   \t')) \
            .add(line_ending('# a comment', 1)) \
            .add(command_invocation('endif('))

        expectedFormatting = """if ()
  abc() # a comment
endif()"""

        self.assertFormatting(expectedFormatting, invocation)

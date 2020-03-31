###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


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
            .add(newlines(1)) \
            .add(command_invocation('endif('))

        expected_formatting = """if ()
  abc()
endif()"""

        self.assertFormatting(expected_formatting, invocation)

    def test_uppercase_if_statement_handled_correctly_like_lowercase(self):
        self.settings['space_after_loop_condition'] = True
        self.settings['force_command_lowercase'] = False

        invocation = file() \
            .add(command_invocation('IF(')) \
            .add(newlines(1)) \
            .add(command_invocation('abc(')) \
            .add(newlines(1)) \
            .add(command_invocation('ELSEIF (')) \
            .add(newlines(1)) \
            .add(command_invocation('def(')) \
            .add(newlines(1)) \
            .add(command_invocation('ENDIF('))

        expected_formatting = """IF ()
  abc()
ELSEIF ()
  def()
ENDIF()"""

        self.assertFormatting(expected_formatting, invocation)

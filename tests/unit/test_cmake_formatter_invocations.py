from tests.unit.parser_composite_elements import newlines, spaces, file, command_invocation, line_ending
from tests.unit.test_cmake_formatter import TestCMakeFormatter


class TestCMakeFormatterCommandInvocations(TestCMakeFormatter):
    def test_function_declaration_should_indent_correctly_within_its_scope(self):
        function_with_invocation_in_second_line = file() \
            .add(command_invocation('function(')) \
            .add(newlines(1)) \
            .add(line_ending('# comment', 1)) \
            .add(command_invocation('test(')) \
            .add(newlines(1)) \
            .add(command_invocation('endfunction(')) \
            .add(newlines(1)) \
            .add(command_invocation('test2('))
        expected_formatting = """function()
  # comment
  test()
endfunction()
test2()"""
        self.assertFormatting(expected_formatting, function_with_invocation_in_second_line)

    def test_if_statement_should_indent_properly_also_removing_unneeded_spaces(self):
        root = file() \
            .add(command_invocation('if(')) \
            .add(newlines(1)) \
            .add(spaces('         ')) \
            .add(command_invocation('test(')) \
            .add(newlines(1)) \
            .add(spaces('         ')) \
            .add(command_invocation('elseif(')) \
            .add(newlines(1)) \
            .add(spaces('         ')) \
            .add(command_invocation('test(')) \
            .add(newlines(1)) \
            .add(spaces('         ')) \
            .add(command_invocation('endif('))

        expected_formatting = """if()
  test()
elseif()
  test()
endif()"""

        self.assertFormatting(expected_formatting, root)

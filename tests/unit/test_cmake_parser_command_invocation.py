###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


from tests.unit.test_cmake_parser import TestCMakeParser
from tests.unit.parser_composite_elements import file, command_invocation, arguments, unquoted_argument, \
    bracket_argument, quoted_argument, spaces, newlines, parentheses, line_ending


class TestParseCommandInvocation(TestCMakeParser):
    def test_without_arguments(self):
        start_invocation = 'include('
        root = file().add(command_invocation(start_invocation, []))

        self.assertReprEqual(root, self.parser.parse(start_invocation + ')'))

    def test_with_empty_quoted_argument(self):
        start_invocation = 'include('
        root = file().add(command_invocation(start_invocation, arguments().add(quoted_argument(''))))

        self.assertReprEqual(root, self.parser.parse(start_invocation + '\"\")'))

    def test_with_unquoted_arguments_in_braces(self):
        start_invocation = 'include('
        expected_args = arguments().add(
            parentheses().add(
                arguments().add(unquoted_argument('some'))
            )
        )
        root = file().add(command_invocation(start_invocation, expected_args))

        self.assertReprEqual(root, self.parser.parse(start_invocation + '(some))'))

    def test_with_bracket_argument(self):
        start_invocation = 'function_name('
        bracket_start = '[['
        bracket_end = ']]'
        bracket_argument_data = 'this is bracket_dwad832423#$@#$ content]===] still there'

        root = file().add(command_invocation(start_invocation,
                                             arguments().add(bracket_argument(0, bracket_argument_data))))

        self.assertReprEqual(root, self.parser.parse(
            f'{start_invocation}{bracket_start}{bracket_argument_data}{bracket_end})'))

    def test_with_quoted_argument_with_escaped_quote_inside(self):
        start_invocation = 'name('
        argument_content = 'simple\n\\\" text'
        root = file().add(
            command_invocation(start_invocation,
                               arguments().add(quoted_argument(argument_content)))
        )

        self.assertReprEqual(root, self.parser.parse(
            f'{start_invocation}"{argument_content}")'))

    def test_real_add_test_command_example(self):
        command = """add_test(
    NAME dbg-${TARGET}-fast
    CONFIGURATIONS Debug
    COMMAND ${Runner_BINARY_DEBUG} $<TARGET_FILE:${TARGET}>
        ("${DATA_PATH_OPTION}"
        [===[--text]===])
    )"""

        expected_arguments_in_parentheses = parentheses().add(arguments()
                                                              .add(quoted_argument('${DATA_PATH_OPTION}'))
                                                              .add(newlines(1))
                                                              .add(spaces('        '))
                                                              .add(bracket_argument(3, '--text')))

        expected_args = arguments() \
            .add(newlines(1)) \
            .add(spaces('    ')) \
            .add(unquoted_argument('NAME')) \
            .add(spaces(' ')) \
            .add(unquoted_argument('dbg-${TARGET}-fast')) \
            .add(newlines(1)) \
            .add(spaces('    ')) \
            .add(unquoted_argument('CONFIGURATIONS')) \
            .add(spaces(' ')) \
            .add(unquoted_argument('Debug')) \
            .add(newlines(1)) \
            .add(spaces('    ')) \
            .add(unquoted_argument('COMMAND')) \
            .add(spaces(' ')) \
            .add(unquoted_argument('${Runner_BINARY_DEBUG}')) \
            .add(spaces(' ')) \
            .add(unquoted_argument('$<TARGET_FILE:${TARGET}>')) \
            .add(newlines(1)) \
            .add(spaces('        ')) \
            .add(expected_arguments_in_parentheses) \
            .add(newlines(1)) \
            .add(spaces('    '))
        expected_invocation = command_invocation('add_test(', expected_args)
        expected_parsed_structure = file().add(expected_invocation)

        self.assertReprEqual(expected_parsed_structure, self.parser.parse(command))

    def test_command_with_line_comment(self):
        command = """add_test(
    NAME # a name
    CONFIGURATIONS)"""

        expected_args = arguments() \
            .add(newlines(1)) \
            .add(spaces('    ')) \
            .add(unquoted_argument('NAME')) \
            .add(spaces(' ')) \
            .add(line_ending('# a name', 1)) \
            .add(spaces('    ')) \
            .add(unquoted_argument('CONFIGURATIONS'))

        expected_parsed_structure = file().add(command_invocation('add_test(', expected_args))

        self.assertReprEqual(expected_parsed_structure, self.parser.parse(command))

    def test_escape_sequence_in_quoted_argument(self):
        command = 'string("\\\\")'

        expected_args = arguments().add(quoted_argument('\\\\'))
        expected_parsed_structure = file().add(command_invocation('string(', expected_args))

        self.assertReprEqual(expected_parsed_structure, self.parser.parse(command))

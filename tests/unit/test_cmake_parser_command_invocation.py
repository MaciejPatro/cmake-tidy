from tests.unit.test_cmake_parser import TestCMakeParser
from tests.unit.parser_composite_elements import file, command_invocation, arguments, unquoted_argument, \
    bracket_argument, quoted_argument, spaces


class TestParseCommandInvocation(TestCMakeParser):
    def test_without_arguments(self):
        start_invocation = 'include('
        root = file().add(command_invocation(start_invocation, []))

        self.assertReprEqual(root, self.parser.parse(start_invocation + ')'))

    def test_with_unquoted_arguments_and_spaces(self):
        start_invocation = 'include \t('
        first_arg = 'CTest'
        whitespaces = ' '
        second_arg = '123'

        expected_arguments = arguments().add(unquoted_argument(first_arg)) \
            .add(spaces(whitespaces)) \
            .add(unquoted_argument(second_arg))
        root = file().add(command_invocation(start_invocation, expected_arguments))

        self.assertReprEqual(root, self.parser.parse(f'{start_invocation}{first_arg}{whitespaces}{second_arg})'))

    def test_with_bracket_argument(self):
        start_invocation = 'function_name('
        bracket_start = '[==['
        bracket_end = ']==]'
        bracket_argument_data = 'this is bracket_dwad832423#$@#$ content]===] still there'

        root = file().add(command_invocation(start_invocation,
                                             arguments().add(bracket_argument(2, bracket_argument_data))))

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

    def test_basic_command_invocation_with_different_arguments(self):
        # TODO: improve handling of command_name
        command_name = 'message('
        unquoted_arg = 'FATAL_ERROR'
        separation = ' '
        quoted_arg = 'Couldn\'t find assembler application'
        command = f'{command_name}{unquoted_arg}{separation}\"{quoted_arg}\")'

        root = file().add(
            command_invocation(command_name,
                               arguments()
                               .add(unquoted_argument(unquoted_arg))
                               .add(spaces(' '))
                               .add(quoted_argument(quoted_arg)))
        )

        self.assertReprEqual(root, self.parser.parse(command))

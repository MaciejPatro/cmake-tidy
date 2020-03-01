from cmake_tidy.formatting.utils.format_newline import FormatNewline
from cmake_tidy.utils.keyword_verifier import KeywordVerifier


class InvocationSplitter:
    def __init__(self, state: dict, settings: dict):
        self.__state = state
        self.__settings = settings
        self.__verifier = KeywordVerifier(settings)

    def split(self, invocation: dict) -> list:
        initial_indent = self.__state['indent']
        arguments = self.__prepare_newline_split_list_of_arguments(initial_indent, invocation)
        self.__ensure_closing_bracket_position(arguments)
        self.__rollback_indent_state(initial_indent)
        return arguments

    def __prepare_newline_split_list_of_arguments(self, initial_indent, invocation):
        arguments = []
        for arg in invocation['arguments']:
            newline = FormatNewline(self.__state, self.__settings)(1)
            if arg == ' ':
                arguments.append(newline)
            else:
                self.__handle_non_whitespace_arguments(arg, arguments, initial_indent)
        return arguments

    def __rollback_indent_state(self, initial_indent):
        self.__state['indent'] = initial_indent

    def __ensure_closing_bracket_position(self, arguments):
        if self.__settings['closing_parentheses_in_newline_when_split']:
            arguments.append(FormatNewline(self.__state, self.__settings)(1))

    def __handle_non_whitespace_arguments(self, arg, arguments, initial_indent):
        self.__update_indent_state(arg, initial_indent)
        self.__fix_line_comment(arg, arguments)
        arguments.append(arg)

    @staticmethod
    def __fix_line_comment(current_argument, arguments):
        if current_argument.startswith('#'):
            arguments[-1] = ' '

    def __update_indent_state(self, arg, initial_indent):
        if self.__verifier.is_keyword(arg):
            self.__state['indent'] = initial_indent + 1

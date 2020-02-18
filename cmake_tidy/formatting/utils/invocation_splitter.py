from cmake_tidy.formatting.utils.format_newline import FormatNewline
from cmake_tidy.utils.keyword_verifier import KeywordVerifier


class InvocationSplitter:
    def __init__(self, state: dict, settings: dict):
        self.__state = state
        self.__settings = settings
        self.__verifier = KeywordVerifier(settings)

    def split(self, invocation: dict) -> list:
        initial_indent = self.__state['indent']
        arguments = []
        for arg in invocation['arguments']:
            newline = FormatNewline(self.__state, self.__settings)(1)
            if arg == ' ':
                arguments.append(newline)
            else:
                if self.__verifier.is_keyword(arg):
                    self.__state['indent'] = initial_indent + 1
                arguments.append(arg)
        if self.__settings['closing_parentheses_in_newline_when_split']:
            arguments.append(FormatNewline(self.__state, self.__settings)(1))
        self.__state['indent'] = initial_indent
        return arguments

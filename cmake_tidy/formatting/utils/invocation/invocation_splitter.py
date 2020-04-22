###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


from cmake_tidy.formatting.utils.format_newline import FormatNewline
from cmake_tidy.formatting.utils.invocation.invocation_realign_modifier import InvocationRealignModifier
from cmake_tidy.formatting.utils.updaters.keyword_state_updater import KeywordStateUpdater
from cmake_tidy.lexical_data import KeywordVerifier


class InvocationSplitter:
    def __init__(self, state: dict, settings: dict):
        self.__prepare_state(state)
        self.__state_updater = KeywordStateUpdater(self.__state, settings)
        self.__verifier = KeywordVerifier(settings)
        self.__settings = settings

    def split(self, invocation: dict) -> list:
        args = self.__split_args_to_newlines(invocation['arguments'])
        args = self.__fix_line_comments(args)
        args = InvocationRealignModifier(self.__state, self.__settings).realign(args)
        return args + self.__add_closing_bracket_separator(invocation)

    def __split_args_to_newlines(self, args: list) -> list:
        if self.__verifier.is_keyword_or_property(args[0]):
            args = [FormatNewline(self.__state, self.__settings)(1)] + args
        return [self.__handle_argument(arg) for arg in args]

    def __handle_argument(self, arg: str) -> str:
        self.__state_updater.update_state(arg)
        return self.__get_converted_whitespace() if arg == ' ' else arg

    def __add_closing_bracket_separator(self, invocation: dict) -> list:
        if self.__settings['closing_parentheses_in_newline_when_split'] and \
                not self.__is_last_element_newline(invocation):
            return [FormatNewline(self.__state, self.__settings)(1)]
        return []

    @staticmethod
    def __is_last_element_newline(invocation: dict) -> bool:
        return invocation['arguments'][-1].startswith('\n')

    def __get_converted_whitespace(self) -> str:
        return FormatNewline(self.__state, self.__settings)(1)

    def __prepare_state(self, state: dict) -> None:
        self.__state = state.copy()
        if self.__state['has_first_class_keyword']:
            self.__state['indent'] -= 1
        self.__state['has_first_class_keyword'] = False
        self.__state['keyword_argument'] = False

    @staticmethod
    def __fix_line_comments(args: list) -> list:
        for i in range(len(args)):
            if args[i].startswith('#'):
                args[i - 1] = ' '
        return args

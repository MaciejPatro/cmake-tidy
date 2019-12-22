import re

from cmake_tidy.formatting.utils.tokens import Tokens


class FormatNewline:
    def __init__(self, state: dict, settings: dict):
        self.__state = state
        self.__settings = settings

    def __call__(self, data) -> str:
        return self.__format_newlines(data) + self.__prepare_initial_newline_indent()

    def __prepare_initial_newline_indent(self) -> str:
        return self.__state['indent'] * self.__settings['tab_size'] * ' '

    def __format_newlines(self, number_of_newlines: int) -> str:
        return '\n' * min(self.__settings['succeeding_newlines'], number_of_newlines)


class FormatStartCommandInvocation:
    def __init__(self, state: dict):
        self.__state = state

    def __call__(self, data) -> str:
        self.__state['indent'] += 1
        return data


class FormatCommandInvocation:
    __start_tokens = ['macro', 'while', 'foreach', 'if', 'function']
    __reindent_commands = ['endfunction', 'endif', 'elseif', 'endwhile', 'endforeach', 'endmacro',
                           'else']

    def __init__(self, state: dict):
        self.__state = state

    def __call__(self, data) -> str:
        original = ''.join(data)
        self.__update_state(original)
        return self.__add_reindent_tokens_where_needed(original)

    def __update_state(self, formatted):
        if not self.__is_start_of_special_command(formatted):
            self.__state['indent'] -= 1
        if self.__is_end_of_special_command(formatted):
            self.__state['indent'] -= 1
        self.__state['keyword_argument'] = False

    @staticmethod
    def __is_start_of_special_command(original: str) -> bool:
        return any([original.startswith(f'{token}(') for token in FormatCommandInvocation.__start_tokens])

    @staticmethod
    def __is_end_of_special_command(original: str) -> bool:
        return any([original.startswith(f'end{token}(') for token in FormatCommandInvocation.__start_tokens])

    @staticmethod
    def __add_reindent_tokens_where_needed(data: str) -> str:
        for reindent_cmd in FormatCommandInvocation.__reindent_commands:
            if data.startswith(f'{reindent_cmd}('):
                return Tokens.reindent + data
        return data


class FormatSpaces:
    def __init__(self, settings: dict, state: dict):
        self.__settings = settings
        self.__state = state

    def __call__(self, data) -> str:
        if self.__state['last'] is 'line_ending':
            return ''
        return data.replace('\t', ' ' * self.__settings['tab_size'])


class FormatArguments:
    __spacing = r'^[ \t]+$'

    def __init__(self, state: dict):
        self.__state = state

    def __call__(self, data) -> str:
        if data[0]:
            self.__update_state()
            return self.__format_arguments(data)
        return ''

    def __update_state(self):
        if self.__state['keyword_argument']:
            self.__state['indent'] -= 1

    def __format_arguments(self, data) -> str:
        data = self.__replace_spacings_between_arguments_with_single_space(data)
        data = self.__remove_spacing_from_first_element(data)
        data = self.__remove_spacing_from_last_element(data)
        return ''.join(data)

    @staticmethod
    def __replace_spacings_between_arguments_with_single_space(data: list) -> list:
        return [re.sub(FormatArguments.__spacing, ' ', element) for element in data]

    @staticmethod
    def __remove_spacing_from_first_element(data: list) -> list:
        return data[1:] if re.match(FormatArguments.__spacing, data[0]) else data

    @staticmethod
    def __remove_spacing_from_last_element(data: list) -> list:
        return data[:-1] if re.match(FormatArguments.__spacing, data[-1]) else data


class FormatUnquotedArgument:
    __keywords = ['TARGET']

    def __init__(self, state: dict):
        self.__state = state

    def __call__(self, data) -> str:
        self.__update_state(data)
        return data

    def __update_state(self, data: str) -> None:
        if self.__is_matching_any_of_keywords(data):
            self.__state['keyword_argument'] = True
            self.__state['indent'] += 1

    @staticmethod
    def __is_matching_any_of_keywords(data):
        return any([data == keyword for keyword in FormatUnquotedArgument.__keywords])


class FormatEndCommandInvocation:
    def __init__(self, state: dict):
        self.__state = state

    def __call__(self, data) -> str:
        if self.__state['keyword_argument']:
            return Tokens.reindent_2 + data
        return Tokens.reindent + data

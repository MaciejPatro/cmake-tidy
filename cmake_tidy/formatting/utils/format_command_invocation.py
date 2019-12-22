from cmake_tidy.formatting.utils.tokens import Tokens


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

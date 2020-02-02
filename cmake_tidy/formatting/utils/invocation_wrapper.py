import re


class InvocationWrapper:
    __newline_pattern = re.compile(r'\A\s\s+\Z')

    def wrap(self, invocation: dict) -> dict:
        wrapped_invoke = self.__prepare_wrapped_invocation(invocation)
        wrapped_invoke['arguments'] = [e if not self.__newline_pattern.match(e) else ' ' for e in
                                       wrapped_invoke['arguments']]
        return wrapped_invoke

    def __prepare_wrapped_invocation(self, invocation: dict) -> dict:
        new_invoke = invocation.copy()
        if self.__newline_pattern.match(new_invoke['arguments'][0]):
            new_invoke['arguments'] = new_invoke['arguments'][1:]
        return new_invoke

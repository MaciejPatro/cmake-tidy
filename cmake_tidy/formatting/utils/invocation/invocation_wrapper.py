###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


from cmake_tidy.formatting.utils.tokens import Tokens


class InvocationWrapper:
    def wrap(self, invocation: dict) -> dict:
        wrapped_invoke = self.__prepare_wrapped_invocation(invocation)
        wrapped_invoke['arguments'] = [e if not Tokens.is_spacing_token(e) else ' ' for e in
                                       wrapped_invoke['arguments']]
        return wrapped_invoke

    @staticmethod
    def __prepare_wrapped_invocation(invocation: dict) -> dict:
        new_invoke = invocation.copy()
        if Tokens.is_spacing_token(new_invoke['arguments'][0]):
            new_invoke['arguments'] = new_invoke['arguments'][1:]
        if Tokens.is_spacing_token(new_invoke['arguments'][-1]):
            new_invoke['arguments'] = new_invoke['arguments'][:-1]
        return new_invoke

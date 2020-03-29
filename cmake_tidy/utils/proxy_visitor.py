###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


class ProxyVisitor:
    def __init__(self, proxies: dict):
        self.__proxies = proxies

    def visit(self, name: str, values=None):
        if name in self.__proxies:
            return self.__proxies[name](values)

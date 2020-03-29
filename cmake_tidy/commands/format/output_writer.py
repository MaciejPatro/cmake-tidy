###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


from cmake_tidy.commands.format import FormatConfiguration


class OutputWriter:
    def __init__(self, configuration: FormatConfiguration):
        self.__config = configuration

    def write(self, data: str) -> None:
        if self.__config.inplace:
            with self.__config.file.open('w') as file:
                file.write(data)
        else:
            print(data)

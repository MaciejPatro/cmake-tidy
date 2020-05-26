###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


from pathlib import Path

from cmake_tidy.commands.format import FormatConfiguration


class WriterError(Exception):
    pass


def write_to_file(file: Path, data: str):
    with file.open('w') as file:
        file.write(data)


class OutputWriter:
    def __init__(self, configuration: FormatConfiguration):
        self.__config = configuration

    def write(self, data: str) -> None:
        if self.__config.inplace:
            self.__try_writing_to_file(data)
        else:
            print(data)

    def __try_writing_to_file(self, data: str) -> None:
        try:
            write_to_file(self.__config.file, data)
        except PermissionError:
            raise WriterError(f'File {self.__config.file} is read-only!')

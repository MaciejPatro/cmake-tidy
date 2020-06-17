###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


from cmake_tidy.lexical_data import KeywordVerifier
from cmake_tidy.utils import ExitCodes

VERSION = '0.5.0'


def show_version() -> int:
    print(f'cmake-tidy: {VERSION} | supported CMake: {KeywordVerifier(dict()).get_cmake_properties_version()}')
    return ExitCodes.SUCCESS

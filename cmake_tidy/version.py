from cmake_tidy.lexical_data import KeywordVerifier

VERSION = '0.4.0'


def show_version():
    print(f'cmake-tidy: {VERSION} | supported CMake: {KeywordVerifier(dict()).get_cmake_properties_version()}')

###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


def input_data(parser):
    parser.add_argument('input',
                        type=str,
                        nargs='?',
                        help='CMake file to be formatted')


def dump_config(parser):
    parser.add_argument('--dump-config',
                        action='store_true',
                        help='dump to stdout current settings. Script tries to read settings from `.cmake-tidy.json` '
                             'file existing in a current directory or provides default settings.')


def inplace(parser):
    parser.add_argument('-i', '--inplace',
                        action='store_true',
                        help='inplace edit specified <input_data> file')

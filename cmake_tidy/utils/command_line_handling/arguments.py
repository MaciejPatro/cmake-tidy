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
                        help='Dump to stdout current settings. Script tries to read settings from `.cmake-tidy.json` '
                             'or provides default settings. Precedence of searching `.cmake-tidy.json` is described '
                             'on github')


def inplace(parser):
    parser.add_argument('-i', '--inplace',
                        action='store_true',
                        help='Inplace edit specified <input_data> file')


def diff(parser):
    parser.add_argument('--diff',
                        action='store_true',
                        help='Print to stdout unified diff between original file and formatted version.')


def verbose(parser):
    parser.add_argument('--verbose',
                        action='store_true',
                        help='Print to stdout information about formatted file')

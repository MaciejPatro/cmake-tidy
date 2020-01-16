def input_data(parser):
    parser.add_argument('input',
                        type=str,
                        nargs='?',
                        help='CMake file to be formatted')


def dump_config(parser):
    parser.add_argument('--dump-config',
                        action='store_true',
                        help='dump configuration to stdout and exit')

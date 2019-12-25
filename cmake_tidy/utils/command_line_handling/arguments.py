def input_data(parser):
    parser.add_argument('input',
                        type=str,
                        nargs='?',
                        help='CMake file to be formatted')

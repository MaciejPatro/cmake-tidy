def input_data(parser):
    parser.add_argument('input',
                        type=str,
                        nargs='?',
                        help='CMake file to be formatted')


def dry_run(parser):
    parser.add_argument('-n', '--dry-run',
                        action='store_true',
                        help='disables execution of formatting of the file')

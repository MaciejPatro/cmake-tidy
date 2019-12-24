import argparse


def input_data(parser):
    parser.add_argument('input',
                        type=argparse.FileType('r'),
                        help='CMake file to be formatted')

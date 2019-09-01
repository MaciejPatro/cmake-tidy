import argparse


def input(parser):
    parser.add_argument('input',
                        type=argparse.FileType('r'),
                        help='CMake file to be formatted')

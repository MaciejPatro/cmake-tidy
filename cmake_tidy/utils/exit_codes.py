###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


from enum import IntEnum, unique


@unique
class ExitCodes(IntEnum):
    SUCCESS = 0
    FAILURE = -1

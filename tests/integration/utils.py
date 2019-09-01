from cmake_tidy.__main__ import main


def execute_cmake_tidy(command: str, arguments: list):
    try:
        main([command] + arguments)
    except SystemExit:
        pass


def normalize(data: str) -> str:
    return data.replace('\r', '')

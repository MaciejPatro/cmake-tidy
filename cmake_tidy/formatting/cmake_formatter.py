class CMakeFormatter:
    @staticmethod
    def format(text: str) -> str:
        return text


class FormatUnhandled:
    def register(self, dictionary: dict):
        dictionary['unhandled'] = self.format

    @staticmethod
    def format(data: str) -> str:
        return data

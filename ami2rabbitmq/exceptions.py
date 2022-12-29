class InvalidEvent(Exception):

    def __init__(self, message):
        self.message = message


class InvalidKey(Exception):

    def __init__(self, message):
        self.message = message
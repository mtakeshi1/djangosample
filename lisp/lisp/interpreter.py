def evaluate(source):
    return ''

class LispError(Exception):
    def __init__(self, message):
        self.message = message


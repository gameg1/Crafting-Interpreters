from Token import *
from TokenType import TokenType

class RuntimeError_(RuntimeError):
    def __init__(self, token, message):
        super().__init__(message)
        self.token = token
        self.message = message
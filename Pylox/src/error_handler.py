import sys

from Token import Token
from TokenType import TokenType


class RuntimeErr(RuntimeError):
    def __init__(self, *args, token: Token) -> None:
        super().__init__(*args)
        self.token = token

class ErrorHandler:
    def __init__(self):
        self.had_error = False
        self.had_runtime_error = False

    @classmethod
    def error(self, token = None, message = ""):
        if isinstance(token, Token):
            if token.type == TokenType.EOF:
                self.report(token.line, "", message)
            else:

                self.report(line= token.line, where=" at '" + token.lexeme + "'", message=message)
        else:
            self.report(token, "", message)
    @classmethod
    def runtime_error(self, error):
        print(f"[Line {error.token.line}] --> {error.message}")
        self.had_error = True
        self.had_runtime_error = True
    @classmethod
    def report(self, line, where, message):
        print(f"Line {line} | Error {where}: {message}", file=sys.stderr)
        self.had_error = True
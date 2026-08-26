import sys
from Token import Token

from TokenType import TokenType

class ParserError(RuntimeError):
    pass

class Return(RuntimeError):
    def __init__(self, value: object | None):
        self.value: object| None = value

class RuntimeErr(RuntimeError):
    def __init__(self, *args: object, token: Token) -> None:
        super().__init__(*args)
        self.token = token

class ErrorHandler:
    has_error = False
    had_runtime_error = False

    @classmethod
    def error(self, where:int| Token, message:str) -> None:
        if isinstance(where, Token):
            if where.type == TokenType.EOF:
                self.report(where.line, "", message)
            else:
                self.report(where.line, f" at '{where.lexeme}'", message)
        else:
            self.report(where, "", message)
    @classmethod
    def runtime_error(self, error: RuntimeErr):
        print(f"[Line {error.token.line}] --> {error.args[0]}")
        self.has_error = True
        self.had_runtime_error = True
    @classmethod
    def report(self, line:int, where:str, message:str):
        print(f"Line {line} | Error {where}: {message}", file=sys.stderr)
        self.has_error = True
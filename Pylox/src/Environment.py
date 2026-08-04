from Token import Token
from error_handler import RuntimeErr

class Environment:
    def __init__(self) -> None:
        self.values: dict[str,object] = {}

    def define(self, name:str, value:object) -> None:
        self.values[name] = value

    def get(self, name:Token) -> object:
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        raise RuntimeErr("Underfined variable '" + name.lexeme + "'.", name)
    
    def assign(self, name: Token, value: object) -> None:
        if  name.lexeme in self.values:
            self.values[name.lexeme] = value
            return

        raise RuntimeErr(name, "Undefined variable '" + name.lexeme + "'.")
from Token import Token
from error_handler import RuntimeErr

class Environment:
    def __init__(self, enclosing: "Environment | None" = None) -> None:
        self.enclosing: Environment | None = enclosing
        self.values: dict[str,object] = {}

    def define(self, name:str, value:object) -> None:
        self.values[name] = value

    def get(self, name:Token) -> object:
        if name.lexeme in self.values:
            return self.values[name.lexeme]

        if (self.enclosing != None):
            return self.enclosing.get(name)
        raise RuntimeErr("Underfined variable '" + name.lexeme + "'.", name)
    
    def assign(self, name: Token, value: object) -> None:
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return

        if (self.enclosing != None):
            self.enclosing.assign(name, value)
            return
        
        raise RuntimeErr(name, "Undefined variable '" + name.lexeme + "'.")
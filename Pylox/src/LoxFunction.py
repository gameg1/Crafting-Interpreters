from typing import TYPE_CHECKING


from Environment import Environment
from error_handler import Return
from loxCallable import loxCallable

if TYPE_CHECKING:
    from interpreter import Interpreter
    import Stmt

class LoxFunction(loxCallable):
    def __init__(self, declaration: "Stmt.Function"):
        self.declaration:Stmt.Function = declaration

    def call(self, interpreter: "Interpreter", arguments:list[object]) -> object:
        environment:Environment = Environment(interpreter.environment)
        # for i in range(len(self.declaration.parms)):
        #     environment.define(self.declaration.parms[i].lexeme,
        #                        arguments[i])
        for param, arg in zip(self.declaration.parms, arguments):
            environment.define(param.lexeme, arg)
            
        try:
            interpreter.executeBlock(self.declaration.body, environment)
        # Catch any return values from a return token
        except Return as e:
            return e.value
        
        return None

    def arity(self):
        return len(self.declaration.parms)

    def toString(self):
        return "<fn " + self.declaration.name.lexeme + ">"
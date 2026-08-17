from typing import TYPE_CHECKING

from Environment import Environment
from loxCallable import loxCallable

if TYPE_CHECKING:
    from interpreter import Interpreter
    import Stmt

class LoxFunction(loxCallable):
    def __init__(self, declaration: "Stmt.Function"):
        self.declaration:Stmt.Function = declaration

    def call(self, interpreter: "Interpreter", arguments:list[object]) -> object:
        environment:Environment = Environment(interpreter.global_env)
        for i in range(len(self.declaration.parms)):
            environment.define(self.declaration.parms[i].lexeme,
                               arguments[i])

        interpreter.executeBlock(self.declaration.body, environment)
        return None

    def arity(self):
        return len(self.declaration.parms)

    def toString(self):
        return "<fn " + self.declaration.name.lexeme + ">"
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from Expr import Expr
from Token import Token

V = TypeVar("V")


class Visitor(ABC, Generic[V]):
    @abstractmethod
    def visit_block_stmt(self, stmt: "Block") -> V: ...
    @abstractmethod
    def visit_expression_stmt(self, stmt: "Expression") -> V: ...
    @abstractmethod
    def visit_print_stmt(self, stmt: "print") -> V: ...

class Stmt(ABC):
    @abstractmethod
    def accept(self, visitor:Visitor[V])-> V:...

class Expression(Stmt):
    def __init__(self, expression: Expr):
        self.expression: Expr = expression

    def accept(self, visitor: Visitor):
        return visitor.visit_expression_stmt(self)

class Block(Stmt):
    def __init__(self, statements: list[Stmt]):
        self.statements: list[Stmt] = statements

    def accept(self, visitor: Visitor):
        return visitor.visit_block_stmt(self)

class Print(Stmt):
    def __init__(self, expression: Expr):
        self.expression: Expr = expression

    def accept(self, visitor: Visitor):
        return visitor.visit_print_stmt(self)

class Var(Stmt):
    def __init__(self, name: Token, initializer:Expr):
        self.name: Token = name
        self.initializer:Expr = initializer

    def accept(self, visitor: Visitor):
        return visitor.visit_var_stmt(self)
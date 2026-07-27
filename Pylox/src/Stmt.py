from abc import ABC, abstractmethod
from Token import Token
from typing import Generic, TypeVar

V = TypeVar("V")


class Visitor(ABC, Generic[V]):
    @abstractmethod
    def visit_expression_stmt(self, stmt: "Expression") -> V: ...
    @abstractmethod
    def visit_print_stmt(self, stmt: "print") -> V: ...


class Expression(Stmt):
    def __init__(self, expression: Expr):
        self.expression: Expr = expression

    def accept(self, visitor: Visitor):
        return visitor.visit_expression_stmt(self)


class print(Stmt):
    def __init__(self, expression: Expr):
        self.expression: Expr = expression

    def accept(self, visitor: Visitor):
        return visitor.visit_print_stmt(self)

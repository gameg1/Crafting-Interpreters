from Expr import *
from TokenType import TokenType


class AstPrinter(Visitor):
    def __init__(self):
        pass
    def print(self, item):
        return item.accept(self)
    
    def visit_binary_expr(self, expr) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)
    
    def visit_grouping_expr(self, expr) -> str:
        return self.parenthesize("group", expr.expression)
    
    def visit_literal_expr(self, expr) -> str:
        if (expr.value == None): return "nil"
        return str(expr.value)
    
    def visit_unary_expr(self, expr) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.right)
    
    def parenthesize(self, name, *exprs) -> str:
        res = f"({name}"
        for expr in exprs:
            res += f" {expr.accept(self)}"
        res += ")"
        return res
V = TypeVar("V")


class Visitor(ABC, Generic[V]):
    @abstractmethod
    def visit_expression | expression_stmt(self, stmt: " Expression | expression") -> V: ...
    @abstractmethod
    def visit_print      | expression_stmt(self, stmt: " print      | expression") -> V: ...
    @abstractmethod
    def visit_var        | name_stmt(self, stmt: " Var        | name") -> V: ...


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


class Var(Stmt):
    def __init__(self, name: Token, initializer: Expr):
        self.name: Token = name
        self.initializer: Expr = initializer

    def accept(self, visitor: Visitor):
        return visitor.visit_var_stmt(self)

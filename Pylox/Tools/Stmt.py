V = TypeVar("V")


class Visitor(ABC, Generic[V]):
    @abstractmethod
    def visit_block      | stattements_stmt(self, stmt: " Block      | stattements") -> V: ...
    @abstractmethod
    def visit_expression | expression_stmt(self, stmt: " Expression | expression") -> V: ...
    @abstractmethod
    def visit_if         | condition_stmt(self, stmt: " If         | condition") -> V: ...
    @abstractmethod
    def visit_print      | expression_stmt(self, stmt: " print      | expression") -> V: ...
    @abstractmethod
    def visit_var        | name_stmt(self, stmt: " Var        | name") -> V: ...
    @abstractmethod
    def visit_while      | condition_stmt(self, stmt: " While      | condition") -> V: ...


class Block(Stmt):
    def __init__(self, stattements: list[Stmt]):
        self.stattements: list[Stmt] = stattements

    def accept(self, visitor: Visitor):
        return visitor.visit_block_stmt(self)


class Expression(Stmt):
    def __init__(self, expression: Expr):
        self.expression: Expr = expression

    def accept(self, visitor: Visitor):
        return visitor.visit_expression_stmt(self)


class If(Stmt):
    def __init__(
        self, condition: Expr, thenBranch: Stmt,elseBranch: Stmt | None
    ):
        self.condition: Expr = condition
        self.thenBranch: Stmt,elseBranch: Stmt | None = thenBranch

    def accept(self, visitor: Visitor):
        return visitor.visit_if_stmt(self)


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


class While(Stmt):
    def __init__(self, condition: Expr, body: Stmt):
        self.condition: Expr = condition
        self.body: Stmt = body

    def accept(self, visitor: Visitor):
        return visitor.visit_while_stmt(self)

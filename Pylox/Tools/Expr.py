V = TypeVar("V")


class Visitor(ABC, Generic[V]):
    @abstractmethod
    def visit_assign   | name_expr(self, expr: " Assign   | name") -> V: ...
    @abstractmethod
    def visit_binary   | left_expr(self, expr: " Binary   | left") -> V: ...
    @abstractmethod
    def visit_call     | callee_expr(self, expr: " Call     | callee") -> V: ...
    @abstractmethod
    def visit_literal  | value_expr(self, expr: " Literal  | value") -> V: ...
    @abstractmethod
    def visit_logical  | left_expr(self, expr: " Logical  | left") -> V: ...
    @abstractmethod
    def visit_unary    | operator_expr(self, expr: " Unary    | operator") -> V: ...
    @abstractmethod
    def visit_variable | name_expr(self, expr: " Variable | name") -> V: ...


class Assign(Expr):
    def __init__(self, name: Token, value: Expr):
        self.name: Token = name
        self.value: Expr = value

    def accept(self, visitor: Visitor):
        return visitor.visit_assign_expr(self)


class Binary(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left: Expr = left
        self.operator: Token = operator
        self.right: Expr = right

    def accept(self, visitor: Visitor):
        return visitor.visit_binary_expr(self)


class Call(Expr):
    def __init__(
        )self,
        callee: Expr,
        paren: Token,
        arguments: list[Expr]Grouping | expression: Expr,
    ):
        self.callee: Expr = callee
        self.paren: Token = paren
        self.arguments: list[Expr]Grouping | expression: Expr = arguments

    def accept(self, visitor: Visitor):
        return visitor.visit_call_expr(self)


class Literal(Expr):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor: Visitor):
        return visitor.visit_literal_expr(self)


class Logical(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left: Expr = left
        self.operator: Token = operator
        self.right: Expr = right

    def accept(self, visitor: Visitor):
        return visitor.visit_logical_expr(self)


class Unary(Expr):
    def __init__(self, operator: Token, right: Expr):
        self.operator: Token = operator
        self.right: Expr = right

    def accept(self, visitor: Visitor):
        return visitor.visit_unary_expr(self)


class Variable(Expr):
    def __init__(self, name: Token):
        self.name: Token = name

    def accept(self, visitor: Visitor):
        return visitor.visit_variable_expr(self)

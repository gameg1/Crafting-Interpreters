import Expr
import Stmt
import time
from TokenType import TokenType
from loxCallable import loxCallable
from LoxFunction import LoxFunction
from error_handler import ErrorHandler, RuntimeErr,Return
from Token import Token
from Environment import Environment


class Clock(loxCallable):
    def arity(self) -> int:
        return 0
    def call(self, interpreter:"Interpreter", args:list):
        return time.time()
    def __str__(self) -> str:
        return "<native clock function>"

class Interpreter(Expr.Visitor, Stmt.Visitor):
    global_env:Environment = Environment()

    def __init__(self):
        self.environment:Environment = self.global_env

    def interpret(self, statements:list[Stmt.Stmt]) -> None:
        try:
            for statement in statements:
                self._execute(statement)
        except RuntimeErr as error:
            ErrorHandler.runtime_error(error)

    def visit_literal_expr(self, expr: Expr.Literal) -> object:
        return expr.value

    def visit_logical_expr(self, expr:Expr.Logical):
        left:object = self._evaluate(expr.left)

        if (expr.operator.type == TokenType.OR):
            if (self._isTruthy(left)):
                return left
            return self._evaluate(expr.right)
        if expr.operator.type == TokenType.AND:
            if (not self._isTruthy(left)):
                return left
            return self._evaluate(expr.right)
        
    def visit_grouping_expr(self, expr: Expr.Grouping) -> object:
        return self._evaluate(expr.expression)
    
    def visit_unary_expr(self, expr: Expr.Unary) -> object:
        right:object = self._evaluate(expr.right)

        match (expr.operator.type):
            case TokenType.MINUS:
                self._checkNumberOperand(expr.operator, right)
                return -(right)
            case TokenType.BANG:
                return not self.isTruthy(right)
        
        return None

    def visit_variable_expr(self, expr:Expr.Variable) -> object:
        return self.environment.get(expr.name)
    
    def visit_binary_expr(self, expr:Expr.Binary) -> object:
        left: object = self._evaluate(expr.left)
        right: object = self._evaluate(expr.right)

        match (expr.operator.type):
            case TokenType.MINUS:
                self._checkNumberOperands(expr.operator, left, right)
                return float(left) - float(right)
            case TokenType.PLUS:
                if (isinstance(left, float) and isinstance(right, float)):
                    return float(left) + float(right)
                if (isinstance(left, str) and isinstance(right, str)):
                    return str(left) + str(right)
                raise RuntimeErr(expr.operator, "Operands must be two number or two strings.")
            case TokenType.SLASH:
                self._checkNumberOperands(expr.operator, left, right)
                return float(left) / float(right)
            case TokenType.STAR:
                self._checkNumberOperands(expr.operator, left, right)
                return float(left) * float(right)
            case TokenType.GREATER:
                self._checkNumberOperands(expr.operator, left, right)
                return float(left) > float(right)
            case TokenType.GREATER_EQUAL:
                self._checkNumberOperands(expr.operator, left, right)
                return float(left) >= float(right)
            case TokenType.LESS:
                self._checkNumberOperands(expr.operator, left, right)
                return float(left) < float(right)
            case TokenType.LESS_EQUAL:
                self._checkNumberOperands(expr.operator, left, right)
                return float(left) <= float(right)
            case TokenType.BANG_EQUAL:
                return left != right
            case TokenType.EQUAL_EQUAL:
                return left == right
            
        return None
    
    def visit_call_expr(self, expr:Expr.Call):
        callee:object = self._evaluate(expr.callee)

        arguments:list[object] = []
        for argument in expr.arguments:
            arguments.append(self._evaluate(argument))

        if len(arguments) != callee.arity():
            raise RuntimeErr(expr.paren, f"Expected {callee.arity()} arguments but got {len(arguments)}.")

        # if (not (isinstance(callee,loxCallable))):
        #     raise RuntimeErr(expr.paren, "Can only call functions and classes.")

        try:
            return callee.call(self, arguments)
        except Exception as e:
            # print (e)
            raise RuntimeErr(e.args[0], token=expr.paren)
        
    def _evaluate(self, expr: Expr) -> object:
        return expr.accept(self)

    def _execute(self, stmt:Stmt.Stmt) -> None:
        stmt.accept(self)

    def executeBlock(self, statements:list[Stmt.Stmt], environment:Environment) -> None:
        previous:Environment = self.environment
        try:
            self.environment = environment
            for statement in statements:
                self._execute(statement)
        finally:
            self.environment = previous

    def visit_block_stmt(self, stmt:Stmt.Block) -> None:
        self.executeBlock(stmt.statements, Environment(self.environment))
        return None

    def visit_expression_stmt(self, stmt: Stmt.Expression) -> None:
        self._evaluate(stmt.expression)
        return None

    def visit_function_stmt(self, stmt: Stmt.Function) -> None:
        function: LoxFunction = LoxFunction(stmt)
        self.environment.define(stmt.name.lexeme, function)
        return None

    def visit_if_stmt(self, stmt: Stmt.If) -> None:
        if self._isTruthy(self._evaluate(stmt.condition)):
            self._execute(stmt.thenBranch)
        elif(stmt.elseBranch != None):
            self._execute(stmt.elseBranch)
        return None

    def visit_print_stmt(self, stmt: Stmt.Print):
        value: object = self._evaluate(stmt.expression)
        print(self._stringify(value))
        return None

    def visit_return_stmt(self, stmt:Stmt.Return):
        value: object = None
        if stmt.value is not None:
            value = self._evaluate(stmt.value)
        # Uses an exception to return the value of the function to the previous envioment/function
        raise Return(value)

    def visit_var_stmt(self, stmt:Stmt.Var) -> None:
        value:object = None
        if (stmt.initializer !=None):
            value = self._evaluate(stmt.initializer)

        self.environment.define(stmt.name.lexeme, value)
        return None

    def visit_while_stmt(self, stmt:Stmt.While):
        while (self._isTruthy(self._evaluate(stmt.condition))):
            self._execute(stmt.body)
        return None

    def visit_assign_expr(self, expr:Expr.Assign):
        value:object = self._evaluate(expr.value)
        self.environment.assign(expr.name, value)
        return value
    

    def _isTruthy(self, Object:object) -> bool:
        return Object is not None and Object is not False
            

    def _stringify(self, object:object) ->str:
        if (object == None): return "nil"

        # if (isinstance(object, float)):
        #     text:str = str(object=object)
        #     if (text.endswith(".0")):
        #         text = text[:-2]
        #     return text

        if isinstance(object, float) and isinstance(object, int):
            return str(int(object))
        
        return str(object)
    
    def _checkNumberOperand(self, operator:Token, operand: object)-> None:
        if (isinstance(operand, float)):
            return
        raise RuntimeErr(operator, "Operand must be a number.")

    def _checkNumberOperands(self, operator:Token, left: object, right:object) -> None:
        if isinstance(left, float) and isinstance(right, float):
            return
        raise RuntimeErr(operator, "Operand must be a number.")
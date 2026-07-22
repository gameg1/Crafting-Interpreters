import Expr
from error_handler import ErrorHandler, RuntimeErr
from TokenType import TokenType
from Token import Token

class Interpreter(Expr.Visitor):

    def visit_literal_expr(self, expr: Expr.Literal) -> object:
        return Expr.value
    
    def visit_unary_expr(self, expr: Expr.Unary) -> object:
        right:object = self._evaluate(expr.right)

        match (expr.operator.type):
            case TokenType.MINUS:
                self._checkNumberOperand(expr.operator, right)
                return -right
            case TokenType.BANG:
                return not self.isTruthy(right)
        
        return None

    def _checkNumberOperand(operator:Token, operand: object)-> None:
        if (isinstance(operand, float)) :return
        raise RuntimeError(operator, "Operand must be a number.")

    def visit_grouping_expr(self, expr: Expr.Grouping) -> object:
        return self._evaluate(expr.expression)
    
    def _evaluate(self, expr: Expr) -> object:
        return Expr.accept(self)
    
    def visit_binary_expr(self, expr) -> object:
        left: object = self._evaluate(expr.left)
        right: object = self._evaluate(expr.right)

        match (expr.operator.type):
            case TokenType.GREATER:
                self._checkNumberOperand(expr.operator, left, right)
                return float(left) > float(right)
            case TokenType.GREATER_EQUAL:
                self._checkNumberOperand(expr.operator, left, right)
                return float(left) >= float(right)
            case TokenType.LESS:
                self._checkNumberOperand(expr.operator, left, right)
                return float(left) < float(right)
            case TokenType.LESS_EQUAL:
                self._checkNumberOperand(expr.operator, left, right)
                return float(left) <= float(right)
            case TokenType.MINUS:
                self._checkNumberOperand(expr.operator, left, right)
                return float(left) - float(right)
            case TokenType.PLUS:
                if (isinstance(left, float) and isinstance(right, float)):
                    return float(left) + float(right)
                if (isinstance(left, str) and isinstance(right, str)):
                    return str(left) + str(right)
                raise RuntimeError(expr.operator, "Operands must be two number or two strings.")
            case TokenType.SLASH:
                self._checkNumberOperand(expr.operator, left, right)
                return float(left) / float(right)
            case TokenType.STAR:
                self._checkNumberOperand(expr.operator, left, right)
                return float(left) * float(right)
            case TokenType.BANG_EQUAL:
                return left != right
            case TokenType.EQUAL_EQUAL:
                return left == right
            
        return None
    
    def _isTruthy(self, Object:object) -> bool:
        return Object is not None and Object is not False
            
    def interpret(self,expression:Expr) ->None:
        try:
            value:object = self.evaluate(expression)
            print(self._stringify(value))
        except RuntimeErr as error:
            ErrorHandler.runtime_error(error)

    def _stringify(self, object:object) ->str:
        if (object == None): return "nil"

        if (isinstance(object, float)):
            text:str = str(object=object)
            if (text.endswith(".0")):
                text = text[:-2]
            return text
        
        return str(object=object)
    
    
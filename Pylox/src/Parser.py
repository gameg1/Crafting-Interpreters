from TokenType import TokenType
from Token import *
import Expr
import Stmt
from error_handler import *

class ParserError(Exception):
    pass

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self._current = 0
    
    def parse(self) -> list[Stmt.Stmt]:
        statements:list[Stmt.Stmt] = []
        while (not self._isAtEnd()):
            statements.append(self._declaration())
        return statements

    def expression(self)-> Expr:
        return self._assignment()

    def _declaration(self) -> Stmt:
        try:
            if self._match([TokenType.VAR]): return self._varDeclaration()
            return self._statement()
        except ParserError:
            self.synchronize()
            return None
    def _statement(self) -> Stmt:
        if self._match([TokenType.PRINT]): return self._printStatement()

        return self._expressionStatement()

    def _printStatement(self) -> Stmt:
        value: Expr = self.expression()
        self._consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Stmt.Print(value)

    def _varDeclaration(self):
        name:Token = self._consume(TokenType.IDENTIFIER, "Expect variable name.")

        initializer:Expr = None
        if self._match([TokenType.EQUAL]): initializer = self.expression()

        self._consume(TokenType.SEMICOLON, "Expect ';' after variable declaration.")
        return Stmt.Var(name, initializer)

    def _expressionStatement(self) -> Stmt:
        expr:Expr = self.expression()
        self._consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        return Stmt.Expression(expr)

    def _assignment(self):
        expr:Expr = self.equality()

        if (self._match([TokenType.EQUAL])):
            equals: Token = self.previous()
            value: Expr = self._assignment()

            if isinstance(expr,Expr.Variable):
                name:Token = expr.Assign(expr.name, value)
                return Expr.Assign(name, value)
            self.error(equals, "Invalid assignment target.")

        return expr
    
    def equality(self)-> Expr:
        expr:Expr = self.comparison()
        while (self._match([TokenType.BANG_EQUAL,TokenType.EQUAL_EQUAL])):
            operator:Token = self.previous()
            right:Expr = self.comparison()
            expr = Expr.Binary(expr, operator=operator,right=right)
        
        return expr
    
    def comparison(self)->Expr:
        expr:Expr = self.term()

        while (self._match([TokenType.GREATER,TokenType.GREATER_EQUAL,TokenType.LESS,TokenType.LESS_EQUAL])):
            operator:Token = self.previous()
            right:Expr = self.term()
            expr = Expr.Binary(expr, operator=operator, right=right)
        
        return expr
    
    def term(self) -> Expr:
        expr:Expr = self.factor()

        while (self._match([TokenType.MINUS,TokenType.PLUS])):
            opertator:Token = self.previous()
            right:Expr = self.factor()
            expr = Expr.Binary(expr, operator=opertator, right=right)
        
        return expr
    
    def factor(self) -> Expr:
        expr:Expr = self.unary()

        while (self._match([TokenType.SLASH,TokenType.STAR])):
            operator:Token = self.previous()
            right: Expr = self.unary()
            expr = Expr.Binary(expr, operator=operator, right=right)
        
        return expr
    
    def unary(self) -> Expr:
        if(self._match([TokenType.BANG,TokenType.MINUS])):
            operator:Token = self.previous()
            right: Expr = self.unary()
            return Expr.Unary(operator=operator, right=right)
        
        return self.primary()
    
    def primary(self) -> Expr:
        if (self._match([TokenType.FALSE])): return Expr.Literal(False)
        if (self._match([TokenType.TRUE])): return Expr.Literal(True)
        if (self._match([TokenType.NIL])): return Expr.Literal(None)

        if (self._match([TokenType.NUMBER,TokenType.STRING])):
            return Expr.Literal(self.previous().literal)
        if (self._match([TokenType.IDENTIFIER])):
            return Expr.Variable(self.previous())
        if (self._match([TokenType.LEFT_PAREN])):
            expr:Expr = self.expression()
            self._consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Expr.Grouping(expr)
        
        #raise self.error(self.peek(), "Expect expression.")
        ErrorHandler.error(self.peek(),"Expect expression.")


    def _match(self, types:list[TokenType]):
        for type in types:
            if self._check(type):
                self._advance()
                return True
        return False
    
    def _consume(self, type:TokenType, message:str)->Token:
        if(self._check(type=type)): return self._advance()

        raise self.error(self.peek(), message)
    

    def _check(self, type:TokenType)-> bool:
        if (self._isAtEnd()): return False
        return self.peek().type == type

    def _advance(self)->Token:
        if(not self._isAtEnd()): self._current += 1
        return self.previous()
    
    def _isAtEnd(self):
        return self.peek().type == TokenType.EOF
    
    def peek(self):
        return self.tokens[self._current]
    
    def previous(self):
        return self.tokens[self._current - 1]
    
    def error(self, token:Token, message:str):
        ErrorHandler.error(token, message)
        return ParserError()
    
    def synchronize(self)-> None:
        self._advance()

        while(not self._isAtEnd()):
            if (self.previous().type == TokenType.SEMICOLON): return

            match (self.peek().type):
                case TokenType.CLASS: return
                case TokenType.FUN: return
                case TokenType.VAR: return
                case TokenType.FOR: return
                case TokenType.IF: return
                case TokenType.WHILE: return
                case TokenType.PRINT: return
                case TokenType.RETURN: return
            self._advance()
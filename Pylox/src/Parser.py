from TokenType import TokenType
from Token import *
from Expr import *
from error_handler import *

class ParserError(Exception):
    pass

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self._current = 0
    
    def parse(self):
        try:
            return self.expression()
        except ParserError:
            return None
            

    def expression(self)-> Expr:
        return self.equality()
    
    def equality(self)-> Expr:
        expr:Expr = self.comparison()
        while (self._match([TokenType.BANG_EQUAL,TokenType.EQUAL_EQUAL])):
            operator:Token = self.previous()
            right:Expr = self.comparison()
            expr = Binary(expr, operator=operator,right=right)
        
        return expr
    
    def comparison(self)->Expr:
        expr:Expr = self.term()

        while (self._match([TokenType.GREATER,TokenType.GREATER_EQUAL,TokenType.LESS,TokenType.LESS_EQUAL])):
            operator:Token = self.previous()
            right:Expr = self.term()
            expr = Binary(expr, operator=operator, right=right)
        
        return expr
    
    def term(self) -> Expr:
        expr:Expr = self.factor()

        while (self._match([TokenType.MINUS,TokenType.PLUS])):
            opertator:Token = self.previous()
            right:Expr = self.factor()
            expr = Binary(expr, operator=opertator, right=right)
        
        return expr
    
    def factor(self) -> Expr:
        expr:Expr = self.unary()

        while (self._match([TokenType.SLASH,TokenType.STAR])):
            operator:Token = self.previous()
            right: Expr = self.unary()
            expr = Binary(expr, operator=operator, right=right)
        
        return expr
    
    def unary(self) -> Expr:
        if(self._match([TokenType.BANG,TokenType.MINUS])):
            operator:Token = self.previous()
            right: Expr = self.unary()
            return Unary(operator=operator, right=right)
        
        return self.primary()
    
    def primary(self) -> Expr:
        if (self._match([TokenType.FALSE])): return Literal(False)
        if (self._match([TokenType.TRUE])): return Literal(True)
        if (self._match([TokenType.NIL])): return Literal(None)

        if (self._match([TokenType.NUMBER,TokenType.STRING])):
            return Literal(self.previous().literal)
        
        if (self._match(TokenType.LEFT_PAREN)):
            expr:Expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)
        
        raise self.error(self.peek(), "Expect expression.")


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
        ErrorHandler.error(ErrorHandler,token, message)
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
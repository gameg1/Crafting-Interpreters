from TokenType import TokenType
from Token import *
from Expr import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self._current = 0
    
    def expression(self)-> Expr:
        return self.equality()
    
    def equality(self)-> Expr:
        expr:Expr = self.comparison()
        while (self.match([TokenType.BANG_EQUAL,TokenType.EQUAL_EQUAL])):
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

        while (self.match(TokenType.SLASH,TokenType.STAR)):
            operator:Token = self.previous()
            right: Expr = self.unary()
            expr = Binary(expr, operator=operator, right=right)
        
        return expr
    
    def unary(self) -> Expr:
        if(self._match(TokenType.BANG,TokenType.MINUS)):
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


    def _match(self, types:list[TokenType]):
        for type in types:
            if self._check(type):
                self.advance()
                return True
        return False
    
    def _check(self, type:TokenType)-> bool:
        if (self._isAtEnd()): return False
        return self.peek().TokenType == type

    def _advance(self)->Token:
        if(not self._isAtEnd()): self._current += 1
        return self.previous()
    
    def _isAtEnd(self):
        return self.peek().TokenType == TokenType.EOF
    
    def peek(self):
        return self.tokens[self._current]
    
    def previous(self):
        return self.tokens[self._current - 1]
    
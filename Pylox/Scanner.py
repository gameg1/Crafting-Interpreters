from TokenType import TokenType
from Token import Token
from pylox import Lox

class Scanner:
    source:str
    tokens: list[Token] = list()

    _start = 0
    _current = 0
    _line = 1

    def __init__(self, source:str):
        self.source = source

    def scanTokens(self) -> list[Token]:
        while (not self._isAtEnd()):
               start = self._current
               self._scanToken()
        
        self.tokens.append(Token(TokenType.EOF, " ", None, self._line))
        return self.tokens
    #TODO: Change this if statement to a case statement
    def _scanToken(self)-> None:
        c:chr = self._advance()
        # Checking for single character tokens
        if c == "("   : self._addToken(TokenType.LEFT_PAREN)
        elif c == ")" : self._addToken(TokenType.RIGHT_PAREN)
        elif c == "{" : self._addToken(TokenType.LEFT_BRACE)
        elif c == "}" : self._addToken(TokenType.RIGHT_BRACE)
        elif c == "," : self._addToken(TokenType.COMMA)
        elif c == "." : self._addToken(TokenType.DOT)
        elif c == "-" : self._addToken(TokenType.MINUS)
        elif c == "+" : self._addToken(TokenType.PLUS)
        elif c == ";" : self._addToken(TokenType.SEMICOLON)
        elif c == "*" : self._addToken(TokenType.STAR)
        # Checking for 
        elif c == "!" : self._addToken(TokenType.BANG_EQUAL) if self._match('=') else self._addToken(TokenType.BANG)
        elif c == "=" : self._addToken(TokenType.EQUAL_EQUAL) if self._match('=') else self._addToken(TokenType.EQUAL)
        elif c == "<" : self._addToken(TokenType.LESS_EQUAL) if self._match('=') else self._addToken(TokenType.LESS)
        elif c == ">" : self._addToken(TokenType.GREATER_EQUAL) if self._match('=') else self._addToken(TokenType.GREATER)

        elif c == "/":
            if (self._match('/')):
                # A comment goes until the end of the line.
                while(self._peek() != '\n' and not self._isAtEnd()):
                    self._advance()
                else:
                    self._addToken(TokenType.SLASH)

        else:
            Lox.error(Lox,self._line, "Unexpected character.")
            
    def _match(self,expected:chr)->bool:
        if(self._isAtEnd()): return False
        if (self.source[self._current] != expected): return False

    def _peek(self) ->chr:
        if (self._isAtEnd()): return '\0'
        return self.source[self._current]

        self._current +=1
        return True

    def _isAtEnd(self):
        return self._current >= len(self.source)
    
    def _advance(self):
        self._current += 1
        self.source[self._current - 1]

    def _addToken(self, tokentype: TokenType, literal=None):
        text:str = self.source[self._start : self._current]
        self.tokens.append(Token(tokentype, text, literal, self._line))
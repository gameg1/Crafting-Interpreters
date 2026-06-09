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
        match c:
        
            case "("   : self._addToken(TokenType.LEFT_PAREN)
            case ")" : self._addToken(TokenType.RIGHT_PAREN)
            case "{" : self._addToken(TokenType.LEFT_BRACE)
            case "}" : self._addToken(TokenType.RIGHT_BRACE)
            case "," : self._addToken(TokenType.COMMA)
            case "." : self._addToken(TokenType.DOT)
            case "-" : self._addToken(TokenType.MINUS)
            case "+" : self._addToken(TokenType.PLUS)
            case ";" : self._addToken(TokenType.SEMICOLON)
            case "*" : self._addToken(TokenType.STAR)
        # Checking for 
            case "!" : self._addToken(TokenType.BANG_EQUAL) if self._match('=') else self._addToken(TokenType.BANG)
            case "=" : self._addToken(TokenType.EQUAL_EQUAL) if self._match('=') else self._addToken(TokenType.EQUAL)
            case "<" : self._addToken(TokenType.LESS_EQUAL) if self._match('=') else self._addToken(TokenType.LESS)
            case ">" : self._addToken(TokenType.GREATER_EQUAL) if self._match('=') else self._addToken(TokenType.GREATER)

            case "/":
                if (self._match('/')):
                    # A comment goes until the end of the line.
                    while(self._peek() != '\n' and not self._isAtEnd()):
                        self._advance()
                    else:
                        self._addToken(TokenType.SLASH)
            # Ignore Whitespace
            case ' ':  pass
            case '\r': pass
            case '\t': pass
            # newline
            case '\n': line += 1
            case '"': self._string()

            case _:
                if self._isDigit(c):
                    self._number()
                else:
                    Lox.error(Lox,self._line, "Unexpected character.")
    
    def _number(self):
        while (self._isDigit(self._peek)): self._advance()

        # Look for a fractional part.
        if (self._peek() == '.' and self._isDigit(self._peekNext())):
            # Comsume the "."
            self._advance()

            while (self._isDigit(self._peek())): self._advance()
        
        self._addToken(TokenType.NUMBER, float(self.source[self._start,self._current]))

    def _string(self) -> None:
        while (self._peek() != '"' and not self._isAtEnd()):
            if (self._peek() == '\n'):
                self._line += 1
            self._advance()
        
        if (self._isAtEnd()):
            Lox.error(self._line, "Unterminated string.")
            return
        
        self._advance()

        value:str = self.source[self._start + 1, self._current - 1]
        self._addToken(TokenType.STRING, value)


    def _match(self, expected:chr)->bool:
        if(self._isAtEnd()): return False
        if (self.source[self._current] != expected): return False

        self._current +=1
        return True
    
    def _peek(self) ->chr:
        if (self._isAtEnd()): return '\0'
        return self.source[self._current]

    def _peekNext(self) ->chr:
        if (self._current + 1 >= len(self.source)): return '\0'
        return self.source[self._current + 1]

    def _isDigit(self, c:chr):
        return c >= '0' and c <= '9'

    def _isAtEnd(self):
        return self._current >= len(self.source)
    
    def _advance(self):
        self._current += 1
        self.source[self._current - 1]

    def _addToken(self, tokentype: TokenType, literal=None):
        text:str = self.source[self._start : self._current]
        self.tokens.append(Token(tokentype, text, literal, self._line))
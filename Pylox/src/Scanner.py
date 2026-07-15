from TokenType import TokenType
from Token import Token
from error_handler import ErrorHandler

class Scanner:


    def __init__(self, source:str, error_handler):
        self.error_handler = error_handler

        self.source:str = source
        self.tokens: list[Token] = list()

        self._start:int = 0
        self._current:int = 0
        self._line:int = 1

        self.keywords = {
            "and":    TokenType.AND,
            "class":  TokenType.CLASS,
            "else":   TokenType.ELSE,
            "false":  TokenType.FALSE,
            "for":    TokenType.FOR,
            "fun":    TokenType.FUN,
            "if":     TokenType.IF,
            "nil":    TokenType.NIL,
            "or":     TokenType.OR,
            "print":  TokenType.PRINT,
            "return": TokenType.RETURN,
            "super":  TokenType.SUPER,
            "this":   TokenType.THIS,
            "true":   TokenType.TRUE,
            "var":    TokenType.VAR,
            "While":  TokenType.WHILE,
        }

    def scanTokens(self) -> list[Token]:
        while (not self._isAtEnd()):
               self._start = self._current
               self._scanToken()
        
        self.tokens.append(Token(TokenType.EOF, " ", None, self._line))
        return self.tokens
    

    def _scanToken(self)-> None:
        c:str = self._advance()
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
                if c.isdigit():
                    self._number()

                elif c.isalpha():
                    self._identifier()

                else:
                    self.error_handler(self._line, "Unexepected character.")
                return
    
    def _identifier(self)->None:
        while (self._isAlphaNumeric(self._peek())): self._advance()

        text:str = self.source[self._start: self._current]
        type:TokenType = self.keywords.get(text)
        if type == None: type = TokenType.IDENTIFIER
        self._addToken(type)

    def _number(self):
        while (self._isDigit(self._peek())): self._advance()

        # Look for a fractional part.
        if (self._peek() == '.' and self._isDigit(self._peekNext())):
            # Comsume the "."
            self._advance()

            while (self._isDigit(self._peek())): self._advance()
        self._addToken(TokenType.NUMBER, float(self.source[self._start: self._current]))

    def _string(self) -> None:
        while (self._peek() != '"' and not self._isAtEnd()):
            if (self._peek() == '\n'):
                self._line += 1
            self._advance()
        
        if (self._isAtEnd()):
            self.error_handler.error(self._line, "Unterminated string.")
            return
        
        self._advance()

        value:str = self.source[self._start + 1: self._current - 1]
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
    
    def _isAlpha(self, c:chr)-> bool:
        return (str(c) >= 'a' and str(c) <= 'z') or \
               (str(c) >= 'A' and str(c) <= 'Z') or \
               str(c) == '_'
    
    def _isAlphaNumeric(self, c:chr) -> bool:
        return str(c).isalpha() or str(c).isdigit()

    def _isDigit(self, c:chr):
        return str(c) >= '0' and str(c) <= '9'

    def _isAtEnd(self):
        return self._current >= len(self.source)
    
    def _advance(self):
        self._current += 1
        return self.source[self._current - 1]

    def _addToken(self, tokentype: TokenType, literal=None):
        text:str = self.source[self._start : self._current]
        self.tokens.append(Token(tokentype, text, literal, self._line))
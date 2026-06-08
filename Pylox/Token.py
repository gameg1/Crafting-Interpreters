from TokenType import TokenType
class Token:
    def __init__(self, type:TokenType, lexeme:str, literal:object, line:int):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line
    
    def toString(self):
        return str(self.type + " " + self.lexeme + " " + self.literal)
    
    def __str__(self):
        return self.toString()
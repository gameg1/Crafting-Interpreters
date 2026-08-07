import sys
from Scanner import Scanner
from runtime_error import RuntimeError_
from error_handler import ErrorHandler
from Parser import *
from interpreter import Interpreter
from astPrinter import AstPrinter


class Lox:
    def __init__(self, interpreter: Interpreter) -> None:
        self.interpreter:Interpreter = interpreter
        self.error_handler = ErrorHandler()
        #self.ast_printer = AstPrinter()

    def run_file(self, path:str) -> None:
        file = open(path)
        self.run(file.read())
        if (self.error_handler.had_error):
            exit(65)
        if (self.error_handler.had_runtime_error):
            exit(70)

    def runPrompt(self) -> None:
        while True:
            line = input("pylox > ")
            if line == None or line == "exit()":
                break
            self.run(line)
            self.error_handler.had_error = False

    def run(self, source:str) -> None:
        # Gives a Scanner a source and an error handler
        scanner = Scanner(source, self.error_handler)
        # Scans the source char by char and returns a list of tokens
        tokens = scanner.scanTokens()
        # Takes the tokens and returns a tree data structure that contian various stmts and exprs
        parser: Parser = Parser(tokens=tokens)
        statements:list[Stmt.Stmt] = parser.parse()

        if (self.error_handler.had_error): sys.exit(65)
        if (self.error_handler.had_runtime_error): sys.exit(70)

        # Interpreates the statements
        self.interpreter.interpret(statements)
        
    
    def error(self, line:int, message:str) -> None:
        self.report(line, "", message)

    def runtimeError(self, error:RuntimeErr):
        print(error.args[0] + "\n[line " + error.token.line + "]") # Check to see if this works
        self.error_handler.had_runtime_error = True
    
    def report(self, line:int, where:str, message:str) -> None:
        print("[line " + str(line) +"] Error" + where + ": " + message)
        self.error_handler.had_error = True


if __name__ == '__main__':
    interpreter = Interpreter()
    lox = Lox(interpreter=interpreter)
    # Prints usage if no input
    if len(sys.argv) > 2:
        print("Usage: pylox [script]")
        exit(64)
    # Runs the file when given a path
    elif (len(sys.argv) == 2):
        lox.run_file(sys.argv[1])
    # Allows the user to run prompts in the cmd line.
    else:
        lox.runPrompt()

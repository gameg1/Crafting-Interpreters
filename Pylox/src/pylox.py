import sys
from Scanner import Scanner
from runtime_error import RuntimeError_
from error_handler import ErrorHandler
from Parser import *
from astPrinter import AstPrinter


class Lox:
    def __init__(self) -> None:
        self.error_handler = ErrorHandler()

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
            self.error_handler.had_error = True

    def run(self, source:str) -> None:
        scanner = Scanner(source, self.error_handler)
        tokens = scanner.scanTokens()
        parser: Parser = Parser(tokens=tokens)
        expression: Expr = parser.parse()

        if (self.error_handler.had_error): return

        print(AstPrinter.print(expression))
        
    
    def error(self, line:int, message:str) -> None:
        self.report(line, "", message)

    def report(self, line:int, where:str, message:str) -> None:
        print("[line " + str(line) +"] Error" + where + ": " + message)
        self.hadError = True


if __name__ == '__main__':
    lox = Lox()
    # Prints usage if no input
    if len(sys.argv) > 2:
        print("Usage: pylox [script]")
        exit(64)
    # Runs the file if given a path
    elif (len(sys.argv) == 2):
        lox.runFile(sys.argv[1])
    # runs the prompt
    else:
        lox.runPrompt()

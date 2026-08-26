import sys
from Parser import Parser

from error_handler import ErrorHandler
from Scanner import Scanner
from interpreter import Interpreter


class Lox:
    def __init__(self, interpreter: Interpreter) -> None:
        self.interpreter:Interpreter = interpreter
        #self.ast_printer = AstPrinter()

    def run_file(self, path:str) -> None:
        file = open(path)
        self.run(file.read())
        if (ErrorHandler.has_error):
            exit(65)
        if (ErrorHandler.had_runtime_error):
            exit(70)

    def runPrompt(self) -> None:
        while True:
            line = input("pylox > ")
            if line == None or line == "exit":
                break
            self.run(line)
            ErrorHandler.had_error = False

    def run(self, source:str) -> None:
        # Gives a Scanner a source and an error handler
        scanner = Scanner(source)
        # Scans the source char by char and returns a list of tokens
        tokens = scanner.scanTokens()
        # Takes the tokens and returns a tree data structure that contian various stmts and exprs
        parser: Parser = Parser(tokens=tokens)
        statements = parser.parse()

        if ErrorHandler.has_error:
            sys.exit(65)
        if ErrorHandler.had_runtime_error:
            sys.exit(70)

        # Interpreates the statements
        self.interpreter.interpret(statements)

if __name__ == '__main__':
    interpreter = Interpreter()
    lox = Lox(interpreter)
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

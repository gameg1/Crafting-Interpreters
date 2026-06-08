import sys
from Scanner import Scanner


class Lox:
    hadError:bool = False
    def __init__(self) -> None:
        pass

    def run_file(self, path:str) -> None:
        file = open(path)
        self.run(file.read())
        if (self.hadError):
            exit(65)

    def runPrompt(self) -> None:
        while True:
            line = input("pylox > ")
            if line == None or line == "exit()":
                break
            self.run(line)
            self.hadError = False

    def run(self, source:str) -> None:
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        for t in tokens:
            print(t)
    
    def error(self, line:int, message:str) -> None:
        self.report(line, "", message)

    def report(self, line:int, where:str, message:str) -> None:
        print("[line " + str(line) +"] Error" + where + ": " + message)
        self.hadError = True


if __name__ == '__main__':
    lox = Lox()
    # Prints usage if no input
    if len(sys.argv) < 2:
        print("Usage: pylox [script]")
        exit(64)
    # Runs the file if given a path
    elif (len(sys.argv) == 2):
        lox.runFile(sys.argv[1])
    # runs the prompt
    else:
        lox.runPrompt()

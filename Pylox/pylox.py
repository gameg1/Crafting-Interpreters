import sys



class Lox:
    def __init__(self) -> None:
        pass

    def run_file(self, path:str) -> None:
        file = open(path)
        self.run(file.read())

    def runPrompt(self) -> None:
        while True:
            line = input("pylox > ")
            if line == None or line == "exit()":
                break
            self.run(line)

    def run(self, source:str) -> None:
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        for t in tokens:
            print(t)

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

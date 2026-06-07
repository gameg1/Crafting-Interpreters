import argparse

parser = argparse.ArgumentParser(description="interprates the lox programming language")

parser.add_argument('input', nargs='+')
args = parser.parse_args()

def main():
    arg_inputs = args.input
    # Prints usage if no input
    if len(arg_inputs) < 1:
        print("Usage: pylox [script]")
        exit(64)
    # Runs the file if given a path
    elif (len(arg_inputs) == 1):
        runFile(arg_inputs[0])
    # runs the prompt
    else:
        runPrompt()

def runFile(path:str) -> None:
    with open(path) as file:
        run(file.read())

if __name__ == '__main__':
    main()
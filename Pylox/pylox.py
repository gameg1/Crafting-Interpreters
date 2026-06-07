import argparse

parser = argparse.ArgumentParser(description="interprates the lox programming language")

parser.add_argument('input', nargs='+')
args = parser.parse_args()

def main():
    arg_inputs = args.input
    if len(arg_inputs < 1):
        print("Usage: pylox [script]")
        exit(64)
    elif (len(arg_inputs) == 1):
        runFile(arg_inputs[0])
    else:
        runPrompt()



if __name__ == '__main__':
    main()
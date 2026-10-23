from .lexer import Lexer
from .parser import Parser
from .evaluator import run_program

def repl():
    env = {}
    print("Welcome to the Tau REPL! - type exit to quit :)")
    while True:
        try:
            line = input("tau> ")
        except (EOFError, KeyboardInterrupt):
            print ("\n Goodbye")
            break
        if line.strip() == "exit":
            print("Goodbye")
            break

        if line.strip() =="":
            continue

        try:
            tokens = Lexer(line).tokenize()
            ast = Parser(tokens).parse_program()
            result, env = run_program(ast, env)
            if result is not None:
                print(result)
        except Exception as e:
            print(f"Error: {e}")
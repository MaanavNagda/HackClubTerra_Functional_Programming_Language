import sys
from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import run_program
from src.repl import repl

if len(sys.argv) > 1:
    #file mode
    try:
        with open(sys.argv[1], 'r') as f:
            source = f.read()
        tokens = Lexer(source).tokenize()
        ast = Parser(tokens).parse_program()
        result, env = run_program(ast, {})
        if result is not None:
            print(result)
    except FileNotFoundError:
        print(f"File {sys.argv[1]} not found.")
    except Exception as e:
        print(f"Error: {e}")
else:
    #interactive mode
    repl()
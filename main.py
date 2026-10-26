import sys
from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import run_program
from src.repl import repl
#Entry point of the system
#Running this file gives the interactive REPL
#Running this file when pointing to another file runs that file
#Both files run the same pipeline, as a language doesn't care about where the source is from, it has to do the same things to it regardless

if len(sys.argv) > 1:
    #file mode, and it reads the whole file, runs it once, and prints the last value
    try:
        with open(sys.argv[1], 'r') as f:
            source = f.read()
        tokens = Lexer(source).tokenize()
        ast = Parser(tokens).parse_program()
        result, env = run_program(ast, {}) #This is a fresh env, and is discarded after use. The files don't need memory because the env is only relevant for that one program, and so doesn't need to be saved/stored.
        if result is not None: 
            print(result)
    except FileNotFoundError:
        print(f"File {sys.argv[1]} not found.") #This is a clean error message in case of a missing file
    except Exception as e:
        print(f"Error: {e}") #Language error prints 
else:
    #interactive mode, when no file is given,and instead the REPL is activated
    repl()
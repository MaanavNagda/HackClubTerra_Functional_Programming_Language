import sys
from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import run_program
from src.machine import run_program_machine
from src.repl import repl
#Entry point of the system
#Running this file gives the interactive REPL
#Running this file when pointing to another file runs that file
#Both files run the same pipeline, as a language doesn't care about where the source is from, it has to do the same things to it regardless



engine = "naive"
filename = None
i = 1
while i < len(sys.argv):
    if sys.argv[i] == "--engine":
        engine = sys.argv[i + 1]
        i = i + 2
    else:
        filename = sys.argv[i]
        i = i + 1

if filename:
    try:
        with open(filename, 'r') as f:
            source = f.read()
        ast = Parser(Lexer(source).tokenize()).parse_program()
        if engine == "machine":
            result, env = run_program_machine(ast,{})
        else:
            result, env = run_program(ast, {})
        if result is not None:
            print(result)
    except FileNotFoundError:
        print(f"File {filename} not found")
    except Exception as e:
        print(f"Error: {e}")
else:
    repl(engine)
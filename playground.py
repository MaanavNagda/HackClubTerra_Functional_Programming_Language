#This file is to make index.py cleaner, by removing the python embedded in the html/js into its own file, also making it easier to fix/find/solve errors, as well as making it overall clearner, by working in the same way as all the other imported files

import json
from src.lexer import Lexer
from src.parser import Parser
from src.machine import run_stepped, format_state, run_program_machine

def steps(src):
    try:
        ast = Parser(Lexer(src).tokenize()).parse_program()
        return json.dumps([format_state(s) for s in run_stepped(ast, {})])
    except Exception as e:
        return json.dumps([str(e)])

def run(src):
    try:
        ast = Parser(Lexer(src).tokenize()).parse_program()
        return str(run_program_machine(ast, {})[0])
    except Exception as e:
        return str(e)
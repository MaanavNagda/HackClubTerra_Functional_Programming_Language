from .lexer import Lexer
from .parser import Parser
from .evaluator import run_program
#This is an interactive shell: REPL
#R --> E --> P --> L = Read --> Evaluate --> Print --> Loop
#This doesn't have any logic about the tau language itself, but instead it connects the lexer, parser, and evaluator together in a loop, so that each input goes through all of the stages, and not just one of them

def repl():
    #env must persist across the lines of the REPL, so things like "let x = 14" survives for the next line input of x + 13
    env = {}
    print("Welcome to the Tau REPL! - type exit to quit :)")
    #Friendly greeting message
    while True:
        #This is the outer try, and it catches the USER's signals, like Ctrl D means an EOFError, or Ctrl C means its ia keyboard interrupt
        try:
            #interactive prompt line starter
            line = input("tau> ")
        except (EOFError, KeyboardInterrupt):
            #exit condition
            print ("\n Goodbye")
            break
        if line.strip() == "exit":
            #exit condition
            print("Goodbye")
            break
        #if none of the exit conditions are met, you simply continue, and as the while loop has no other exit conditions, this will loop on forevre
        if line.strip() =="":
            continue

        #The inner try catches language errors. This is things like incorrect syntax or logic, wchich may error out that one line, but will not error out that whole session. This is becasue a mistake is not an indication to close the REPL, and the user may still want/need to use the things stored in env, so the REPL should not be shut. This try prints out the error message, but still keeps the REPL alive
        try:
            tokens = Lexer(line).tokenize() #This converts the raw input string into tokens by running the lexer
            ast = Parser(tokens).parse_program() #This converts the tokens from the lexer into an AST by running the parser
            result, env = run_program(ast, env)  #This evaluates the tree by running the evaluator
            if result is not None: #If there is a result, it is outputted
                print(result)
        except Exception as e:
            print(f"Error: {e}")
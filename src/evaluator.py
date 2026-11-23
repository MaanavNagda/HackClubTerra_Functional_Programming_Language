from .ast_nodes import Number, Var, BinOp, Let, If, Bool, FnDef, Call, Lambda, Str, List, Checkpoint, Rewind
#Walks the AST that the parser produced, and then computes the values



#This is a runtime function value, and it captures the parameter, body, and environment when it is created
class closure():
    def __init__(self, param, body, env):
        self.param = param
        self.body = body
        self.env = env

#a builtin is a named primitive that is provided by the language itself. it is stored as a value in the starting env, not as a keyword, so it can be passed, stored, and shadowed like everything else.
#however like a keyword, its name is also reserved exclusively for it.

class Builtin():
    def __init__(self, name):
        self.name = name

class Effect():
    def __init__(self, name, args):
        self.name = name
        self.args = args

class Partial():
    #a builtin that has collected some but not all of its arguments
    #Map produces a partial of map and the function, as the function still waits for the lsit
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def step(self, arg):
        newArgs = self.args + (arg, )
        if len(newArgs) < BUILTIN_ARITY[self.name]:
            return Partial(self.name, newArgs)
        if self.name == "<map>":
            fn = newArgs[0]
            lst = newArgs[1]
            if not isinstance(lst, list):
                raise Exception(f"{self.name.strip("<>")} needs a list")
            result = []
            for x in lst:
                result.append(call_value(fn, x))
            return result
        elif self.name == "<filter>":
            fn = newArgs[0]
            lst = newArgs[1]
            if not isinstance(lst, list):
                raise Exception(f"{self.name.strip("<>")} needs a list")
            result = []
            for x in lst:
                if call_value(fn, x):
                    result.append(x)
            return result
    

BUILTIN_ARITY = {"<map>": 2,
                 "<filter>": 2,}


#This is the builtins that every program starts with:
BUILTINS = {"print": Builtin("print"),
            "dispatch!": Builtin("dispatch!"),
            "reroute!": Builtin("reroute!"),
             "page!": Builtin("page!"),
             "write!": Builtin("write!"),
             "commit!": Builtin("commit!"),
             "<dot>": Builtin("<dot>"),
             "<map>": Builtin("<map>"),
             "<filter>": Builtin("<filter>")
            }

#This runs the actual implementation of the builtin. It is shared with the machien so that both engines agree
def call_builtin(name, arg):
    if name == "print":
        print(arg)
        return arg #This returns the variable so that the pipelines keep flowing
    if name == "dispatch!" or name == "reroute!" or name == "page!" or name == "write!":
        return Effect(name, (arg,))
    if name == "commit!":
        if isinstance(arg, list):
            for each in arg:
                print(each.name, each.args)
        else:
            print(arg.name, arg.args)
        return arg
    if name == "<dot>":
        if isinstance(arg, closure) or isinstance(arg, Builtin) or isinstance(arg, list):
            return arg
        else:
            raise Exception("...")
    if name in BUILTIN_ARITY:
        return Partial(name, (arg,))
    else:
        raise Exception(f"unknown builtin {name}") #All builtins are defined above, and so if it doesn't match it, then an error is thrown


def call_value(func, arg):
    if isinstance(func, Builtin):
        return call_builtin(func.name, arg)
    if isinstance(func, Partial):
        return func.step(arg)
    if isinstance(func, closure):
        callEnv = {**func.env}
        callEnv[func.param] = arg
        return run_program(func.body, callEnv)[0]
    raise Exception(f"calling non-function")


#Moved from machine.py to evaluator.py to fix the circular dependecy crash that would have otherwise occurred when machine.py tried to call rpn.py (as rpn.py is calling stuff from machine.py as well)
#operator calculations
#shared with the evaluator so both engines agree on operator usage
def apply_op(op, left, right):
    if op == "/":
        if right == 0:
            raise Exception(f"division by {right} error")
        return left/right
    if op == "++":
        if isinstance(left, list):
            l = left
        else:
            l = [left]
        if isinstance(right, list):
            r = right
        else:
            r = [right]
        return l + r
    if op == "+":
        if isinstance(left, str) or isinstance(right, str):
            return str(left) + str(right)
        return left + right
    if op == "-":
        return left - right
    if op =="*":
        return left * right
    if op =="==":
        return left == right
    if op =="!=":
        return left != right
    if op=="<":
        return left < right
    if op ==">":
        return left > right
    if op == "<=":
        return left <= right
    if op == ">=":
        return left >= right
    raise Exception(f"unknown operator")


#evaluate() handles the expressions
#evaluates a single AST node -> a value
# env is a dictionary (name -> value) that holds all the current bindings
#Bin op evaluates its own subtrees, which is what makes it a recursive tree walk
def evaluate(node, env):
    #Evaluating a lambda creates a closure that captures the current environment
    if isinstance(node, Lambda):
        return closure(node.param, node.body, env)
    #Evaluates the function and argument, then runs the function body with that argument bound to its parameter 
    if isinstance(node, Call):
        func = evaluate(node.func, env)
        arg = evaluate(node.arg, env)
        return call_value(func, arg)
    if isinstance(node, Number):
        return node.value #literals evaluate to themselves
    if isinstance(node, Bool):
        return node.value #boolean literals also evaluate to themselves
    if isinstance(node, Str):
        return node.value
    if isinstance(node, List):
        return [evaluate(element, env) for element in node.elements]
    if isinstance(node, If):
        cond  = evaluate(node.cond,env) #evaluates the condition first
        if cond:
            return evaluate(node.then, env) #truthy, so the the then branch only
        elif node.else_branch is not None:
            return evaluate(node.else_branch, env) #falsy, so the else branch only (which may be a nested if branch)
        return None
    if isinstance(node, Var):
        if node.name in env:
            return env[node.name] #Looks up the binding from env
        else:
            raise Exception(f"undefined variable {node.name} at line {node.line}, col {node.col}")
            #Uses the nodes position to point at the source
    if isinstance(node, BinOp):
        left = evaluate(node.left, env) #evaluates both sides first
        right = evaluate(node.right, env) #then applies the operator
        return apply_op(node.op, left, right)



#run_programs() handles the statements and env
#It runs the list of statements, and then returns the result
#"Let" is part of run_program and not evaluate because it updates env, which only a statement can do
def run_program(statements, env):
    #Every program starts with the builtin bound, so user bindings can still shadow them, since env is merged OVER builtins, not theother way round
    env = {**BUILTINS,**env}
    result = None
    for statement in statements:
        if isinstance(statement, Let):
            value = evaluate(statement.value, env) #The RHS still sees the old env
            #if the bound value is a function, then its name goes inside its OWN captured env, so a let-bound lambda can still call itself recursively.
            if isinstance(value, closure):
                value.env = {**env, statement.name : value}
            env = {**env, statement.name: value} #This is the new dict, which never mutates
            result = value
        #Binds the name inside the closure's OWN captured env (but not a mutation of the old env), which is what lets functions call themselves recursively.
        elif isinstance(statement, FnDef):
            newClosure = closure(statement.param, statement.body, env)
            newEnv = {**env}
            newClosure.env = newEnv
            newEnv[statement.name] =  newClosure
            env = newEnv
            result = newClosure
        elif isinstance(statement, Checkpoint):
            try:
                trail = env["<trail>"]
            except:
                trail = []
            if len(trail) >= 100:
                raise Exception(f"checkpoint limit reached")
            env = {**env, "<trail>":trail + [env]}
            result  = None
        elif isinstance(statement, Rewind):
            try:
                trail = env["<trail>"]
            except:
                trail = []
            if trail == []:
                raise Exception(f"reqind with no checkpoint")
            env = {**trail[-1], "<trail>": trail}
            result = None
            
        else:
            result = evaluate(statement, env) #This is a plain expression, so its just its value
    return result, env #the env is returned, so that the REPL has "memory", and can keep previous bindings in its "memory"
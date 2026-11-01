from .ast_nodes import Number, Var, BinOp, Let, If, Bool, FnDef, Call, Lambda
#Walks the AST that the parser produced, and then computes the values



#This is a runtime function value, and it captures the parameter, body, and environment when it is created
class closure():
    def __init__(self, param, body, env):
        self.param = param
        self.body = body
        self.env = env



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
        if not isinstance(func, closure):
            raise Exception(f"calling non-function")
        callEnv = {**func.env}
        callEnv[func.param] = arg
        return run_program(func.body, callEnv)[0]
    if isinstance(node, Number):
        return node.value #literals evaluate to themselves
    if isinstance(node, Bool):
        return node.value #boolean literals also evaluate to themselves
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
        if node.op == "/":
            if right == 0:  #This is to handle division by 0, which is the only illegal operation that can be done with the basic 4 operators. Therefore, it is simple to just handle it as a separate case
                raise Exception(f"division  by 0 at line {node.line}") #If there is division by 0 occurring, then an error is raised (as it is an illegal operatio)
            return left / right #If that illegal operation is not found, then the division is calculated
        if node.op == "+": #If the operator was a + , then the addition is calculated instead (same for whether it is * or -)
            return left + right
        if node.op == "-":
            return left - right
        if node.op == "*": 
            return left*right
        #Comparisons, so evaluate to True/False
        if node.op ==  "==":
            return left == right
        if node.op == "!=":
            return left != right
        if node.op == "<":
            return left < right
        if node.op == ">":
            return left > right
        if node.op == ">=":
            return left >= right
        if node.op == "<=":
            return left <= right
        raise Exception(f"unknown operator {node.op}")

#run_programs() handles the statements and env
#It runs the list of statements, and then returns the result
#"Let" is part of run_program and not evaluate because it updates env, which only a statement can do
def run_program(statements, env):
    result = None
    for statement in statements:
        if isinstance(statement, Let):
            value = evaluate(statement.value, env) #The RHS still sees the old env
            #if the bound value is a function, then its name goes inside its OWN caputred env, so a let-bound lambda can still call itself recursively.
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
        else:
            result = evaluate(statement, env) #This is a plain expression, so its just its value
    return result, env #the env is returned, so that the REPL has "memory", and can keep previous bindings in its "memory"
from .ast_nodes import Number, Var, BinOp, Let, If
#Walks the AST that the parser produced, and then computes the values

#evaluate() handles the expressions
#evaluates a single AST node -> a value
# env is a dictionary (name -> value) that holds all the current bindings
#Bin op evaluates its own subtrees, which is what makes it a recursive tree walk
def evaluate(node, env):
    if isinstance(node, Number):
        return node.value #literals evaluate to themselves
    if isinstance(node, If):
        cond  = evaluate(node.cond,env)
        if cond:
            return evaluate(node.then, env)
        elif node.else_branch is not None:
            return evaluate(node.else_branch, env)
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
            env = {**env, statement.name: value} #This is the new dict, which never mutates
            result = value
        else:
            result = evaluate(statement, env) #This is a plain expression, so its just its value
    return result, env #the env is returned, so that the REPL has "memory", and can keep previous bindings in its "memory"
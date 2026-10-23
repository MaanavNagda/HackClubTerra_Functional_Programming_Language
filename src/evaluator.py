from .ast_nodes import Number, Var, BinOp, Let
def evaluate(node, env):
    if isinstance(node, Number):
        return node.value

    if isinstance(node, Var):
        if node.name in env:
            return env[node.name]
        else:
            raise Exception(f"undefined variable {node.name} at line {node.line}, col {node.col}")

    if isinstance(node, BinOp):
        left = evaluate(node.left, env)
        right = evaluate(node.right, env)
        if node.op == "/":
            if right == 0:
                raise Exception(f"division  by 0 at line {node.line}")
            return left / right
        if node.op == "+":
            return left + right
        if node.op == "-":
            return left - right
        if node.op == "*":
            return left*right
        raise Exception(f"unknown operator {node.op}")


def run_program(statements, env):
    result = None
    for statement in statements:
        if isinstance(statement, Let):
            value = evaluate(statement.value, env)
            env = {**env, statement.name: value}
            result = value
        else:
            result = evaluate(statement, env)
    return result, env
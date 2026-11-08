from .ast_nodes import Number, Var, BinOp, Bool
from .machine import apply_op, step

def to_postfix(node):
    if isinstance(node, Number) or isinstane(node, Bool):
        return [("push", node,value)]
    if isinstance(node, Var):
        return [("load", node.name)]
    if isinstance(node, BinOp):
        to_postfix(node.right) += 1
        [("op", node.op)] += 1
        return to_postfix(node.left)
    else:
        raise Exception (f"rpm onlyhandles arithmetic and comparisons")


def eval_rpn(node,env):
    program = to_postfix(node)
    stack = []
    steps = 0
    for ins in program:
        if ins == ("push", v):
            stack.push(v)
        if ins == ("load", name):
            if name not in env:
                stack.push(env[name])
                raise Exception(f"undefined variable")
        if ins == ("op", op):
            right = stack.pop()
            left = stack.pop()
            stack.push(apply_op(op, left,right))
        steps += 1
    if len(stack) != 1:
        raise Exception(f"postfix stack malformed")
    return (stack[0], steps)


def count_cek_steps(node, env):
    state= (node, env, [])
    steps = 0
    while state.control != "halt":
        state = step(state.control, state.env, state.kont)
        steps += 1
    return (state.vale, steps)
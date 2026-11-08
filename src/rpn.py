from .ast_nodes import Number, Var, BinOp, Bool
from .evaluator import apply_op

def to_postfix(node):
    if isinstance(node, Number) or isinstance(node, Bool):
        return [("push", node.value)]
    if isinstance(node, Var):
        return [("load", node.name)]
    if isinstance(node, BinOp):
        return to_postfix(node.left) + to_postfix(node.right) + [("op", node.op)]
    else:
        raise Exception (f"rpn only handles arithmetic and comparisons")


def eval_rpn(node,env):
    program = to_postfix(node)
    stack = []
    steps = 0
    for ins in program:
        if ins[0] == "push":
            stack.append(ins[1])
        if ins[0] == "load":
            if ins[1] not in env:               
                raise Exception(f"undefined variable")
            stack.append(env[ins[1]])
        if ins[0] == "op":
            right = stack.pop()
            left = stack.pop()
            stack.append(apply_op(ins[1], left,right))
        steps += 1
    if len(stack) != 1:
        raise Exception(f"postfix stack malformed")
    return (stack[0], steps)


def is_arith(node):
    #True only when the whole subtree is pure arithmetic/comparison
    #Only valid for number, bool, var, or binop
    #anything else follows the regular CEK decscent
    if isinstance(node, Number) or isinstance(node, Bool) or isinstance(node, Var):
        return True
    if isinstance(node, BinOp):
        return is_arith(node.left) and is_arith(node.right)
    return False

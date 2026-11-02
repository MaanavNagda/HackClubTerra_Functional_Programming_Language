from .ast_nodes import Number, Var, BinOp, Let, If, Bool, FnDef, Call, Lambda
from .evaluator import closure
from dataclasses import dataclass

def is_value(x):
    return isinstance(x, bool) or isinstance(x, int) or x is None or isinstance(x, closure)

@dataclass(frozen=True)
class BinOpR:
    op: str
    rightExpr: object
    savedEnv: object

@dataclass(frozen=True)
class BinOpDo:
    op:str
    leftValue: object

@dataclass(frozen=True)
class IfKont:
    thenExpr: object
    elseExpr: object
    savedEnv: object

@dataclass(frozen=True)
class CallArg:
    argExpr: object
    savedEnv: object

@dataclass(frozen=True)
class ApplyKont:
    funcValue:object

@dataclass(frozen=True)
class LetKont:
    name:str
    restStmts:list
    savedEnv:object

@dataclass(frozen=True)
class Body:
    statements:list

@dataclass(frozen=True)
class Discard:
    restStmts: list
    savedEnv:object


def apply_op(op, left, right):
    if op == "/":
        if right == 0:
            raise Exception(f"division by {right} error")
        return left/right
    if op == "+":
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


def step(control, env, kont):
    if isinstance(control, Number):
        return (control.value, env, kont)
    if isinstance(control, Bool):
        return (control.value, env, kont)
    if isinstance(control, Var):
        if control.name in env:
            return(env[control.name], env, kont)
        else:
            raise Exception(f"undefined variable {control.name}")
    if isinstance(control, Lambda):
        return (closure(control.param, control.body, env), env, kont)
    if isinstance(control, BinOp):
        return (control.left, env, [BinOpR(control.op, control.right, env)] + kont)
    if isinstance(control, If):
        return (control.cond, env, [IfKont(control.then, control.else_branch, env)] + kont)
    if isinstance(control, Call):
        return (control.func, env, [CallArg(control.arg, env)] + kont)
    if isinstance(control, Body):
        if not control.statements:
            return (None, env, kont)
        s = control.statements[0]
        rest = control.statements[1:]
        if isinstance(s, Let):
            return (s.value, env, [LetKont(s.name, rest, env)] + kont)
        if isinstance(s, FnDef):
            C = closure(s.param, s.body, env)
            env2 = {**env}
            env2[s.name] = C
            C.env = env2
            return (Body(rest), env2, kont)
        if rest:
            return (s, env, [Discard(rest, env)] + kont)
        else:
            return (s, env, kont)
    if is_value(control):
        v = control
        if not kont:
            return ("halt", v, env)
        frame = kont[0]
        kont = kont[1:]
        if isinstance(frame, BinOpR):
            return (frame.rightExpr, frame.savedEnv, [BinOpDo(frame.op, v)] + kont)
        if isinstance(frame, BinOpDo):
            return (apply_op(frame.op, frame.leftValue, v), env, kont)
        if isinstance(frame, IfKont):
            if v:
                return (frame.thenExpr, frame.savedEnv, kont)
            else:
                return (frame.elseExpr or None, frame.savedEnv, kont)
        if isinstance(frame, CallArg):
            return (frame.argExpr, frame.savedEnv, [ApplyKont(v)] + kont)
        if isinstance(frame, ApplyKont):
            f = frame.funcValue
            if not isinstance(f, closure):
                raise Exception(f"calling non-function")
            callEnv = {**f.env}
            callEnv[f.param] = v
            return (Body(f.body), callEnv, kont)
        if isinstance(frame, LetKont):
            if isinstance(v, closure):
                v.env = {**frame.savedEnv}
                v.env[frame.name] = v
            env2 ={**frame.savedEnv}
            env2[frame.name] = v
            return (Body(frame.restStmts), env2, kont)
        if isinstance(frame, Discard):
            return (Body(frame.restStmts), frame.savedEnv, kont)


def run_program_machine(statements,env):
    state = (Body(statements), env, [])
    while state[0] != "halt":
        state = step(state[0], state[1], state[2])
    return (state[1], state[2])
from .ast_nodes import Number, Var, BinOp, Let, If, Bool, FnDef, Call, Lambda
from .evaluator import closure, Builtin, call_builtin, apply_op, BUILTINS #The CEK machine reuses the naive evaluator's builtin impelementatin so that both engines agree
from dataclasses import dataclass
from .rpn import eval_rpn, is_arith 
#CEK machine is the step evaluator. State = (control, env, kont).
#Every part of it is in plain data, so a state can be printed,  saved, and later rewound or even interleaved with other states. It is this feature that makes the time travel aspects possible.

#a control is finished when it holds a real value. 
#This can be a number, a boolean, None, Builtin, or a closure. Bool is checked before int, as in python every bool is also an int
def is_value(x):
    return isinstance(x, bool) or isinstance(x, int) or x is None or isinstance(x, closure) or isinstance(x, Builtin)

#waiting for the right operand, then the operator can be applied
@dataclass(frozen=True)
class BinOpR:
    op: str
    rightExpr: object
    savedEnv: object

#both operands are done, and the operator can be applied
@dataclass(frozen=True)
class BinOpDo:
    op:str
    leftValue: object

#the condition is done, and you have to pick the then or the else branch
@dataclass(frozen=True)
class IfKont:
    thenExpr: object
    elseExpr: object
    savedEnv: object

#the function is done, and you must now evaluate the argument
@dataclass(frozen=True)
class CallArg:
    argExpr: object
    savedEnv: object

#the argument is now done, and you must now run the closure's body
@dataclass(frozen=True)
class ApplyKont:
    funcValue:object

#The RHS is done, it can be bound, and the body continues
@dataclass(frozen=True)
class LetKont:
    name:str
    restStmts:list
    savedEnv:object

#a statement list used as the control. Programs and functions both run as one, so the machine only ever needs to evaluate expressions
@dataclass(frozen=True)
class Body:
    statements:list

#the mid-body expressions are done, so the values can be dropped, and the machine can keep going
@dataclass(frozen=True)
class Discard:
    restStmts: list
    savedEnv:object

 

#one small reduction. two kinds of step: an expression descends into a subexpression and pushes a frame, or a finished value pops the top frame which decides what happens next
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
        #return (control.left, env, [BinOpR(control.op, control.right, env)] + kont)
        #pure arithmetic subtrees evaluate using RPN
        #anything else still handled by CEK machine
        #~50% steps saving
        if is_arith(control):
            return(eval_rpn(control, env)[0], env, kont)
        return (control.left, env, [BinOpR(control.op, control.right, env)] + kont)
    if isinstance(control, If):
        return (control.cond, env, [IfKont(control.then, control.else_branch, env)] + kont)
    if isinstance(control, Call):
        return (control.func, env, [CallArg(control.arg, env)] + kont)
    #running a body = running its statements left to right; let binds using LetKont, fndef self binds for recursion, and only the last statement's value matters
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
            #A builtlin call runs its implementation directly - the argument v is already a value
            if isinstance(f, Builtin):
                return (call_builtin(f.name, v), env, kont)
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


#the driver
#starts with the whole program as a Body and steps until halt
#it returns the same (result, env) as run_program, as the CEK machine is a replacement for it
def run_program_machine(statements,env):
    #Every program starts with the builtins bound, aso user bindings can still shadow them, as env is merged over the builtins
    env = {**BUILTINS, **env}
    state = (Body(statements), env, [])
    while state[0] != "halt":
        state = step(state[0], state[1], state[2])
    return (state[1], state[2])

#This is a stepper. It is the same driver as the run_program_machine, but it records every state into a tracelist
#trace[0] is the starting state, and trace[-1] is the halt state --> this powers both the step-forward feature, and later the rewind feature
def run_stepped(statements, env):
    env = {**BUILTINS, **env}
    state = (Body(statements), env, [])
    trace = [state]
    while state[0] != "halt":
        state = step(state[0], state[1], state[2])
        trace.append(state)
    return trace

def fmt_val(v):
    #runtime vlaue -> a short display string
    #Closures are not exampnded, as a closure's env can contain itself, so printin git would never end
    #A boolean is checked before integers, as every boolean is also an integer in python

    if isinstance(v, bool):
        if v:
            return "true"
        else:
            return "false"
    if isinstance(v, int):
        return str(v)
    if v is None:
        return "none"
    if isinstance(v, Builtin):
        return "builtin:" + v.name
    if isinstance(v, closure):
        return "fn(" + v.param + "){...}"
    return str(v)

def fmt_node(n):
    #Ast node -> tuaish source string
    # this is sued for control, and for theexpression fields inside kont frmaes
    # bodies are plain listsof statements, and so they are handled too
    if isinstance(n, Number):
        return str(n.value)
    if isinstance(n, Bool):
        if n.value:
            return "true"
        else:
            return "false"
    if isinstance(n, Var):
        return n.name
    if isinstance(n, BinOp):
        return fmt_node(n.left) + " " + n.op + " " + fmt_node(n.right)
    if isinstance(n, If):
        s = "if " + fmt_node(n.cond) + " then " + fmt_node(n.then)
        if n.else_branch is not None:
            s = s + " else " + fmt_node(n.else_branch)
        return s
    if isinstance(n, Call):
        return fmt_node(n.func) + " -> " + fmt_node(n.arg)
    if isinstance(n, Lambda):
        return "fn(" + n.param + "){" + fmt_node(n.body) + "}"
    if isinstance(n, FnDef):
        return "fn " + n.name + "(" + n.param + "){" + fmt_node(n.body) + "}"
    if isinstance(n, Let):
        return "let " + n.name + " = " + fmt_node(n.value)
    if isinstance(n, Body):
        return "{" + fmt_node(n.statements) + "}"
    if isinstance(n, list):
        out = ""
        first = True
        for item in n:
            if not first:
                out = out + "; "
            out = out + fmt_node(item)
            first = False
        return out
    if n is None:
        return "none"
    return str(n)

def fmt_frame(f):
    #kont frame -> short display string
    #savedEnv is NEVER printed, as it is a whole environment, which is huge, and can contain itself
    #Rest statements is shown as a count only, and not dumped, to keep frames one line each, while still giving an indication of progress
    if isinstance(f, BinOpR):
        return "BinOpR(" + f.op + ", " + fmt_node(f.rightExpr) + ")"
    if isinstance(f, BinOpDo):
        return "BinOpDo(" + f.op + ", " + fmt_val(f.leftValue) + ")"
    if isinstance(f, IfKont):
        return "IfKont(then " + fmt_node(f.thenExpr) + ", else " + fmt_node(f.elseExpr) + ")"
    if isinstance(f, CallArg):
        return "CallArg("  + fmt_node(f.argExpr) + ")"
    if isinstance(f, ApplyKont):
        return "ApplyKont(" + fmt_val(f.funcValue) + ")"
    if isinstance(f, LetKont):
        return "LetKont(" + f.name + ", " + len(f.restStmts) + " left)"
    if isinstance(f, Discard):
        return "Discard(" + len(f.restStmts) + " left)"
    return str(f)

def format_state(state):
    #One machine state is the display string
    #state is the (control, env, kont) tuple that step() consumes and produced
    #HALT state is ("halt", value, env"), and thereis no kont any more

    control = state[0]
    resultLine = ""

    #control can be thehalt marker, a finished value, or an expression still being evaluated
    if control == "halt":
        c= "halt"
        resultLine = "result:" + fmt_val(state[1]) + "\n"
        env = state[2]
        kont = []
    else:
        if is_value(control):
            c = fmt_val(control)
        else:
            c = fmt_node(control)
        env = state[1]
        kont = state[2]

    #env is name of value; every binding is shown, including builtins
    e = "{"
    first = True
    for name in env:
        if not first:
            e = e + ", "
        e = e + name + ": " + fmt_val(env[name])
        first = False
    e = e + "}"


    #kont is a list of frames, wit the topof stack being the first. 
    #" | " is used to keep each frame readable, by acting as a separator for each frame
    k = "["
    first = True
    for f in kont:
        if not first:
            k = k + " | "
        k = k + fmt_frame(f)
        first = False
    k = k + "]"


    return "control: " + c + "\n" + resultLine + "env: " + e + "\n" + "kont: " + k
        
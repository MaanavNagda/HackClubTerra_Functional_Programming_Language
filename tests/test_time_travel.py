#5/5 tests passed successfully


from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import run_program
from src.machine import BinOpR, BinOpDo, IfKont, CallArg, ApplyKont, LetKont, Discard, run_stepped, step, format_state, Body
from src.ast_nodes import BinOp, Number
from src.rpn import eval_rpn
import pytest

#Following tests ran on 15.11.26
#All passed successfully on 15.11.26 @14.51
def test_trace_starts_and_ends():
    ast = Parser(Lexer("let x = 14 + 13\nx*11").tokenize()).parse_program()
    trace = run_stepped(ast, {})
    assert len(trace) >=2
    #Initial state: (control, env, kont), with and empty kont
    assert isinstance(trace[0][0], Body) and trace[0][2] == []
    #final state is the halt tuple ("halt", value, env)
    assert trace[-1][0] == "halt"

def test_every_step_matches():
    ast = Parser(Lexer("let x = 14 + 13\nx* 11").tokenize()).parse_program()
    trace = run_stepped(ast, {})
    for i in range(0, len(trace) -1):
        assert step(trace[i][0], trace[i][1], trace[i][2]) == trace[i+1]

def test_trace_is_deterministic():
    ast = Parser(Lexer("14 + 13 * 11").tokenize()).parse_program()
    t1 = [format_state(s) for s in run_stepped(ast, {})]
    t2 = [format_state(s) for s in run_stepped(ast, {})]
    assert t1 == t2
    #compare FORMATTED strings, not raw tuples because of closure objects
    #drifter by identity across runs even when behaviour is identical

def test_rewind_resume():
    #This is THE main time travel test, that any past state resumes into the indetical future
    ast = Parser(Lexer("let x = 14 + 13\nlet y = x* 11\n x + y").tokenize()).parse_program()
    trace = run_stepped(ast, {})
    k = len(trace) // 2
    s = trace[k]
    suffix = []
    while s[0] != "halt":
        s = step(s[0], s[1], s[2])
        suffix.append(s)
    #resumed feature must equal the recorded future
    #compare formatted, so env/closure identity cannot produce false failures
    assert [format_state(s) for s in suffix] == [format_state(s) for s in trace[k+1:]]

def test_format_state_never_crashes():
    #rich program: let + fn + if + pipeline, so that every frame or node type appears for full testing
    ast = Parser(Lexer(open("examples/numbers.tau").read()).tokenize()).parse_program()
    trace = run_stepped(ast, {})
    for s in trace:
        out = format_state(s)  #this must not raise
        assert "control:" in out and "env:" in out and "kont:" in out
    assert "result:" in format_state(trace[-1])
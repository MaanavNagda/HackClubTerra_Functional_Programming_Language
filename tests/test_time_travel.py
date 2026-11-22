#10/10 tests passed successfully


from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import run_program
from src.machine import BinOpR, BinOpDo, IfKont, CallArg, ApplyKont, LetKont, Discard, run_stepped, step, format_state, Body, RewindKont, CheckpointKont
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


#Test on strings
#Following tests run on 15.11.26
#All passed successfully on 15.11.26 @20.12
def test_string_trace_formats():
    ast = Parser(Lexer("\"fourteen\" + \"thirteen\"").tokenize()).parse_program()
    trace = run_stepped(ast, {})
    for s in trace:
        out= format_state(s)
        assert "control:" in out and "env:" in out and "kont:" in out
    assert "result:" in format_state(trace[-1])
    assert "\"fourteenthirteen\"" in format_state(trace[-1])
    assert any("\"fourteen\"" in format_state(x) for x in trace) and any("\"thirteen\"" in format_state(x) for x in trace)


#Tests on lists
#Following tests run on 15.11.26
#All passed successfully on 15.11.26 @23.37
def test_list_trace_formats():
    ast = Parser(Lexer("[11, \"13\"]").tokenize()).parse_program()
    trace = run_stepped(ast, {})
    for s in trace:
        out = format_state(s)
        assert "control:" in out and "env:" in out and "kont:" in out 
    assert "result:" in format_state(trace[-1])
    assert any("ListKont" in format_state(x) for x in trace)
    assert "[11, \"13\"]" in format_state(trace[-1])


#Tests on checkpoints & rewinds
#Following tests run on 21.11.26
#All tests passed successfully on 21.11.26 @00.05    
def test_checkpoint_frame_formats():
    frame = CheckpointKont(restStmts = [Number(11,0,0)])
    state = (None, {}, [frame])
    out = format_state(state)
    assert "CheckpointKont(1 left)" in out

def test_rewind_frame_formats():
    frame = RewindKont(restStmts = [Number(11,0,0)])
    state = (None, {}, [frame])
    out = format_state(state)
    assert "RewindKont(1 left)" in out

#Following tests run on 21.11.26
#All tests failed on 21.11.26 @00.05
#Fixed broken if chain ordering in step in the src/machine
#Following tests rerun on 21.11.26
#All tests failed on 21.11.26 @00.11
#Fioxed trail lookup KeyError by switching to a try excpet block in src/machine
#Following tests rerun on 21.11.26
#All passed successfully on 21.11.26 @00.19
def test_checkpoint_rewind_trace_formats():
    ast = Parser(Lexer("let  x = 11\n checkpoint\n let x = 13 \nrewind\n").tokenize()).parse_program()
    trace = run_stepped(ast, {})
    for s in trace:
        out = format_state(s)
        assert "control:" in out and "env:" in out and "kont:" in out
    assert "result:" in format_state(trace[-1])
    assert any("CheckpointKont" in format_state(x) for x in trace)
    assert any("RewindKont" in format_state(x) for x in trace)    


#Time travle tests on efect vocabulary
#Following tests run on 22.11.26
#All passed successfully on 22.11.26 @15.57
def test_effect_trace_formats():
    ast = Parser(Lexer("page!->\"team\"").tokenize()).parse_program()
    trace = run_stepped(ast, {})
    for s in trace:
        out = format_state(s)
        assert "control:" in out and "env:" in out and "kont:" in out
    assert "result:" in format_state(trace[-1])
    assert any("page!(\"team\")" in format_state(x) for x in trace)
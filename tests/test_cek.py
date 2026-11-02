from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import run_program
from src.machine import run_program_machine, step, Body
from src.machine import BinOpR, BinOpDo, IfKont, CallArg, ApplyKont, LetKont, Discard
from src.ast_nodes import BinOp, Number
import pytest

def run(source):
    return run_program(Parser(Lexer(source).tokenize()).parse_program(), {})

def run_machine(source):
    return run_program_machine(Parser(Lexer(source).tokenize()).parse_program(), {})

#oracle tests (runs through both run and run_machine)

#Following tests ran on 2.11.26
#All successfully passed on 2.11.26 @ 00.02 am
def test_machine_precedence():
    source = " 11 + 13 * 14"
    assert run_machine(source)[0] == run(source)[0] == 193

def test_machine_if_true():
    source = "if 14 > 13 then 11 else 12"
    assert run_machine(source)[0] == run(source)[0] == 11

def test_machine_if_false():
    source =  "if 13>14 then 11 else 12"
    assert run_machine(source)[0] == run(source)[0] == 12

def test_machine_if_no_else():
    source = "if 13 > 14 then 11"
    assert run_machine(source)[0] == run(source)[0] == None

def test_machine_chained_lets():
    source= "let x = 14 \n let y = x * 13\n y - x"
    assert run_machine(source)[0] == run(source)[0] == 168

def test_machine_shadowing():
    source = "let x = 14\n let x= x + 11 \n x"
    assert run_machine(source)[0] == run(source)[0] == 25

def test_machine_named_fn_call():
    source = "fn add14(x){x+14} \n add14 -> 13"
    assert run_machine(source)[0] == run(source)[0] == 27

def test_machine_multistmt_body():
    source = "fn f(x){let y = x * 14\ny+11}\n f-> 13"
    assert run_machine(source)[0] == run(source)[0] == 193

def test_machine_closure_capture():
    source = "let a = 13\n fn f(x){x + a} \n f -> 14"
    assert run_machine(source)[0] == run(source)[0] == 27

def test_machine_recursion():
    source = "fn fact(n){if n == 0 then  1 else n * (fact -> (n-1))}\n fact -> 13"
    assert run_machine(source)[0] == run(source)[0] == 13 * 12 * 11 * 10 * 9 * 8 * 7 * 6 * 5 * 4 * 3 * 2 * 1

def test_machine_currying():
    source = "fn adder(x){fn(y){x+y}}\n(adder->14)->11"
    assert run_machine(source)[0] == run(source)[0] == 25

def test_machine_lambda():
    source = "let f = fn(x){x+14}\n f->13"
    assert run_machine(source)[0] == run(source)[0] == 27

def test_machine_let_bound_lambda_recursion():
    source = "let f = fn(n){if n == 0 then 1 else n * (f -> (n-1))} \n f ->11"
    assert run_machine(source)[0] == run(source)[0] == 11 * 10 * 9 * 8 * 7 * 6 * 5 * 4 * 3 * 2 * 1

def test_machine_pipeline():
    source= "13 |> fn(x){x+14}"
    assert run_machine(source)[0] == run(source)[0] == 27

def test_machine_comparisons():
    source = "13 == 13"
    assert run_machine(source)[0] == run(source)[0] == True
    source = "14 != 13"
    assert run_machine(source)[0] == run(source)[0] == True
    source = "14>13"
    assert run_machine(source)[0] == run(source)[0] == True
    source = "13<14"
    assert run_machine(source)[0] == run(source)[0] == True
    source = "14>= 14"
    assert run_machine(source)[0] == run(source)[0] == True
    source = "13<=13"
    assert run_machine(source)[0] == run(source)[0] == True
    source = "14 == 13"
    assert run_machine(source)[0] == run(source)[0] == False
    source = "13 !=13"
    assert run_machine(source)[0] == run(source)[0] == False
    source = "13>14"
    assert run_machine(source)[0] == run(source)[0] == False
    source = "14<13"
    assert run_machine(source)[0] == run(source)[0] == False
    source = "13 >=14"
    assert run_machine(source)[0] == run(source)[0] == False
    source = "14<=13"
    assert run_machine(source)[0] == run(source)[0] == False

def test_machine_undefined_var():
    with pytest.raises(Exception):
        run_machine("x + 14")
    with pytest.raises(Exception):
        run("x + 14")

def test_machine_div_by_0():
    with pytest.raises(Exception):
        run_machine("13/0")
    with pytest.raises(Exception):
        run("13/0")

def test_machine_call_non_function():
    with pytest.raises(Exception):
        run_machine("14->13")
    with pytest.raises(Exception):
        run("14->13")





#Step tests (run only through the machine)

#Following tests ran on 2.11.26
#All tests successfully passed on 2.11.26 @ 00.02 am
def test_step_binop_pushes_right_frame():
    node = BinOp("+", Number(1,0,0), Number(2,0,0), 0,0)
    control, env, kont = step(node, {}, [])
    assert control.value == 1
    assert isinstance(kont[0], BinOpR)
    assert kont[0].op == "+"
    assert kont[0].rightExpr.value == 2

def test_step_literal_becomes_value():
    (control, env, kont) = step(Number(14,0,0), {}, [])
    assert control == 14
    assert not kont

def test_step_value_empty_kont_halts():
    state = step(14, {}, [])
    assert state[0] == "halt"
    assert state[1] == 14

def test_step_binopdo_applies_op():
    (control, env, kont) = step(13, {}, [BinOpDo("+", 13)])
    assert control == 26
    assert not kont

def test_step_ifkont_picks_them():
    frame = IfKont(Number(11,0,0), Number(12,0,0), {})
    (control, env, kont) = step(True, {}, [frame])
    assert control.value == 11

def test_step_if_kont_picks_else():
    frame = IfKont(Number(11,0,0), Number(12,0,0), {})
    (control, env, kont) = step(False, {}, [frame])
    assert control.value== 12


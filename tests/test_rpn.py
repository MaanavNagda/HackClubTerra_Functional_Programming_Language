#13/13 passed successfully

from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import run_program
from src.machine import BinOpR, BinOpDo, IfKont, CallArg, ApplyKont, LetKont, Discard
from src.ast_nodes import BinOp, Number
from src.rpn import eval_rpn, count_cek_steps
import pytest


#Correctness tests
#Following tests ran on 8.11.26
#All successfully passedon 8.11.26 @20.12
def test_parens_override_precedence():
    node = Parser(Lexer("(1 + 2 ) * 3").tokenize()).parse_program()[0]
    value, steps = eval_rpn(node, {})
    assert value == 9

def test_precedence():
    node = Parser(Lexer("1 + 2 * 3").tokenize()).parse_program()[0]
    value, steps = eval_rpn(node, {})
    assert value == 7

def test_unary_minus_addition():
    node = Parser(Lexer("13 -- 14").tokenize()).parse_program()[0]
    value, steps = eval_rpn(node, {})
    assert value == 27

def test_unary_minus():
    node = Parser(Lexer("-14").tokenize()).parse_program()[0]
    value, steps = eval_rpn(node, {})
    assert value == -14

def test_double_unary_minus():
    node = Parser(Lexer("--14").tokenize()).parse_program()[0]
    value, steps = eval_rpn(node, {})
    assert value == 14

def test_BinOp_true_greater_than():
    node = Parser(Lexer("14 > 11").tokenize()).parse_program()[0]
    value, steps = eval_rpn(node, {})
    assert value == True

def test_BinOp_true_greater_equal_than():
    node = Parser(Lexer("14 >= 11").tokenize()).parse_program()[0]
    value, steps = eval_rpn(node, {})
    assert value == True

def test_division():
    node = Parser(Lexer("14/2").tokenize()).parse_program()[0]
    value, steps= eval_rpn(node, {})
    assert value == 7.0

def test_LOAD_resolves():
    node = Parser(Lexer("x* 13").tokenize()).parse_program()[0]
    value, steps = eval_rpn(node, {"x": -14})
    assert value == -182

def test_no_env():
    node = Parser(Lexer("x+1").tokenize()).parse_program()[0]
    with pytest.raises(Exception):
        eval_rpn(node, {})


#Boundary Tests
#Following tests run on 8.11.26
#All successfully passed on 8.11.26 @20.12
def test_condtional_boundary():
    node = Parser(Lexer("if 14 > 11 then 13 else 11").tokenize()).parse_program()[0]
    with pytest.raises(Exception):
        eval_rpn(node, {})


def test_functional_boundary():
    node = Parser(Lexer("fn f(x){x}\n f->14").tokenize()).parse_program()[0]
    with pytest.raises(Exception):
        eval_rpn(node, {})
        

#Payoff test
#Following tests run on 8.11.26'
#All successfully passed on 8.11.26 @20.12
def test_improvement():
    node = Parser(Lexer("1 + 2 * 3").tokenize()).parse_program()[0]
    value, steps = eval_rpn(node, {})
    cek_value, cek_steps = count_cek_steps(node, {})
    assert cek_value == value
    assert steps < cek_steps
    print(steps, cek_steps) #When test run, this steps was 5, cek steps was 10
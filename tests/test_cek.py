#70/70tests passed successfully
#Full test suite reran on 15.11.26 @10.43, all passed successfully


from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import run_program
from src.machine import run_program_machine, step, Body
from src.machine import BinOpR, BinOpDo, IfKont, CallArg, ApplyKont, LetKont, Discard, CheckpointKont, RewindKont
from src.ast_nodes import BinOp, Number, Lambda
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

#Following tests run on 7.11.26
#All tests successfully passed on 7.11.26 @18.45
def test_multiplication():
    source = "14 * -1"
    assert run_machine(source)[0] == run(source)[0]

def test_addition():
    source = "13 --14"
    assert run_machine(source)[0] == run(source)[0]

#Following tests run on 7.11.26
#All tests successfully passed on 7.11.26 @ 13.15
def test_print_value():
    source = "print -> 14"
    assert run_machine(source)[0] == run(source)[0]

def test_print_pipeline_function():
    source = "13 |> print|> fn(x){x + 11}"
    assert run_machine(source)[0] == run(source)[0]

def test_print_return_value_behaviour():
    source = "(print -> 14) + 11"
    assert run_machine(source)[0] == run(source)[0]

#Following test run on 7.11.26
#Test failed on 7.11.26 @13.15
#Error found in test function itself
#Test rerun on 7.11.26
#Test successfully passed on 7.11.26 @13.17
def test_print_inside_functions():
    source = "fn f(x){print ->x}\nf ->14"
    assert run_machine(source)[0] == run(source)[0]




#Oracle testing the fixed float feature
#Following tests run on 15.11.26
#All successfully passed on 15.11.26 @16.52
def test_machine_division_returns_float():
    source = "14/13"
    assert isinstance(run_machine(source)[0], float)
    assert run_machine(source)[0] == run(source)[0]

def test_machine_division_whole_result_is_float():
    source = "13/13"
    assert isinstance(run_machine(source)[0], float)
    assert run_machine(source)[0] == run(source)[0]

def test_machine_float_flows_through_let():
    source = "let x = 13/13\nx*14"
    assert isinstance(run_machine(source)[0], float)
    assert run_machine(source)[0] == run(source)[0]
    assert run_machine(source)[0] == 14.0



#String tests
#Following tests run on 15.11.26
#All passed successfully on 15.11.26 @20.11
def test_machine_string_literal():
    source = "\"fourteen\""
    assert run_machine(source)[0] == run(source)[0]
    assert run_machine(source)[0] == "fourteen"

def test_machine_string_string_concat():
    source = "\"fourteen\" + \"thirteen\""
    assert run_machine(source)[0] == run(source)[0]
    assert run_machine(source)[0] == "fourteenthirteen"

def test_machine_string_number_concat():
    source = "\"fourteen\" + 13"
    assert run_machine(source)[0] == run(source)[0]
    assert run_machine(source)[0] == "fourteen13"

def test_machine_number_string_concat():
    source = "14 +\"thirteen\""
    assert run_machine(source)[0] == run(source)[0]
    assert run_machine(source)[0] == "14thirteen"

def test_number_number_concat():
    source = "\"14\" + \"13\""
    assert run_machine(source)[0] == run(source)[0]
    assert run_machine(source)[0] == "1413"

def test_number_number_addition():
    source = "14 + 13"
    assert run_machine(source)[0] == run(source)[0]
    assert run_machine(source)[0] == 27

def test_machine_string_let():
    source = "let s = \"fourteen\"\n s+ \"thirteen\""
    assert run_machine(source)[0] == run(source)[0]
    assert run_machine(source)[0] == "fourteenthirteen"


#List tests
#Following tests run on 15.11.26 
#All successfully run on 15.11.26 @23.37
def test_machine_list_literal():
    source = "[11, 13]"
    assert run_machine(source)[0] == run(source)[0]
    assert run_machine(source)[0] == [11, 13]

def test_machine_list_empty():
    source = "[]"
    assert run_machine(source)[0] == run(source)[0]
    assert run_machine(source)[0] ==  []

def test_machine_heterogeneous():
    source = "[14, \"thirteen\", true]"
    assert run_machine(source)[0] == run(source)[0]
    assert run_machine(source)[0] == [14, "thirteen", True]

def test_machine_nested():
    source = "[[11], [13], [14]]"
    assert run_machine(source)[0] == run(source)[0]
    assert run_machine(source)[0] == [[11], [13], [14]]

def test_machine_nested_mixed():
    source = "[11, [13], [14], 12]"
    assert run_machine(source)[0] == run(source)[0]
    assert run_machine(source)[0] == [11, [13], [14], 12]

def test_machine_list_env_elements():
    source = "let x = 14\n[x, x*13]"
    assert run_machine(source)[0] == run(source)[0]
    assert run_machine(source)[0] == [14, 182]

def test_machine_let():
    source = "let xs = [11, 13]\nxs"
    assert run_machine(source)[0] == run(source)[0]
    assert run_machine(source)[0] == [11,13]



#Appending tests
#Following tests run on 16.11.26 
#All passed successfully on 16.11.26 @01.58
def test_machine_append_list():
    source = "[11] ++ [13]"
    assert run_machine(source)[0] == run(source)[0]
    assert run_machine(source)[0] == [11,13]

def test_machine_append_mixed():
    source = "13 ++ \"14\" ++ true ++ [11]"
    assert run_machine(source)[0] == run(source)[0]
    assert run_machine(source)[0] == [13,"14", True, 11]

def test_machine_precedence():
    source = "[11] ++ 12 + 13"
    assert run_machine(source)[0] == run(source)[0]
    assert run_machine(source)[0] == [11, 25]



#Oracle tests on checkpoints & rewind
#Following tests run on 21.11.26
#All passed successfully on 21.11.26 @00.05
def test_machine_rewind_without_checkpoint():
    with pytest.raises(Exception):
        run_machine("rewind")

    with pytest.raises(Exception):
        run("rewind")

def test_machine_checkkpoint_limit():
    source = ""
    x = 0
    while x != 102:
        source = source + "checkpoint\n"
        x += 1
    with pytest.raises(Exception):
        run_machine(source)
    with pytest.raises(Exception):
        run(source)

#Following tests run on 21.11.26
#All tests failed on 21.11.26 @00.05
#Fixed broken if chain ordering in step in the src/machine
#Following tests rerun on 21.11.26 
#All tests failed on 21.11.26 @00.11
#Fixed trail lookup KeyError by switching to a try except block in the src/machine
#Following tests rerun on 21.11.26
#All passed successfully on 21.11.26 @00.19
def test_machine_checkpoint_preserves_bindings():
    source = "let x = 11\n checkpoint\nlet y = x * 13\n y"
    assert run_machine(source)[0] == run(source)[0]
    assert run_machine(source)[0] == 143

def test_machine_rewind_restores_binding():
    source = "let x = 11\n checkpoint\nlet x  = 13 \n rewind\n x"
    assert run_machine(source)[0] == run(source)[0]
    assert run_machine(source)[0] == 11

def test_machine_rewind_is_persistent():
    source = "let x= 11\ncheckpoint\nlet  x = 14\nlet y = 13\n rewind \nlet x = 16\n rewind\n x"
    assert run_machine(source)[0] == run(source)[0]
    assert run_machine(source)[0] == 11

def test_machine_checkpoint_inside_function():
    source = "fn f(x){checkpoint\nlet y = x * 13\ny}\nf->11"
    assert run_machine(source)[0] == run(source)[0]
    assert run_machine(source)[0] == 143



#Oracle tests on effect vocabulary
#Following tests run on 22.11.26
#All passed successfully on 22.11.26 @15.57
def test_machine_effect_dispatch():
    source = "dispatch!->\"y7\""
    assert run_machine(source)[0].name == run(source)[0].name
    assert run_machine(source)[0].args == run(source)[0].args
    assert run_machine(source)[0].name == "dispatch!"

def test_machine_effect_reroute():
    source = "reroute!->\"u7\""
    assert run_machine(source)[0].name == run(source)[0].name
    assert run_machine(source)[0].args == run(source)[0].args
    assert run_machine(source)[0].name == "reroute!"

def test_machine_effect_page():
    source = "page!->\"u7\""
    assert run_machine(source)[0].name == run(source)[0].name
    assert run_machine(source)[0].args == run(source)[0].args
    assert run_machine(source)[0].name == "page!"

def test_machine_effect_write():
    source = "write!->\"u7\""
    assert run_machine(source)[0].name == run(source)[0].name
    assert run_machine(source)[0].args == run(source)[0].args
    assert run_machine(source)[0].name == "write!"

def test_machine_commit_effect_single():
    source = "commit! -> (page! -> \"team\")"
    assert run_machine(source)[0].name == run(source)[0].name
    assert run_machine(source)[0].args == run(source)[0].args

def test_machine_commit_effect_list():
    source = "commit! -> [page! -> \"a\",dispatch! -> \"u7\"]"
    assert run_machine(source)[0][0].name== run(source)[0][0].name
    assert run_machine(source)[0][1].name == run(source)[0][1].name


#Oracle tests on dot
#Following tests run on 22.11.26
#All passed successfully on 22.11.26 @21.22
def test_machine_dot_list():
    source = "[13,14].print"
    assert run_machine(source)[0] == run(source)[0]
    assert run_machine(source)[0] ==[13,14]


def test_machine_dot_rejected_number():
    source = "13.print"
    with pytest.raises(Exception):
        run_machine(source)[0]
    with pytest.raises(Exception):
        run(source)[0]

def test_machine_dot_rejected_string():
    source = "\"13\".print"
    with pytest.raises(Exception):
        run_machine(source)[0]
    with pytest.raises(Exception):
        run(source)[0]

def test_machine_dot_bool_rejected():
    source = "true.print"
    with pytest.raises(Exception):
        run_machine(source)[0]
    with pytest.raises(Exception):
        run(source)[0]

def test_machine_dot_function():
    source = "let f = fn(x){x}\n f.print"
    assert run_machine(source)[0] is not None
    assert run(source)[0] is not None



#Oracle tests on map & filter
#Following tests run on 23.11.26
#All passed successfully on 23.11.26 @00.56
def test_machine_map_basic():
    source = "fn(x){x* 11}.map  -> [14,13]"
    assert run_machine(source)[0] == run(source)[0]
    assert run_machine(source)[0] == [154, 143]

def test_machine_filter_basic():
    source = "fn(x){x>13}.filter -> [11,14,13]"
    assert run_machine(source)[0] == run(source)[0]
    assert run_machine(source)[0] == [14]

def test_machine_map_partial_trace():
    source = "fn(x){x}.map"
    assert run_machine(source)[0].name == run(source)[0].name
    assert len(run_machine(source)[0].args) == len(run(source)[0].args)


#Step tests (run only through the machine)

#Following tests ran on 2.11.26
#All tests successfully passed on 2.11.26 @ 00.02 am


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

#Following tests re-run on 8.11.26
#Test failed on 8.11.26 @20.38
#Test updated to reflect new CEK x RPN hybrid architecture, as failure was due it testing a no loger existing feature
#Test reran on 8.11.26
#Test passed successfully @20.45
def test_step_binop_pushes_right_frame():
    node = BinOp("+", Number(1,0,0), Lambda("x", [], 0, 0), 0,0)
    control, env, kont = step(node, {}, [])
    assert control.value == 1
    assert isinstance(kont[0], BinOpR)
    assert kont[0].op == "+"
    assert isinstance(kont[0].rightExpr, Lambda)

#Following tests run on 8.11.26
#All successfully passed on 8.11.26 @20.45
def test_step_arith_uses_rpn():
    node = BinOp("+", Number(1,0,0), Number(2,0,0), 0,0)
    control, env, kont = step(node, {}, [])
    assert control == 3
    assert not kont




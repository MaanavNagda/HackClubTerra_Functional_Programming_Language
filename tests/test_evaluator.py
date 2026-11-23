#117/117 tests successfuly
#Full test suite reran on 15.11.26 @10.43, 98 passed successfully, 4 (test_let_sequence, test_line_commit, test_comment_only_line, test_token_positions) failed, tests need updating because of the newline fix.
#Full test suite reran on 15.11.26 @11.02, all passed successfully

from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import run_program
from src.tokens import TokenType
from src.ast_nodes import If, Let, Bool, FnDef, Call, Var, BinOp, Number, Lambda, Str, List, Checkpoint, Rewind
import pytest
#Helper function
def run(source):
    return run_program(Parser(Lexer(source).tokenize()).parse_program(), {})


                 
#Tests on evalutor

#Following tests run on 23.10.26
#All passed successfully on 23.10.26 @20.10pm
def test_let_binding():
    result, env = run("let x = 5\nx+3")
    assert result == 8 and env["x"] == 5

def test_precedence_value():
    result, env = run("1 + 2 * 3")
    assert result == 7

def test_chained_lets():
    result, env = run("let x = 5\n let y = x * 2\ny-x")
    assert result == 5

def test_undefined_variable():
    with pytest.raises(Exception):
        run("x+1")

def test_division_by_zero():
    with pytest.raises(Exception):
        run("4/0")


##Evaluator tests for conditionals and comparisons
#Following Tests run on 26.10.26
#All passsed successfully on 26.10.26 @01.50am
def test_if_true_branch():
    result, env = run("if 14 > 13 then 11 else 12")
    assert result == 11

def test_if_false_branch():
    result, env = run("if 13 > 14 then 11 else 12")
    assert result == 12

def test_else_if_chain():
    result, env = run("if 13>14 then 11 elseif 16>12 then 8 else 21")
    assert result == 8

def test_if_no_else():
    result, env = run("if 13>14 then 11")
    assert result is None

def test_each_comparison():
    result, env = run("3==3")
    assert result is True
    result, env = run("3!=4")
    assert result is True
    result, env = run("13<14")
    assert result is True
    result, env = run("14>13")
    assert result is True
    result, env = run("14 <=14")
    assert result is True
    result, env = run("13>=13")
    assert result is True


##Evaluator tests on Booleans
#Following tests run on 26.10.26
#All passed succesfully on 26.10.26 @02.10am
def test_bool_evaluates_to_self():
    result, env = run("true")
    assert result is True
    result, env = run("false")
    assert result is False


def test_if_with_bool_literal():
    result, env = run("if true then 13 else 14")
    assert result == 13
    result, env = run("if false then 13 else 14")
    assert result == 14

def test_bool_variable_as_condition():
    result, env = run("let b = 13 == 13\nif b then 11 else 14")
    assert result == 11



#Evaluator tests on functions
#Following tests run on 1.11.26
#All passed succesfully on 1.11.26 @ 15.59
def test_simple_call():
    result, env, = run("fn add13(x){x+13}\nadd13 ->14")
    assert result == 27

def test_body_last_expr():
    result, env = run("fn f(x){let y = x * 13\n y + 14}\n f ->11")
    assert result == 157

def test_closure_capture():
    result, env = run("let a = 13\n fn f(x){x + a}\nf -> 14")
    assert result == 27

def test_param_is_local():
    result, env = run("let y = 13\nfn f(x){let y = x\n y} \nf -> 14\ny")
    assert result == 13

def test_recursion():
    result, env = run("fn fact(n){if n == 0 then 1 else n * (fact -> (n-1))}\nfact->11")
    assert result == 11*10* 9*8*7*6*5*4*3*2*1

def test_call_non_function():
    with pytest.raises(Exception):
        run("14 -> 13")

#Evaluator tests on Lambda function feature
#Following tests ran on 1.11.26
#All successfully passed on 1.11.26 @ 17.27pm
def test_basic_input():
    result, env = run("let f = fn(x){x+13}\nf -> 14")
    assert result == 27

def test_capture():
    result, env = run("let a = 14\n let f = fn(x){x*a}\n f->13")
    assert result == 182

def test_immediate_call():
    result, env = run("fn(x){x*11} -> 13")
    assert result == 143

def test_first_class_arg():
    result, env = run("fn apply(f){f->11}\n apply -> fn(x){x*14}")
    assert result == 154

def test_currying():
    result, env = run("fn adder(x){fn(y){x+y}}\n (adder -> 14) ->11")
    assert result == 25

def test_the_letBound_recursion():
    result, env = run("let fact = fn(n){if n == 0 then 1 else n * (fact -> (n-1))}\n fact -> 13")
    assert result == 13 * 12 * 11 * 10 * 9 * 8 * 7 * 6 * 5 * 4 * 3 * 2 * 1

def test_param_shadows_outlier():
    result, env = run("let x = 13\n let f = fn(x){x+14}\nf->11\nx")
    assert result == 13

def test_multi_statement_body():
    result, env = run("let f = fn(x){let y = x * 11\n y + 13}\n f -> 14")
    assert result == 167


#Evaluator tests on pipeline feature
#Following tests ran on 1.11.26
#All passed successfully on 1.11.26 @20.06pm
def test_pipeline_simple():
    result, env = run("13 |> fn(x){x+14}")
    assert result == 27

def test_pipeline_chain():
    result, env = run("13 |> fn(x){x*14} |> fn(x){x-11}")
    assert result == 171

def test_named_fun():
    result, env = run("fn double(x){x*2}\n 13 |> double")
    assert result == 26

def test_pipe_into_let():
    result, env = run("let out = 13 |> fn(x){x*11}\n out")
    assert result == 143


#Evaluator tests on unary minus
#Tests ran on 7.11.26
#All tests passed successfully on 7.11.26 @ 18.41
def test_negative_number():
    result, env = run("-14")
    assert result == -14

def test_negative_multiplication():
    result, env = run("14 * -1")
    assert result == -14

def test_negative_number_multiplication():
    result, env = run("-13 * 2")
    assert result == -26

def test_both_negative_multiplication():
    result, env = run("-13 * -3")
    assert result == 39

def test_assignment():
    result, env = run("let x = -14\n x")
    assert result == -14

def test_addition():
    result, env = run("13 -- 14")
    assert result == 27

#Test ran on 7.11.26
#Test failed on 7.11.26 @18.41
#Test re-ran on 7.11.26
#Test passed successfully on 7.11.26 @18.44 --> error in test function fixed
def test_function():
    result, env = run("fn id(x){x}\nid -> -14")
    assert result == -14


#Evaluator tests on print function
#Following tests ran on 7.11.26
#All passed successfully on 7.11.26 @13.13
def test_print_value():
    result, env = run("print -> 14")
    assert result == 14

def test_print_pipeline():
    result, env = run_program(Parser(Lexer("13|> print").tokenize()).parse_program(),{})
    assert result == 13

def test_print_let():
    result, env = run_program(Parser(Lexer("let p = print\n p -> 14").tokenize()).parse_program(), {})
    assert result == 14

def test_print_function():
    result, env = run_program(Parser(Lexer("fn apply(f){f->11}\napply->print").tokenize()).parse_program(), {})
    assert result == 11

def test_print_return_value_behaviour_pipeline():
    result, env = run_program(Parser(Lexer("13|> print |> fn(z){z+11}").tokenize()).parse_program(), {})
    assert result == 24

def test_print_return_value_behaviour_precedence():
    result, env = run_program(Parser(Lexer("(print -> 14) + 11").tokenize()).parse_program(), {})
    assert result == 25 #14 outputted, returns 25

def test_print_return_value_behaviour_let():
    result, env = run_program(Parser(Lexer("let x = print ->14\n x * 11").tokenize()).parse_program(), {})
    assert result == 154 #outputs 14, returns 154

def test_print_argument_evaluation_addition():
    result, env = run_program(Parser(Lexer("print -> 14 + 13").tokenize()).parse_program(), {})
    assert result == 27 #both output and returned value is 27

def test_print_argument_evaluation_conditionals():
    result, env = run_program(Parser(Lexer("print -> 14 > 11").tokenize()).parse_program(), {})
    assert result == True

def test_print_argument_evaluation_unary_minus():
    result, env = run_program(Parser(Lexer("print -> -14").tokenize()).parse_program(), {})
    assert result == -14

def test_print_inside_function():
    result, env = run_program(Parser(Lexer("fn f(x){print->x}\n f->14").tokenize()).parse_program(), {})
    assert result == 14

def test_print_inside_conditional_branch():
    result, env = run_program(Parser(Lexer("if 14>11 then print -> 13 else print ->11").tokenize()).parse_program(), {})
    assert result == 13

def test_print_inside_concitional_branch_false():
    result, env = run_program(Parser(Lexer("if 11>14 then print -> 13 else print ->11").tokenize()).parse_program(), {})
    assert result == 11

def test_print_multiple_times(): #test number 100!!
    result, env = run_program(Parser(Lexer("print ->14\n print->11").tokenize()).parse_program(), {})
    assert result == 11 #outputs both, returns just 11

#Following test rerun on 8.11.26
#Test failed on 8.11.26 @ 21.14
#This is because this is no longer a feature, as let print = is no longer valid. This was to test that user binding would win when reserved hadnt been implemented, but now it has been implemented, it is failing as it should
#Therefore, test will simply be commented out, as it has served its purpose, and is no longer valid.
#def test_print_shadowing():
 #   result, env = run_program(Parser(Lexer("let print = fn(x){x * 11}\n print -> 13").tokenize()).parse_program(), {})
  #  assert result == 143 #user binding should win

#Evaluator test on reserving builtin keywords
#Following tests run on 8.11.26
#Tests passed successfully on 8.11.26 @21.16
def test_cannot_redefine_builtin_let():
    with pytest.raises(Exception):
        run_program(Parser(Lexer("let print = 5").tokenize()).parse_program(), {})

def test_cannot_redefine_builtin_function():
    with pytest.raises(Exception):
        run_program(Parser(Lexer("fn print(x){x}").tokenize()).parse_program(), {})

def test_builtin_still_capable():
    result, env = run_program(Parser(Lexer("print ->14").tokenize()).parse_program(), {})
    assert result == 14


 
#Tests on main (general stuff)
#Test failed on 23.10.26 @21.30pm
#Error fixed, test rerun, and test passed successfully on 23.10.26 @21.35pm
def test_nested_parens():
    result, env = run("(1+2) * 3")
    assert result == 9

#Test passed successfully on 23.10.26 @21.30pm
def test_shadowing():
    result, env = run("let x = 4\n let x = x + 1 \nx")
    assert result == 5



#Evaluator tests on strings
#Following tests run on 15.11.26
#All passed successfully on 15.11.26 @20.14
def test_string_eval():
    result, env = run_program(Parser(Lexer("\"fourteen\"").tokenize()).parse_program(), {})
    assert result == "fourteen"

def test_string_string_concat():
    result, env = run_program(Parser(Lexer("\"fourteen\" + \"thirteen\"").tokenize()).parse_program(), {})
    assert result == "fourteenthirteen"

def test_string_number_concat():
    result, env = run_program(Parser(Lexer("\"fourteen\" + 13").tokenize()).parse_program(), {})
    assert result == "fourteen13"

def test_number_string_concat():
    result, env = run_program(Parser(Lexer("14 + \"thirteen\"").tokenize()).parse_program(), {})
    assert result == "14thirteen"

def test_number_number_addition_still_works():
    result, env = run_program(Parser(Lexer("14 + 14").tokenize()).parse_program(), {})
    assert result == 28

def test_number_number_string_concat():
    result, env = run_program(Parser(Lexer("\"14\" + \"13\"").tokenize()).parse_program(), {})
    assert result == "1413"

def test_string_let():
    result, env = run_program(Parser(Lexer("let s= \"fourteen\"\n s + \"thirteen\"").tokenize()).parse_program(), {})
    assert result == "fourteenthirteen"

def test_string_as_call_arg():
    result, env = run_program(Parser(Lexer("fn shout(s){s + \"fourteen\"}\n shout -> \"thirteen\"").tokenize()).parse_program(), {})
    assert result == "thirteenfourteen"


#Evaluator tests on lists
#Following tests run on 15.11.26
#All passed successfully on 15.11.26 @23.37
def test_list_eval():
    result, env = run_program(Parser(Lexer("[13,14]").tokenize()).parse_program(), {})
    assert result == [13,14]

def test_list_heterogenous_eval():
    result, env= run_program(Parser(Lexer("[14, \"thirteen\", true]").tokenize()).parse_program(), {})
    assert result == [14, "thirteen", True]

def test_list_nested_eval():
    result, env = run_program(Parser(Lexer("[[11], [13], [14]]").tokenize()).parse_program(), {})
    assert result == [[11], [13], [14]]

def test_list_computed_elements():
    result, env = run_program(Parser(Lexer("[12 + 16, 13 * 11]").tokenize()).parse_program(), {})
    assert result == [28, 143]

def test_list_env():
    result, env = run_program(Parser(Lexer("let x = 14\n[x,x+13]").tokenize()).parse_program(), {})
    assert result == [14,27]

def test_list_list_concat():
    result, env = run_program(Parser(Lexer("[11] + [14]").tokenize()).parse_program(), {})
    assert result == [11,14]

def test_list_eq_true():
    result, env = run_program(Parser(Lexer("[11, 14] == [11, 14]").tokenize()).parse_program(), {})
    assert result == True

def test_list_eq_false():
    result, env = run_program(Parser(Lexer("[11, 13] == [11, 14]").tokenize()).parse_program(), {})
    assert result == False


#Evaluator tests on appending to lists
#Following tests run on 16.11.26
#All passed successfully on 16.11.26 @01.58
def test_append_lists():
    result, env= run_program(Parser(Lexer("[11,13] ++ [14]").tokenize()).parse_program(), {})
    assert result == [11,13,14]

def test_append_number_right():
    result, env = run_program(Parser(Lexer("[11] ++ 13").tokenize()).parse_program(), {})
    assert result == [11, 13]

def test_apend_number_left():
    result, env = run_program(Parser(Lexer("13 ++ [14]").tokenize()).parse_program(), {})
    assert result == [13,14]

def test_append_numbers():
    result, env= run_program(Parser(Lexer("13++14").tokenize()).parse_program(), {})
    assert result ==[13,14]

def test_append_new_list():
    result, env = run_program(Parser(Lexer("13++[]").tokenize()).parse_program(), {})
    assert result == [13]

def test_append_mixed_list_to_list():
    result, env = run_program(Parser(Lexer("13 ++[11] ++ \"14\" ++ true").tokenize()).parse_program(), {})
    assert result == [13, 11, "14", True]

def test_append_mixed_list():
    result, env= run_program(Parser(Lexer("13++11++\"14\" ++ true").tokenize()).parse_program(), {})
    assert result ==[13, 11, "14", True]

def test_append_precedence():
    result, env = run_program(Parser(Lexer("13 ++ 11 + 14").tokenize()).parse_program(), {})
    assert result == [13,25]

def test_apend_strings():
    result, env = run_program(Parser(Lexer("\"13\"++\"14\"").tokenize()).parse_program(), {})
    assert result == ["13", "14"]

def test_append_let():
    result, env  = run_program(Parser(Lexer("let xs = [11] \n xs ++ [13]").tokenize()).parse_program(), {})
    assert result == [11, 13]


#Evalutator tests on checkpoints and rewinds
#Following tests run on 21.11.26
#All passed successfully on 21.11.26 @00.05
def test_checkpoint_multiline():
    result, env = run_program(Parser(Lexer("let x=11\ncheckpoint\nlet y = x * 13\ny").tokenize()).parse_program(), {})
    assert result == 143

def test_checkpoint_rewind():
    result, env = run_program(Parser(Lexer("let x = 11\ncheckpoint\nlet x = 13\nrewind\nx").tokenize()).parse_program(), {})
    assert result == 11

def test_checkpoint_persistance():
    result, env = run_program(Parser(Lexer("let x = 11 \ncheckpoint \nlet y = 13\nrewind \n let x = 14\n rewind\n x").tokenize()).parse_program(), {})
    assert result == 11

def test_standalone_rewind():
    with pytest.raises(Exception):
        run_program(Parser(Lexer("rewind").tokenize()).parse_program(), {})

def test_checkpoint_overflow():
    with pytest.raises(Exception):
        source = "checkpoint\n"
        x = 0
        while x!=101:
            source = source + "checkpoint\n"
            x +=1 
        run_program(Parser(Lexer(source).tokenize()).parse_program(), {})

def test_checkpoint_functions():
    result, env = run_program(Parser(Lexer("fn f(x){checkpoint\nlet y = x * 13\ny}\nf -> 11").tokenize()).parse_program(), {})
    assert result == 143


#Evaluator tests on effect vocabulary
#Following tests run on 22.11.26
#All passed successfully on 22.11.26 @15.57
def test_page_effect_returns_description():
    result, env = run_program(Parser(Lexer("page! -> \"team-oncall\"").tokenize()).parse_program(), {})
    assert result.name == "page!"
    assert result.args == ("team-oncall",)

def test_dispatch_builtin():
    result, env = run_program(Parser(Lexer("dispatch! -> \"u7\"").tokenize()).parse_program(), {})
    assert result.name == "dispatch!"

def test_reroute_builtin():
    result, env = run_program(Parser(Lexer("reroute!->\"u7\"").tokenize()).parse_program(), {})
    assert result.name == "reroute!"

def test_page_builtin():
    result, env = run_program(Parser(Lexer("page!->\"u7\"").tokenize()).parse_program(), {})
    assert result.name == "page!"

def test_write_builtin():
    result, env = run_program(Parser(Lexer("write!->\"u7\"").tokenize()).parse_program(), {})
    assert result.name == "write!"

def test_commit_single_effect():
    result, env =  run_program(Parser(Lexer("commit! -> (page! -> \"team\")").tokenize()).parse_program(), {})
    assert result.name == "page!"

def test_effect_builtin_reserved():
    with pytest.raises(Exception):
        results, env= run_program(Parser(Lexer("let page! = 13").tokenize()).parse_program(), {})

def test_effect_is_value():
    result, env = run_program(Parser(Lexer("let fx = page! -> \"x\"").tokenize()).parse_program(), {})
    assert result.name == "page!"



#Following tests run on 22.11.26
#All tests failed on 22.11.26 @15.57
#Fixed issue with the test suite formatting
#Following tests rerun on 22.11.26
#All passed successfully on 22.11.26 @16.06
def test_commit_effect_list():
    result, env = run_program(Parser(Lexer("commit! -> [page! ->\"a\", dispatch! -> \"u7\"]").tokenize()).parse_program(), {})
    assert result[0].name == "page!"
    assert result[1].name == "dispatch!"



#Evaluator tests on dot
#Following tests run on 22.11.26
#All passed successfully on 22.11.26 @21.22
def test_dot_list_print_eval():
    result, env = run_program(Parser(Lexer("[13,14].print").tokenize()).parse_program(), {})
    assert result == [13,14]

def test_dot_function_print_eval():
    result, env = run_program(Parser(Lexer("fn(x){x+13}.print").tokenize()).parse_program(), {})
    assert result is not None

def test_dot_number_name_rejection():
    with pytest.raises(Exception):
        run_program(Parser(Lexer("13.print").tokenize()).parse_program(), {})

def test_dot_bool_name_rejected():
    with pytest.raises(Exception):
        run_program(Parser(Lexer("true.print").tokenize()).parse_program(), {})

def test_dot_string_name_rejection():
    with pytest.raises(Exception):
        run_program(Parser(Lexer("\"13\".print").tokenize()).parse_program(), {})


#Following tests run on 22.11.26
#All tests failed on 22.11.26 @21.22
#Fixed error with test, as floats are rounded, so assert failed due to python rounding
#Following tests rerun on 22.11.26
#All passed successfully on 22.11.26 @21.27
def test_dot_float_eval():
    result, env = run_program(Parser(Lexer("13.5 + 14.25").tokenize()).parse_program(), {})
    assert result == 27.75



#Evaluator tests on map & filter
#Following tests run on 23.11.26
#All passed successfully on 23.11.26 @00.57
def test_map_basic():
    result, env = run_program(Parser(Lexer("fn(x){x * 11}.map -> [13,14]").tokenize()).parse_program(), {})
    assert result == [143,154]

def test_map_with_named_function():
    result, env = run_program(Parser(Lexer("let undecouple = fn(x){x * 11} \n undecouple.map -> [11,14] ").tokenize()).parse_program(), {})
    assert result == [121,154]

def test_partial_alone():
    result, env = run_program(Parser(Lexer("fn(x){x}.map").tokenize()).parse_program(), {})
    assert result.name == "<map>"
    assert len(result.args) == 1

def test_map_rejects_non_list():
    with pytest.raises(Exception):
        run_program(Parser(Lexer("fn(x){x}.map ->14").tokenize()).parse_program(), {})

def test_map_rejects_non_function():
    with pytest.raises(Exception):
        run_program(Parser(Lexer("13.map").tokenize()).parse_program(), {})

def test_filter_basic():
    result, env = run_program(Parser(Lexer("fn(x){x>13}.filter ->[11,14,13]").tokenize()).parse_program(), {})
    assert result == [14]

def test_filter_all():
    result, env = run_program(Parser(Lexer("fn(x){x>13}.filter -> [14,143,1432]").tokenize()).parse_program(), {})
    assert result == [14,143,1432]

def test_filter_none():
    result, env = run_program(Parser(Lexer("fn(x){x>13}.filter -> [8,11,12]").tokenize()).parse_program(), {})
    assert result == []

def test_filter_rejects_non_list():
    with pytest.raises(Exception):
        run_program(Parser(Lexer("fn(x){x}.filter -> \"12\"").tokenize()).parse_program(), {})

def test_map_arrow_banned():
    with pytest.raises(Exception):
        run_program(Parser(Lexer("map -> fn(x){x} -> [11,13]").tokenize()).parse_program(), {})

def test_map_pipeline_banned():
    with pytest.raises(Exception):
        run_program(Parser(Lexer("[11,12] |> map -> fn(x){x}").tokenize()).parse_program(), {})

def test_filter_arrow_banned():
    with pytest.raises(Exception):
        run_program(Parser(Lexer("filter -> fn(x){x}->[11]").tokenize()).parse_program(), {})

def test_filter_pipeline_banned():
    with pytest.raises(Exception):
        run_program(Parser(Lexer("[11] |> filter -> fn(x){x}").tokenize()).parse_program(), {})
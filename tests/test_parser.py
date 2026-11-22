#37/37 tests successfuly
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
                 



   

#Tests on the Parser

#Following tests run on 23.10.26
#All passed successfully on 23.10.26 @20.10pm
def test_precedence_tree():
    ast = Parser(Lexer("1 + 2 * 3").tokenize()).parse_program()
    root = ast[0]
    assert root.op == "+"
    assert root.left.value == 1
    assert root.right.op == "*"
    assert root.right.left.value == 2
    assert root.right.right.value == 3


##Parser tests on conditions and  double character operators
#Following tests run on 26.10.26 
#All passed successfull on 26.10.26 @01.29am
def test_if_node_shape():
    ast = Parser(Lexer("if 14 > 13 then 11 else 12").tokenize()).parse_program()
    root = ast[0]
    assert isinstance(root, If)
    assert root.cond.op == ">"
    assert root.then.value == 11
    assert root.else_branch.value == 12

def test_elseif_is_nested_if():
    ast = Parser(Lexer("if a then 13 elseif b then 14 else 11").tokenize()).parse_program()
    root = ast[0]
    assert isinstance(root, If)
    assert isinstance(root.else_branch, If)
    assert root.else_branch.then.value == 14
    assert root.else_branch.else_branch.value == 11

def test_comparison_binds_looser_than_addition():
    ast = Parser(Lexer("1 + 2 == 3").tokenize()).parse_program()
    root = ast[0]
    assert root.op == "=="
    assert root.left.op == "+"

def test_if_without_else_is_none():
    ast = Parser(Lexer("if a then 13").tokenize()).parse_program()
    assert ast[0].else_branch is None

def test_if_inside_expression():
    ast = Parser(Lexer("let y = if x > 14 then 13 else 11 \ny").tokenize()).parse_program()
    assert isinstance(ast[0], Let)
    assert isinstance(ast[0].value, If)

##Parser tests on Boolean
#Following tests run on 26.10.26
#All passed successfully on 26.10.26 @20.10am
def test_bool_nodes():
    ast = Parser(Lexer("true").tokenize()).parse_program()
    assert isinstance(ast[0], Bool) and ast[0].value is True

#Parser tests on functions
#Following tests run on 1.11.26
#All passed succesfully on 1.11.26 @ 15.59pm
def test_fndef_shape():
    ast = Parser(Lexer("fn add14(x){x+14}").tokenize()).parse_program()
    root = ast[0]
    assert isinstance(root, FnDef)
    assert root.name == "add14"
    assert root.param == "x"
    assert root.body[0].op == "+"

def test_fndef_multistatement():
    ast = Parser(Lexer("fn f(x){let y = x + 13\ny}").tokenize()).parse_program()
    root = ast[0]
    assert len(root.body) == 2
    assert isinstance(root.body[0], Let)
    assert isinstance(root.body[1], Var)

def test_call_node():
    ast = Parser(Lexer("add14 -> 13").tokenize()).parse_program()
    root = ast[0]
    assert isinstance(root, Call)
    assert root.func.name == "add14"
    assert root.arg.value == 13

def test_call_lef_assoc():
    ast = Parser(Lexer("f -> 13 -> 14").tokenize()).parse_program()
    root = ast[0]
    assert isinstance(root, Call)
    assert isinstance(root.func, Call)

def test_call_arg_expr():
    ast = Parser(Lexer("add -> 13 + 14").tokenize()).parse_program()
    root = ast[0]
    assert root.arg.op == "+"

#Parser tests on lambda function feature
#Following tests ran on 1.11.26
#All passed sauccessfully on 1.11.26 @17.27pm
def test_statement_level_lambda():
    ast = Parser(Lexer("fn(x){x+1}").tokenize()).parse_program()
    root = ast[0]
    assert root.param == "x"
    assert isinstance(root.body[0], BinOp)
    assert root.body[0].op == "+"

def test_named_def():
    ast = Parser(Lexer("fn f(x){x}").tokenize()).parse_program()
    root = ast[0]
    assert isinstance(root, FnDef)
    assert not isinstance(root, Lambda)

def test_lambda_RHS():
    ast = Parser(Lexer("let f = fn(x){x}").tokenize()).parse_program()
    root = ast[0]
    assert isinstance(root, Let)
    assert isinstance(ast[0].value, Lambda)

def test_lambda_call_arg():
    ast = Parser(Lexer("apply -> fn(x){x}").tokenize()).parse_program()
    root = ast[0]
    assert isinstance(root, Call)
    assert isinstance(root.arg, Lambda)

def test_immediate_call():
    ast = Parser(Lexer("fn(x){x} -> 14").tokenize()).parse_program()
    root = ast[0]
    assert isinstance(root, Call)
    assert isinstance(root.func, Lambda)

def test_nested_in_body():
    ast = Parser(Lexer("fn outer(x){fn(y){y}}").tokenize()).parse_program()
    root = ast[0]
    assert isinstance(ast[0].body[0], Lambda)


#Parser tests on pipeline feature
#Following tests ran on 1.11.26
#All passed successfully on 1.11.26 @20.06pm
def test_pipeline_shape():
    ast = Parser(Lexer("x|> f").tokenize()).parse_program()
    root = ast[0]
    assert isinstance(root, Call)
    assert isinstance(root.func, Var)
    assert root.arg.name == "x"
    assert root.func.name == "f"
    assert isinstance(root.arg, Var)

def test_pipeline_left_assoc():
    ast = Parser(Lexer("x|>f|>g").tokenize()).parse_program()
    root = ast[0]
    assert isinstance(root.arg, Call)
    assert root.func.name == "g"

def test_rhs_call():
    ast = Parser(Lexer("x |> f ->14").tokenize()).parse_program()
    root = ast[0]
    assert isinstance(root.func, Call)
    assert root.arg.name == "x"

#Parser tests on unary minus
#Following tests ran on 7.11.26
#All passed successfully on 7.11.26 @18.41
def test_unary_minus_node():
    ast = Parser(Lexer("-14").tokenize()).parse_program()
    root = ast[0]
    assert isinstance(root, BinOp)
    assert root.op == "-"
    assert isinstance(root.left, Number)
    assert root.left.value == 0
    assert isinstance(root.right, Number)
    assert root.right.value == 14

def test_minus_on_var():
    ast = Parser(Lexer("-x").tokenize()).parse_program()
    root = ast[0]
    assert isinstance(root.right, Var)
    assert root.right.name == "x"

def minus_inside_multiplication():
    ast = Parser(Lexer("14 * -1").tokenize()).parse_program()
    root = ast[0]
    assert root.op == "+"
    assert isinstance(root.right, BinOp)
    assert root.right.op == "-"

def binary_minus():
    ast = Parser(Lexer("13 -  -14").tokenize()).parse_program()
    root = ast[0]
    assert root.op == "-"
    assert root.left.value == 13
    assert isinstance(root.right, BinOp)

def double_negation():
    ast = Parser(Lexer("--14").tokenize()).parse_program()
    root = ast[0]
    assert isinstance(root, BinOp)
    assert isinstance(root.right, BinOp)

#Parser tests on strings
#Following tests run on 15.11.26 
#All passed successfully on 15.11.26 @20.14
def test_string_node():
    ast = Parser(Lexer("\"eleven\"").tokenize()).parse_program()
    root = ast[0]
    assert isinstance(root, Str)
    assert root.value == "eleven"


#Parser tests on lists
#Following tests run on 15.11.26
#All passed successfully on 15.11.26 @23.37
def test_list_node():
    ast = Parser(Lexer("[11,14]").tokenize()).parse_program()
    root = ast[0]
    assert isinstance(root, List)
    assert [e.value for e in root.elements] == [11,14]

def test_list_empty_node():
    ast = Parser(Lexer("[]").tokenize()).parse_program()
    root = ast[0]
    assert isinstance(root, List)
    assert root.elements == []

def test_list_heterogeneous():
    ast = Parser(Lexer("[13, \"fourteen\", true]").tokenize()).parse_program()
    root = ast[0]
    assert isinstance(root, List)
    assert [e.value for e in root.elements] == [13, "fourteen", True]

def test_list_missing_comma():
    with pytest.raises(Exception):
        Parser(Lexer("[11 14]").tokenize()).parse_program()

def test_list_trailing_comma(): #At the moment this is treated as an error, later will be tolerated
    with pytest.raises(Exception):
        Parser(Lexer("[13,]").tokenize()).parse_program()


#Parser Tests on append
#Following tests run on 16.11.26
#All passed successfully on 16.11.26 @01.58
def test_append_node():
    ast = Parser(Lexer("[13] ++ [14]").tokenize()).parse_program()
    root = ast[0]
    assert isinstance(root, BinOp)
    assert isinstance(root.left, List)
    assert isinstance(root.right, List)
    assert root.op == "++"

def test_append_precendence_node():
    ast = Parser(Lexer("[11] ++ 12 + 13").tokenize()).parse_program()
    root = ast[0]
    assert isinstance(root, BinOp)
    assert root.op == "++"
    assert isinstance(root.right, BinOp)

def test_append_left_assoc():
    ast = Parser(Lexer("11 ++ 13 ++ 14").tokenize()).parse_program()
    root = ast[0]
    assert isinstance(root, BinOp)
    assert isinstance(root.left, BinOp)


#Parser tests on checkpoints and rewind
#Following tests run on 21.11.26
#All passed successfully on 21.11.26 @00.05
def test_checkpoint_rewind():
    ast = Parser(Lexer("checkpoint\nrewind").tokenize()).parse_program()
    root = ast[0]
    assert isinstance(root, Checkpoint)
    assert isinstance(ast[1], Rewind)

def test_checkpoint_function():
    ast = Parser(Lexer("fn f(x){checkpoint\nrewind\nx}").tokenize()).parse_program()
    root = ast[0]
    assert isinstance(root, FnDef)
    assert isinstance(root.body[1], Rewind)
    assert isinstance(root.body[0], Checkpoint)

def test_checkpoint_let():
    ast = Parser(Lexer("let x =5\ncheckpoint\nlet y = 2\nrewind\nx ").tokenize()).parse_program()
    root = ast[0]
    assert len(ast) == 5
    assert isinstance(ast[1], Checkpoint)
    assert isinstance(ast[3], Rewind)
    

#Parser tests on effect vocabulary
#Following tests run on 22.11.26
#All passed successfully on 22.11.26 @15.57
def test_effect_call_parses():
    ast = Parser(Lexer("page! -> \"team\"").tokenize()).parse_program()
    root = ast[0]
    assert isinstance(root, Call)
    assert root.func.name == "page!"

#Parser tests on dot
#Following tests run on 22.11.26
#All passed successfully on 22.11.26 @21.22
def test_dot_parses():
    ast = Parser(Lexer("x.print").tokenize()).parse_program()
    root= ast[0]
    assert isinstance(root.arg, Call)
    assert root.func.name == "print"
    assert root.arg.func.name == "<dot>"







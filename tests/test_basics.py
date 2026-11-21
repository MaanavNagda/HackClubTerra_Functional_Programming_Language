#147/147 tests successfuly
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

#Tests on Lexer

#Following tests run on 23.10.26
#All passed successfully on 23.10.26 @20.10pm
def test_keywork_boundary():
    tokens = Lexer("letter = 3").tokenize()
    assert tokens[0].type == TokenType.IDENT and tokens[0].value == "letter"


def test_identifier_with_digits():
    tokens = Lexer("x2_y").tokenize()
    assert tokens[0].type == TokenType.IDENT and tokens[0].value == "x2_y"

def test_empty_input():
    tokens = Lexer("").tokenize()
    assert len(tokens) == 1 and tokens[0].type == TokenType.EOF

def test_illegal_character():
    with pytest.raises(Exception):
        Lexer("5 $").tokenize()

#Following tests rerun on 15.11.26 
#All tests failed on 15.11.26 @10.43
#Fixed token error, as new token has been created, so assertion has to be updated
#Following tests rerun (3) on 15.11.26
#All tests failed on 15.11.26 @10.55
#Fixed ordering on the assertion, which was throwing the error
#Following tests rerun (4) on 15.11.26
#All passed successfully on 15.11.26 @11.02
def test_let_sequence():
    tokens = Lexer("let x = 5 + 3\nlet y = x * 2").tokenize()
    types = [t.type for t in tokens]
    assert types == [TokenType.LET, TokenType.IDENT, TokenType.EQUALS, TokenType.NUMBER,  TokenType.PLUS, TokenType.NUMBER,TokenType.NEWLINE,
                     TokenType.LET, TokenType.IDENT, TokenType.EQUALS, TokenType.IDENT, TokenType.STAR, TokenType.NUMBER, TokenType.EOF]
    assert tokens[1].value == "x"
    assert tokens[3].value == 5

##Lexer tests on two tokens
#Following tests run on 26.10.26
#All passed successfully on 26.10.26 @00:52am
def test_comparison_operators():
    tokens = Lexer("x == 14 != y >=13").tokenize()
    types = [t.type for t in tokens]
    assert types == [TokenType.IDENT, TokenType.EQEQ, TokenType.NUMBER, TokenType.NE, TokenType.IDENT, TokenType.GTE, TokenType.NUMBER, TokenType.EOF]
    

def test_single_equals_not_split(): #This is to make sure that in case of a double character operator, it is only counted once even if it is made up of two characters
    tokens = Lexer("x = 14").tokenize()
    assert tokens[1].type == TokenType.EQUALS

def test_single_lt_gt():
    tokens = Lexer("a < b > c").tokenize()
    assert tokens[1].type == TokenType.LT
    assert tokens[3].type == TokenType.GT

def test_if_keywords():
    tokens = Lexer("if x then y elseif z then b else a").tokenize()
    types = [t.type for t in tokens]
    assert types == [TokenType.IF, TokenType.IDENT, TokenType.THEN, TokenType.IDENT, TokenType.ELIF, TokenType.IDENT, TokenType.THEN, TokenType.IDENT, TokenType.ELSE, TokenType.IDENT,TokenType.EOF]

def test_booleans():
    tokens = Lexer("true != false").tokenize()
    types = [t.type for t in tokens]
    assert types == [TokenType.TRUE, TokenType.NE, TokenType.FALSE, TokenType.EOF]

##Lexer tests on Booleans
#Following tests run on 26.10.26
#All passed successfully on 26.10.26 @02.10am
def test_bool_literals():
    tokens = Lexer("true false").tokenize()
    types = [t.type for t in tokens]
    assert types == [TokenType.TRUE, TokenType.FALSE, TokenType.EOF]
    
#Lexer tests on comments
#Following tests run on 26.10.26
#All passed successfully on 26.10.25 @02.39am


def test_comment_at_EOF():
    tokens = Lexer("5;; trailing").tokenize()
    types = [t.type for t in tokens]
    assert types == [TokenType.NUMBER, TokenType.EOF]

def test_single_semi_colon_errors():
    with pytest.raises(Exception):
        Lexer("13; oops").tokenize()

def test_only_comment():
    tokens = Lexer(";;Just a comment lol").tokenize()
    types = [t.type for t in tokens]
    assert types == [TokenType.EOF]


#Following tests rerun on 15.11.26
#All tests failed on 15.11.26 @10.43
#Fixed missing token error, as a new token was created, so assertion needs to be updated
#Following tests rerun (3) on 15.11.26
#All passed successfully on 15.11.26 @10.55
def test_comment_only_line():
    tokens = Lexer(";; nothing here \n5").tokenize()
    types = [t.type for t in tokens]
    assert types == [TokenType.NEWLINE, TokenType.NUMBER, TokenType.EOF]

def test_line_comment():
    tokens = Lexer("let x = 13;;bind x\nx").tokenize()
    types = [t.type for t in tokens]
    assert types == [TokenType.LET, TokenType.IDENT, TokenType.EQUALS, TokenType.NUMBER, TokenType.NEWLINE, TokenType.IDENT, TokenType.EOF]


#Lexer tests on functions
#Following tests run on 1.11.26
#All passed succesfully on 1.11.26 @ 15.59pm
def test_fn_brace_tokens():
    tokens = Lexer("fn f(x){}").tokenize()
    types = [t.type for t in tokens]
    assert types == [TokenType.FN, TokenType.IDENT, TokenType.LPAREN, TokenType.IDENT, TokenType.RPAREN, TokenType.LBRACE, TokenType.RBRACE, TokenType.EOF]

def test_apply_token():
    tokens = Lexer("add14-> 14").tokenize()
    types = [t.type for t in tokens]
    assert types == [TokenType.IDENT, TokenType.APPLY, TokenType.NUMBER, TokenType.EOF]

def test_dash_not_apply():
    tokens = Lexer("a - 13").tokenize()
    types = [t.type for t in tokens]
    assert types == [TokenType.IDENT, TokenType.MINUS, TokenType.NUMBER, TokenType.EOF]


#Lexer tests on pipeline feature
#Following tests ran on 1.1.26
#All passed successfully on 1.11.26 @20.06pm
def test_pipe_token():
    tokens = Lexer("a|>b").tokenize()
    types = [t.type for t in tokens]
    assert types == [TokenType.IDENT, TokenType.PIPE, TokenType.IDENT, TokenType.EOF]

def test_bare_pipe_errors():
    with pytest.raises(Exception):
        Lexer("a|").tokenize()

def test_pipe_vs_apply():
    tokens = Lexer("a |> f -> 13").tokenize()
    types = [t.type for t in tokens]
    assert types == [TokenType.IDENT, TokenType.PIPE, TokenType.IDENT, TokenType.APPLY, TokenType.NUMBER, TokenType.EOF]


#Lexer tests on Strings
#Following tests run on 15.11.26 
#All tests failed on 15.11.26 @20.14
#Fixed error with the test suites themselves
#All tests rerun on 15.11.26
#All passed successfully on 15.11.26 @20.20
def test_string_token():
    tokens = Lexer("\"hello\"").tokenize()
    types = [t.type for t in tokens]
    assert types == [TokenType.STRING, TokenType.EOF]
    assert tokens[0].value == "hello"

def test_string_escape():
    tokens = Lexer("\"a\\\"b\"").tokenize()
    types = [t.type for t in tokens]
    assert tokens[0].value == "a\"b"
    assert types == [TokenType.STRING, TokenType.EOF]

def test_string_in_let():
    tokens = Lexer("let x = \"fourteen\"").tokenize()
    types = [t.type for t in tokens]
    assert types == [TokenType.LET, TokenType.IDENT, TokenType.EQUALS, TokenType.STRING, TokenType.EOF]
    

def test_string_unterminated():
    with pytest.raises(Exception):
        Lexer("\"thirteen").tokenize()


#Lexer tests of lists
#Following tests run on 15.11.26
#All passed successfully on 15.11.26 @23.37
def test_list_empty_tokens():
    tokens = Lexer("[]").tokenize()
    types = [t.type for t in tokens]
    assert types == [TokenType.LBRACKET, TokenType.RBRACKET, TokenType.EOF]

def test_list_tokens():
    tokens = Lexer("[11,13]").tokenize()
    types = [t.type for t in tokens]
    assert types == [TokenType.LBRACKET, TokenType.NUMBER, TokenType.COMMA, TokenType.NUMBER, TokenType.RBRACKET, TokenType.EOF]

def test_list_multiline():
    tokens = Lexer("[14,\n13]").tokenize()
    types = [t.type for t in tokens]
    assert types == [TokenType.LBRACKET, TokenType.NUMBER, TokenType.COMMA, TokenType.NUMBER, TokenType.RBRACKET, TokenType.EOF] #crucially, no TokenType.NEWLINE, as there is NOT supposed to be any newlines inside brackets during parsing

def test_list_multi_type():
    tokens = Lexer("[14, \" thirteen\", false]").tokenize()
    types = [t.type for t in tokens]
    assert types == [TokenType.LBRACKET, TokenType.NUMBER, TokenType.COMMA, TokenType.STRING, TokenType.COMMA, TokenType.FALSE, TokenType.RBRACKET, TokenType.EOF]


#Lexer tests on appending
#Following tests run on 16.11.26
#All passed successfully on 16.11.26 @01.58 
def test_append_token():
    tokens = Lexer("[11] ++ [13]").tokenize()
    types = [t.type for t in tokens]
    assert types == [TokenType.LBRACKET, TokenType.NUMBER, TokenType.RBRACKET, TokenType.APPEND, TokenType.LBRACKET, TokenType.NUMBER, TokenType.RBRACKET, TokenType.EOF]
    

def test_append_token_compact():
    tokens = Lexer("13 ++ 14").tokenize()
    types = [t.type for t in tokens]
    assert types == [TokenType.NUMBER, TokenType.APPEND, TokenType.NUMBER, TokenType.EOF]



#Lexer tests on Checkpoints & rewinding
#Following tests run on 21.11.26
#All passed successfully on 21.11.26 @00.05
def test_checkpoint_token():
    tokens = Lexer("checkpoint").tokenize()
    types = [t.type for t in tokens]
    assert types == [TokenType.CHECKPOINT, TokenType.EOF]

def test_checkpoint_rewind_tokens():
    tokens = Lexer("checkpoint\nrewind").tokenize()
    types = [t.type for t in tokens]
    assert types == [TokenType.CHECKPOINT, TokenType.NEWLINE, TokenType.REWIND, TokenType.EOF]




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
    






#Tests on positions

#Following tests run on 23.10.26
#All passed successfully on 23.10.26 @20.10pm
#Following tests rerun on 15.11.26
#All failed on 15.11.26 @10.43
#Fixed token error (as new token was added to the list)
#Following tests rerun (3) on 15.11.26
#All passed successfully on 15.11.26 @10.55pm
def test_token_positions():
    tokens = Lexer("let x = 5\nlet y =x ").tokenize()
    assert (tokens[5].line, tokens[5].col) == (2,1)

                 
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
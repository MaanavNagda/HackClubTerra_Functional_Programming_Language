#66 tests successfuly
from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import run_program
from src.tokens import TokenType
from src.ast_nodes import If, Let, Bool, FnDef, Call, Var, BinOp, Number, Lambda
import pytest
#Helper function
def run(source):
    return run_program(Parser(Lexer(source).tokenize()).parse_program(), {})

#Tests on Lexer

#Following tests run on 23.10.26
#All passed successfully on 23.10.26 @20.10pm
def test_let_sequence():
    tokens = Lexer("let x = 5 + 3\nlet y = x * 2").tokenize()
    types = [t.type for t in tokens]
    assert types == [TokenType.LET, TokenType.IDENT, TokenType.EQUALS, TokenType.NUMBER, TokenType.PLUS, TokenType.NUMBER,
                     TokenType.LET, TokenType.IDENT, TokenType.EQUALS, TokenType.IDENT, TokenType.STAR, TokenType.NUMBER, TokenType.EOF]
    assert tokens[1].value == "x"
    assert tokens[3].value == 5

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
def test_line_comment():
    tokens = Lexer("let x = 13;;bind x\nx").tokenize()
    types = [t.type for t in tokens]
    assert types == [TokenType.LET, TokenType.IDENT, TokenType.EQUALS, TokenType.NUMBER, TokenType.IDENT, TokenType.EOF]

def test_comment_only_line():
    tokens = Lexer(";; nothing here \n5").tokenize()
    types = [t.type for t in tokens]
    assert types == [TokenType.NUMBER, TokenType.EOF]

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







#Tests on positions

#Following tests run on 23.10.26
#All passed successfully on 23.10.26 @20.10pm
def test_token_positions():
    tokens = Lexer("let x = 5\nlet y =x ").tokenize()
    assert (tokens[4].line, tokens[4].col) == (2,1)

                 
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



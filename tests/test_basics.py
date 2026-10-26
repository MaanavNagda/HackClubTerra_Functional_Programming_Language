from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import run_program
from src.tokens import TokenType
from src.ast_nodes import If, Let
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



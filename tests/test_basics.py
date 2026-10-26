from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import run_program
from src.tokens import TokenType
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



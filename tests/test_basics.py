from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import run_program
from src.tokens import TokenType
import pytest

#Tests on Lexer

#Following tests run on 23.10.26
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


#Tests on the Parser

#Following tests run on 23.10.26
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
def test_token_positions():
    tokens = Lexer("let x = 5\nlet y =x ").tokenize()
    assert (tokens[4].line, tokens[4].col) == (2,1)

                 

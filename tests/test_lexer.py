#40/40 tests successfuly
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


#Lexer tests on effect vocabulary
#Following tests run on 22.11.26
#All passed successfully on 22.11.26 @15.57
def test_effect_bang_indetifier():
    tokens = Lexer("page!").tokenize()
    types = [t.type for t in tokens]
    assert types == [TokenType.IDENT, TokenType.EOF]
    assert tokens[0].value == "page!"

def test_effect_bang_not_equals():
    tokens = Lexer("a != b").tokenize()
    types = [t.type for t in tokens]
    assert types == [TokenType.IDENT, TokenType.NE, TokenType.IDENT, TokenType.EOF]



# Lexer tests on positions
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





#Lexer tests on dot
#Following tests run on 22.11.26
#All passed successfully on 22.11.26 @21.22
def test_dot_ident():
    tokens = Lexer("x.print").tokenize()
    types = [t.type for t in tokens]
    assert types == [TokenType.IDENT, TokenType.DOT, TokenType.IDENT, TokenType.EOF]

def test_dot_float():
    tokens = Lexer("13.14").tokenize()
    types = [t.type for t in tokens]
    assert types == [TokenType.NUMBER, TokenType.EOF]
    assert tokens[0].value == 13.14

def test_dot_number_name():
    tokens = Lexer("13.print").tokenize() #Note even though invalid, it stil lexilises, and so still a useful test to run
    types = [t.type for t in tokens]
    assert types == [TokenType.NUMBER, TokenType.DOT, TokenType.IDENT, TokenType.EOF]

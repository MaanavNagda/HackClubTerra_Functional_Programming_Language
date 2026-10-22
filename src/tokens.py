from enum import Enum, auto
from dataclasses import dataclass

class TokenType(Enum):
    #literals
    NUMBER = auto()
    IDENT = auto()

    #keywords (add as functionality is written)
    LET = auto()

    #operators
    PLUS = auto() #+
    MINUS = auto() #-
    STAR = auto() #*
    SLASH = auto() #/
    EQUALS = auto() #=


    #grouping
    LPAREN = auto() #(
    RPAREN = auto() #)

    EOF = auto()

@dataclass(frozen=True)
class Token:
    type: TokenType
    value: object
    line: int
    col: int

#keyword table so the lexer can differentiate keywords from variables
KEYWORDS = {"let": TokenType.LET}


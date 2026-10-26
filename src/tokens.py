from enum import Enum, auto
from dataclasses import dataclass
#This is about the actual vocabulary and syntax of the language, and therefore its token types and record, as well as the look up tables that the lexer and parser use


#TokenType is the categories of the tokens, not just the text itself. This is how the input is split into the different types of things it can be, so the language can process them
#Enum + auto() is sufficient to give each thing a unique ID automatically without having to manually enter one in
class TokenType(Enum):
    #literals and names
    NUMBER = auto()  #For example "13" or "14"
    IDENT = auto()  #For example "x"or "banana" or "comet" 

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

    EOF = auto() #This is the end of input marker, and it is the parser's stop signal, telling it that there is no more input left to parse


#A token is its category, its payload, and where it was in the source.
#A value is either an integer (for numbers), or a name (for identifiers). Simple operators just carry their character itself.
#Line/col are there so that errors can point to the exact source position of the error, making it a lot more identifiable (and so a lot easier to fix) than a generic there is an error message.
@dataclass(frozen=True)
class Token:
    type: TokenType
    value: object
    line: int
    col: int

#keyword table so the lexer can differentiate keywords from variables
#So far, the input of let becomes LET category, and everything else stays as the IDENT category
KEYWORDS = {"let": TokenType.LET}

#A dictionary of single chars that are their own token type (mainly the different mathematical operators and symbols)
SINGLE_CHAR_TOKENS = {
    '+': TokenType.PLUS,
    '-': TokenType.MINUS,
    '*': TokenType.STAR,
    '/': TokenType.SLASH,
    '=': TokenType.EQUALS,
    '(': TokenType.LPAREN,
    ')': TokenType.RPAREN
}

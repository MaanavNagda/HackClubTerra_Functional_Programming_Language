from enum import Enum, auto
from dataclasses import dataclass
#This is about the actual vocabulary and syntax of the language, and therefore its token types and record, as well as the look up tables that the lexer and parser use


#TokenType is the categories of the tokens, not just the text itself. This is how the input is split into the different types of things it can be, so the language can process them
#Enum + auto() is sufficient to give each thing a unique ID automatically without having to manually enter one in
class TokenType(Enum):
    #literals and names
    NUMBER = auto()  #For example "13" or "14"
    IDENT = auto()  #For example "x"or "banana" or "comet" 
    STRING = auto() #For example "Foxy" or "<14 :$ :&"

    #keywords (add as functionality is written)
    LET = auto()
    IF = auto()
    ELSE = auto()
    ELIF = auto()
    THEN = auto()
    TRUE = auto()
    FALSE = auto()
    CHECKPOINT = auto()
    REWIND = auto()

    #operators
    PLUS = auto() #+
    MINUS = auto() #-
    STAR = auto() #*
    SLASH = auto() #/
    EQUALS = auto() #=

    #comparison operators
    LT = auto()
    GT = auto()
    LTE = auto()
    GTE = auto()
    EQEQ = auto()
    NE = auto()

    #grouping
    LPAREN = auto() #(
    RPAREN = auto() #)

    EOF = auto() #This is the end of input marker, and it is the parser's stop signal, telling it that there is no more input left to parse

    NEWLINE = auto() #statement separator - emitted once per source line, outside ()

    FN = auto() #the fn keyword which starts both named defs of functions, and lambdas
    LBRACE = auto() #the { that opens a function body
    RBRACE = auto() #the } that closes a function body
    LBRACKET = auto() #The [ that opens a list 
    RBRACKET = auto() #The ] that closes a list
    COMMA = auto() #, Used as a separator, mainly in lists
    APPLY = auto() #The -> operator, which applies a function to an argument
    PIPE = auto() #the |> operator, which pipes a value into a function, and desugars to a Call (desugars is the method of translating convenient syntax into a more basic form that can be handled by existing implementation)
    APPEND = auto() #The ++ operator, which concatenates lists


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
#So far, the input of anything that matches from the below table (let, if, then, elseif, true, false, else) becomes keywords, and everything else stays as the IDENT category
KEYWORDS = {"let": TokenType.LET,
            "if": TokenType.IF,
            "then": TokenType.THEN,
            "elseif": TokenType.ELIF,
            "true": TokenType.TRUE,
            "false": TokenType.FALSE,
            "else": TokenType.ELSE,
            "fn": TokenType.FN,
            "checkpoint": TokenType.CHECKPOINT,
            "rewind": TokenType.REWIND
            }

#A dictionary of single chars that are their own token type (mainly the different mathematical operators and symbols)
SINGLE_CHAR_TOKENS = {
    '+': TokenType.PLUS,
    '-': TokenType.MINUS,
    '*': TokenType.STAR,
    '/': TokenType.SLASH,
    '=': TokenType.EQUALS,
    '(': TokenType.LPAREN,
    ')': TokenType.RPAREN,
    ">": TokenType.GT,
    "<": TokenType.LT,
    "{": TokenType.LBRACE,
    "}": TokenType.RBRACE,
    "[": TokenType.LBRACKET,
    "]": TokenType.RBRACKET,
    ",": TokenType.COMMA
}

#A dictionary of char pairs that are their own token type (mainly the comparison operators)
#The lexer checks these BEFORE the single chars, so longest match wins
#This happens because otherwise "==" would register as two "=" and not one "=="
TWO_CHAR_TOKENS = {
    "==": TokenType.EQEQ, #= is the binder for LET, and so cannot be used here
    "!=": TokenType.NE,
    "<=": TokenType.LTE,
    ">=": TokenType.GTE,
    "->": TokenType.APPLY, #function application operator
    "|>": TokenType.PIPE, #Pipeline operator
    "++": TokenType.APPEND #Appending list operator
}

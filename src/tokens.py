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
    PLUS = 
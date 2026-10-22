from dataclasses import dataclass


#Numbers
@dataclass(frozen=True)
class Number:
    value: int
    line:int
    col:int


#Vaariable
@dataclass(frozen=True)
class Var:
    name:str
    line:int
    col:int

#Binary Operations
@dataclass(frozen=True)
class BinOp:
    op:str
    left: object
    right: object
    line:int
    col:int


#let statements
@dataclass(frozen=True)
class Let:
    name:str
    value: object
    line:int
    col:int
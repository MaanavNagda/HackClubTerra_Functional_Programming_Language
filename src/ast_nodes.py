from dataclasses import dataclass
#dataclass is for immutable records, so the fields are only set once, and then never change

#A number literal. Handles all of the numbers like 42 in the program
@dataclass(frozen=True)
class Number:
    value: int
    line:int
    col:int


#A variable reference, such as the "x" in "x + 3"
#Stores the name only, the value is looked up in the env at the time of evaluation
@dataclass(frozen=True)
class Var:
    name:str
    line:int
    col:int

#Binary Operations - handles the preference stuff, allowing BODMAS to work, as it will evaluate multiplication before addition for example even if the addition comes before the multiplication
@dataclass(frozen=True)
class BinOp:
    op:str   #the 4 basic mathematical operations ("+", "-", "*", "/")
    left: object #AST (Abstract Syntax Tree) node
    right: object #AST node
    line:int   #position of the operator token
    col:int


#let statements - this is the command to bind a value to a variable
#It is a statement, and not an expression, so it is only legal to do at the top level
@dataclass(frozen=True)
class Let:
    name:str
    value: object  #AST node for the right hand side
    line:int     #position of the "let" keyword
    col:int


#conditional if c then a else b, so only one branch every evaluates
#also an easier to write sentence, and only takes up one line
#A branch itself may be an if, and thats how elseif chains work
@dataclass(frozen=True)
class If:
    cond: object  #AST node - the condition
    then: object  #AST node - evaluated when cond is truthy
    else_branch: object #AST node- when its false
    line: int
    col: int


#boolean literals - true/false; evaluates to themselves like number does
@dataclass(frozen=True)
class Bool:
    value: bool  
    line: int
    col: int
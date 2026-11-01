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


#A named function definition. It binds the name to the function in the env.
#It is a statement (and not an expression) as it updates the env (similar to let)
#Body is a list of statements, and the last one in that list is what is returned when the function is called
@dataclass(frozen=True)
class FnDef:
    name:str    #the name of the function
    param:str   #the name of the parameter (additional arguments come from currying & nested functions) (currying is writing a multi-argument function as a chain of single-argument function instead; each takes one argument, and returns the next function)
    body:list   #list of all the statements in the function, and the result of the last one is what is returned
    line:int
    col:int


#Used to apply a function to an argument
#Pipelining also desugars to this, so there is only one thing for the evaluator to deal with, rather than multiple ways of saying the same thing
@dataclass(frozen=True)
class Call:       
    func:object   #AST node - anything that should evaluate to a closure
    arg:object    #AST node - the input that the function is applied to
    line:int
    col:int


#This is an anonymous function
#It is used when a VALUE is expected, but writing it as a function is better
#It evaluates to a closure
#It can still recurse through a let
#It is an expression (not a statement), and so cannot alter the env (although it is able to capture it).
@dataclass(frozen=True)
class Lambda:
    param:str
    body:list
    line:int
    col:int
    
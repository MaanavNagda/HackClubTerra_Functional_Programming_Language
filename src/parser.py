from .tokens import Token, TokenType, KEYWORDS, SINGLE_CHAR_TOKENS
from .ast_nodes import Let, BinOp, Number, Var
#The input is the tokens list, and the output is the AST nodes
# Expression precendence is built into the function layering, and this helps it follow BODMAS
#The deeper functions bind together more, and this is what allows things like * to be completed before +


class Parser:
    #tokens is the lexer's output list, and it ends with an EOF token
    #pos is the current index into it (hence why it starts at 0)
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0


    #This is for the very top level of the program, as it is just a list of statements
    def parse_program(self):
        statements = []
        while self.peek().type !=  TokenType.EOF: #This happens until the input is exhausted
            if self.peek().type == TokenType.LET:
                statements.append(self.parse_let())
            else:
                statements.append(self.parse_expression())
        return statements


    #This is a grammar rule, saying that a let statement must have this exact shape. 
    def parse_let(self):
        let_tok = self.expect(TokenType.LET) #Consumes the let
        name = self.expect(TokenType.IDENT).value  #.value is the name string
        self.expect(TokenType.EQUALS)
        value = self.parse_expression()  #This parses the full RHS expression
        return Let(name, value, let_tok.line, let_tok.col)


    #This is where the expressions enter from, and is done so that future ones can slot in without touching callers.
    def parse_expression(self):
        return self.parse_additive()

    #This handles addition and subtraction, which is the lowest levels of BODMAS (Addition handles subtraction as well, as subtracting is just adding the negative of that number)
    def parse_additive(self):
        left= self.parse_multiplicative() #left as the multiplication comes from deeper level (as it has more precedence)
        while self.peek().type in [TokenType.PLUS, TokenType.MINUS]:
            op_tok = self.advance()
            right = self.parse_multiplicative() #* and / have already been grouped inside
            left = BinOp(op_tok.value, left, right, op_tok.line, op_tok.col) #left folding makes operations left-associative (1-2-3 = (1-2)-3), which helps with handling the order of addition and subtraction
        return left

    #* and / binds together tighter, because they run inside the + & - function, so they get evaluated first, and only then is + & - evaluated, which is necessary as that is how bodmas works
    #The actual function itself works in the same way as the addition function, except it evaluates it as * and / instead, as division is just multiplication of the reciprocal number, like how subtraction is just addition of the negative of the number.
    def parse_multiplicative(self):
        left = self.parse_primary()
        while self.peek().type in [TokenType.STAR, TokenType.SLASH]:
            op_tok = self.advance()
            right = self.parse_primary()
            left = BinOp(op_tok.value, left, right, op_tok.line, op_tok.col)
        return left

    #these are the things that cannot be split even further (like brackets, as they are at the top of BODMAS)
    #It runs inside the multiplication function, which in turn runs inside the addition function, which means that this one gets evaluated first
    def parse_primary(self):
        tok = self.advance()
        if tok.type == TokenType.NUMBER:
            return Number(tok.value, tok.line, tok.col)
        if tok.type == TokenType.IDENT:
            return Var(tok.value, tok.line, tok.col)
        if tok.type == TokenType.LPAREN:
            e = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return e
        raise Exception(f"expected expression, got {tok} at line {tok.line}, col {tok.col}")

#--------These are helper functions (below)----------------------------------------------------------------------

    #peek looks at the current token, but doesnt consume it. EOF is always the last token
    def peek(self):
        return self.tokens[self.pos]
    
    #consumes and returns the current token, allowing the rest of the program to be read
    def advance(self):
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    #Used to ensure that the token is off the expected type, otherwise it is an indication that there is an error in the program (hence the inclusion of an Exception in this helper function only)
    def expect(self, ttype):
        if self.peek().type == ttype:
            return self.advance()
        else:
            raise Exception(f"expected {ttype}, got {self.peek()} at line {self.peek().line}, col {self.peek().col}")
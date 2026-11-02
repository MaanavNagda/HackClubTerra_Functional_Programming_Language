from .tokens import Token, TokenType, KEYWORDS, SINGLE_CHAR_TOKENS
from .ast_nodes import Let, BinOp, Number, Var, If, Bool, FnDef, Call, Lambda
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
            #fn has two meanings - either fn followed by a name, then LPAREN, which is a named definition, or fn followed straight by the LPAREN, which is a Lambda expression, so we look the token ahead to decide which it is
            elif self.peek().type == TokenType.FN:
                if self.peek_at(1).type == TokenType.IDENT:
                    statements.append(self.parse_fndef())
                else:
                    statements.append(self.parse_expression())
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

    #Parses a named function definition
    #The body is shared with lambdas using parse_body(), as both are just statement lists, so the its better to outsource it to a function rather than repeating it
    def parse_fndef(self):
        fn_tok = self.expect(TokenType.FN)
        name = self.expect(TokenType.IDENT).value
        self.expect(TokenType.LPAREN)
        param = self.expect(TokenType.IDENT).value
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.LBRACE)
        body = self.parse_body()
        self.expect(TokenType.RBRACE)
        return FnDef(name, param, body, fn_tok.line, fn_tok.col)

    #This is for parsing the list of statements inside the LBRACE and RBRACE, and is shared by both named functions and lambdas
    #Also needs the lookahead, as there can be nested functions, so needs to know how to deal with that.
    def parse_body(self):
        body = []
        while self.peek().type != TokenType.RBRACE:
            if self.peek().type == TokenType.LET:
                body.append(self.parse_let())
            elif self.peek().type == TokenType.FN and self.peek_at(1).type == TokenType.IDENT:
                body.append(self.parse_fndef())
            else:
                body.append(self.parse_expression())
        return body

    #This is where the expressions enter from, and is done so that future ones can slot in without touching callers.
    def parse_expression(self):
        if self.peek().type in [TokenType.IF, TokenType.ELIF]:
            return self.parse_if()
        return self.parse_pipeline()

    #This is for the pipeline operator, and is the loosest level (sitting a level above ->)
    #x |> f desugars to Call(f,x), hence why the operands swap 
    def parse_pipeline(self):
        left = self.parse_call()
        while self.peek().type == TokenType.PIPE:
            opTok = self.advance()
            right = self.parse_call()
            left = Call(right, left, opTok.line, opTok.col)
        return left

    #This is the application operator applies
    #it is left associative, which is what makes curried functions work naturally
    def parse_call(self):
        left = self.parse_comparison()
        while self.peek().type == TokenType.APPLY:
            op_tok = self.advance()
            right = self.parse_comparison()
            left = Call(left, right, op_tok.line, op_tok.col)
        return left


    #Comparison level, and looser than any arithmetic, as a comparison will naturally act as a divider between two sides
    #Tighter than if, and has the same left-folding shape as addition/multiplication
    def parse_comparison(self):
        left = self.parse_additive()
        while self.peek().type in [TokenType.EQEQ, TokenType.NE, TokenType.LT, TokenType.GT, TokenType.LTE, TokenType.GTE]:
            op_tok = self.advance()
            right = self.parse_additive()
            left = BinOp(op_tok.value, left, right, op_tok.line, op_tok.col)
        return left

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
        if tok.type == TokenType.TRUE:
            return Bool(True, tok.line, tok.col)
        if tok.type == TokenType.FALSE:
            return Bool(False, tok.line, tok.col)
        if tok.type == TokenType.IDENT:
            return Var(tok.value, tok.line, tok.col)
        if tok.type == TokenType.LPAREN:
            e = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return e
        #fn in the expression position is an anonymous lambda, and so is a primary like numbers/vars
        #This is what lets lambdas aappear inside the RHS of a let statement, call args, and pipelines.
        if tok.type == TokenType.FN:
            self.expect(TokenType.LPAREN)
            param = self.expect(TokenType.IDENT).value
            self.expect(TokenType.RPAREN)
            self.expect(TokenType.LBRACE)
            body = self.parse_body()
            self.expect(TokenType.RBRACE)
            return Lambda(param, body, tok.line, tok.col)
        #unary minus (like -14 or x * -1) now desugars to 0 - operand, so the evaluators don't see a brand new node type, and instead just see a regular subtraction.
        #It only activates when an operand is expected, so "a - b" sill parses as subtraction
        if tok.type == TokenType.MINUS:
            operand = self.parse_primary()
            return BinOp("-", Number(0, tok.line, tok.col), operand,tok.line, tok.col)
        raise Exception(f"expected expression, got {tok} at line {tok.line}, col {tok.col}")


    #handles the conditionals logic, and parses it in the correct order
    #elseif is just nested if branches
    def parse_if(self):
        if_tok = self.advance()
        cond = self.parse_expression()
        self.expect(TokenType.THEN)
        then_branch = self.parse_expression()
        if self.peek().type == TokenType.ELSE:
            self.advance()
            else_branch = self.parse_expression()
        elif self.peek().type == TokenType.ELIF:
            else_branch =self.parse_if()
        else:
            else_branch = None
        return If(cond, then_branch, else_branch, if_tok.line, if_tok.col)

#--------These are helper functions (below)----------------------------------------------------------------------

    #peek looks at the current token, but doesnt consume it. EOF is always the last token
    def peek(self):
        return self.tokens[self.pos]

    #Looks n tokens ahead, without consuming them, which is how regular defined functions are distinguished from lambda expressions
    def peek_at(self, n):
        return self.tokens[self.pos + n]
    
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
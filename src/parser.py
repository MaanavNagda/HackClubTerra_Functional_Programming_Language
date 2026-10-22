from .tokens import Token, TokenType, KEYWORDS, SINGLE_CHAR_TOKENS
from .ast_nodes import Let, BinOp, Number, Var

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def parse_program(self):
        statements = []
        while self.peek().type !=  TokenType.EOF:
            if self.peek().type == TokenType.LET:
                statements.append(self.parse_let())
            else:
                statements.append(self.parse_expression())
        return statements

    def parse_let(self):
        let_tok = self.expect(TokenType.LET)
        name = self.expect(TokenType.IDENT).value
        self.expect(TokenType.EQUALS)
        value = self.parse_expression()
        return Let(name, value, let_tok.line, let_tok.col)

    def parse_expression(self):
        return self.parse_additive()


    def parse_additive(self):
        left= self.parse_multiplicative()
        while self.peek().type in [TokenType.PLUS, TokenType.MINUS]:
            op_tok = self.advance()
            right = self.parse_multiplicative()
            left = BinOp(op_tok.value, left, right, op_tok.line, op_tok.col)
        return left

    def parse_multiplicative(self):
        left = self.parse_primary()
        while self.peek().type in [TokenType.STAR, TokenType.SLASH]:
            op_tok = self.advance()
            right = self.parse_primary()
            left = BinOp(op_tok.value, left, right, op_tok.line, op_tok.col)
        return left

    def parse_primary(self):
        tok = self.advance()
        if tok.type == TokenType.NUMBER:
            return Number(tok.value, tok.line, tok.col)
        if tok.type == TokenType.IDENT:
            return Var(tok.value, tok.line, tok.col)
        if tok.type == TokenType.LPAREN:
            e = parse_expression()
            self.expect(TokenType.RPAREN)
            return e
        raise Exception(f"expected expression, got {tok} at line {tok.line}, col {tok.col}")


    def peek(self):
        return self.tokens[self.pos]
    def advance(self):
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok
    def expect(self, ttype):
        if self.peek().type == ttype:
            return self.advance()
        else:
            raise Exception(f"expected {ttype}, got {self.peek()} at line {self.peek().line}, col {self.peek().col}")
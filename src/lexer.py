from .tokens import Token, TokenType
class Lexer:
    def __init__(self, input_string):
        self.input_string = input_string
        self.pos = 0
        self.line = 1
        self.col = 1
        self.tokens = []
    def peek(self):
        if self.pos >= len(self.input_string):
            return None
        return self.input_string[self.pos]


    def peek_next(self):
        if self.pos + 1 >= len(self.input_string):
            return None
        return self.input_string[self.pos + 1]


    def advance(self):
        char = self.input_string[self.pos]
        self.pos += 1
        if char == '\n':
            self.line += 1
            self.col = 1
        else:
            self.col += 1
        return char


    def emit(self, ttype, value, start_line, start_col):
        self.tokens.append(Token(ttype, value, start_line, start_col))




        
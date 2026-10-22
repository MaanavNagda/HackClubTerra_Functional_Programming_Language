from .tokens import Token, TokenType, KEYWORDS, SINGLE_CHAR_TOKENS
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


    def tokenize(self):
        while self.peek() is not None:
            #getting rid of whitespace first
            while self.peek() is not None and self.peek().isspace():
                self.advance()

            #whitespace EOF
            if self.peek() is None:
                break

            #Save position before
            start_line = self.line
            start_col = self.col

            #dispatch on the current character
            char = self.peek()
            if char.isdigit():
                self.read_number(start_line, start_col)
            elif char.isalpha() or char == '_':
                self.read_indentifier(start_line, start_col)
            elif char in SINGLE_CHAR_TOKENS:
                self.emit(SINGLE_CHAR_TOKENS[char], char, start_line, start_col)
                self.advance()
            else:
                raise Exception(f"Unexpected character '{char}' at line {start_line}, column {start_col}")

        self.emit(TokenType.EOF, None, self.line, self.col)
        return self.tokens 

    def read_number(self, start_line, start_col):
        digits = ""
        while self.peek() is not None and self.peek().isdigit():
            digits += self.advance()
        self.emit(TokenType.NUMBER, int(digits), start_line, start_col)

    def read_indentifier(self, start_line, start_col):
        word = ""
        while self.peek() is not None and (self.peek().isalnum() or self.peek() == '_'):
            word += self.advance()
        self.emit(KEYWORDS.get(word, TokenType.IDENT), word, start_line, start_col)
    
from .tokens import Token, TokenType, KEYWORDS, SINGLE_CHAR_TOKENS, TWO_CHAR_TOKENS, DOT
#Turns raw source text into a list of tokens. This list of tokens is categorising the pieces of text into the types saved in /src/tokens.py
#Parser consumes its output



class Lexer:
    #the pos, line, and col is for identifying positions in the source, like a cursor
    #tokens is the output list that has been broken down into types
    #Has the rule that only advance() can alter the pos/line/col, so that every token's position stays accurate
    def __init__(self, input_string):
        self.input_string = input_string
        self.pos = 0
        self.line = 1
        self.col = 1
        self.tokens = []
        #This is for how deep we are inside (). Newlines only become tokens at depth 0, so mult-line expressions inside brackets keep working
        self.paren_depth = 0

    #Looks at the current character, without consuming (the none signals the end of the input)
    def peek(self):
        if self.pos >= len(self.input_string):
            return None
        return self.input_string[self.pos]

    #Looks at the character after the current one, also without consuming. This is for two character operators (like ==)
    def peek_next(self):
        if self.pos + 1 >= len(self.input_string):
            return None
        return self.input_string[self.pos + 1]


    #This consumes and returns current char, which essentially means that the pos/line/col change. it is the ONLY place that they can be changed from
    def advance(self):
        char = self.input_string[self.pos]
        self.pos += 1
        if char == '\n':
            self.line += 1
            self.col = 1
        else:
            self.col += 1
        return char

    #Appends a finished token (position is passed by the caller as to where that finished token should go)
    def emit(self, ttype, value, start_line, start_col):
        self.tokens.append(Token(ttype, value, start_line, start_col))


    def tokenize(self):
        #This is to loop until the input is exhausted
        while self.peek() is not None:
            #getting rid of whitespace first (note that newlines are included as a type of whitespace, and so will be removed as well in this step)
            #Also skips any comments, by finding the comment marker ";;" and consuming every subsequent character until a new line is reached
            while True:
                #Updated - first checking if there is a new line token, before isspace, so we can use the newline separator. Only then does it delete the whitespace.
                #a new line only becomes a token outside (), if it is inside a parens, then it is a plain whitespace, so multline functions don't break
                if self.peek() == "\n":
                    nl_line = self.line
                    nl_col = self.col
                    self.advance()
                    if self.paren_depth == 0:
                        self.emit(TokenType.NEWLINE, "\n", nl_line, nl_col)
                elif self.peek() is not None and self.peek().isspace():
                    self.advance()
                elif self.peek() == ";" and self.peek_next() == ";":
                    while self.peek() is not None and self.peek() != "\n":
                        self.advance()
                else:
                    break

            #Also a check for the EOF tag, as otherwise trailing whitespace may cause issues  
            if self.peek() is None:
                break

            #Save the start lines and cols before consuming them, so the tokens point to the first character
            start_line = self.line
            start_col = self.col

            #dispatch on the current character
            char = self.peek()
            pair = char + (self.peek_next() or "") #looking ahead at the next character to see if it is a pair operator or a single operator
            if pair in TWO_CHAR_TOKENS: #making sure that we match pair tokens before single ones, as otherwise an "==" operator will instead be treated as two "=", which is not correct
                self.emit(TWO_CHAR_TOKENS[pair], pair, start_line, start_col)
                self.advance()
                self.advance() #BOTH characters need consuming, and so advance is called twice instead of the usual once.
            elif char.isdigit():
                self.read_number(start_line, start_col)
            elif char.isalpha() or char == '_':
                self.read_identifier(start_line, start_col)
            elif char == '"':
                self.read_string(start_line, start_col)
            elif char in SINGLE_CHAR_TOKENS:
                self.emit(SINGLE_CHAR_TOKENS[char], char, start_line, start_col)
                if char == "(" or char == "[":
                    self.paren_depth += 1
                if (char == ")" or char == "]") and self.paren_depth > 0:
                    self.paren_depth -= 1
                self.advance()
            else:
                raise Exception(f"Unexpected character '{char}' at line {start_line}, column {start_col}")
        #The parser needs the EOF to know when the program ends
        self.emit(TokenType.EOF, None, self.line, self.col)
        return self.tokens 

    #This is for digits - one NUMBER token (an integer value, not a raw text string)
    def read_number(self, start_line, start_col):
        digits = ""
        while self.peek() is not None and self.peek().isdigit():
            digits += self.advance()

        if self.peek() == "." and self.peek_next() is not None and self.peek_next().isdigit():
            digits += self.advance()
            while self.peek() is not None and self.peek().isdigit():
                digits += self.advance()
            self.emit(TokenType.NUMBER, float(digits), start_line, start_col)
        else:
            self.emit(TokenType.NUMBER, int(digits), start_line, start_col)
   
   
   
   
   
    #This is for letters and digits, and it is the whole word first, and only then checks for key words
    #This order is needed as that stops things like an input of "letter" lexing as the key word "let" and then "ter", when in reality, it is not a keyword at all, but a separate word (letter)
    def read_identifier(self, start_line, start_col):
        word = ""
        while self.peek() is not None and (self.peek().isalnum() or self.peek() == '_'):
            word += self.advance()
        if self.peek() == "!" and self.peek_next() != "=":
            word += "!"
            self.advance()
        self.emit(KEYWORDS.get(word, TokenType.IDENT), word, start_line, start_col)

    def read_string(self, start_line, start_col):
        self.advance() #consumes the opening quote
        value = ""
        while True:
            c = self.peek()
            if c is None or c == "\n": #strings are single line
                raise Exception(f"unterminated string at line {start_line}, column {start_col}")
            if c == "\\": #This is using \ as a string literal. This means that if you want to put a special character in a string, you can use \ before it without it breaking the system. If you want to type a \ character, you simply do \\, and it will result in the \ character being stored once
                self.advance()
                value = value + self.advance()
            elif c == '"':
                self.advance()
                self.emit(TokenType.STRING, value, start_line, start_col)
                return
            else:
                value = value + self.advance()
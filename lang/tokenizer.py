class Tokenizer:
    def __init__(self, text, offset=1):
        self.text = text
        self.current = 0
        self.start = 0
        self.length = len(text)
        self.tokens = []
        self.special_chars = set(["{", "}", "@", "|"])
        self.line = offset

    def next(self):
        self.current += 1
        if (not self.atEnd()) and (self.curr() == "\n"):
            self.line += 1

    def curr(self):
        try:
            return self.text[self.current]
        except:
            raise SyntaxError(f"Line {self.line}: Unexpected EOF")

    def checkpoint(self):
        self.start = self.current

    def get_chunk(self):
        return self.text[self.start:self.current]

    def atEnd(self):
        return self.current > self.length - 1

    def tokenize_char(self):
        char = self.curr()
        if char == "{":
            self.tokens.append(("LEFT_CURLY", None, self.line))
            self.next()
        elif char == "}":
            self.tokens.append(("RIGHT_CURLY", None, self.line))
            self.next()
        elif char == "@":
            self.next()
            self.checkpoint()
            while self.curr() != "{":
                self.next()
            op = self.get_chunk()
            if not op:
                raise SyntaxError(f"Line {self.line}: No operation specified")
            self.tokens.append(("OP", op, self.line))
        elif char == "|":
            self.next()
            if self.curr() == "|":
                self.next()
                self.tokens.append(("ARG", None, self.line))
            else:
                raise SyntaxError(f"Line {self.line}: Expected second \|")
        else:
            self.checkpoint()
            self.next()
            while (not self.atEnd()) and (self.curr() not in self.special_chars):
                self.next()
            content = self.get_chunk()
            self.tokens.append(("CONTENT", content, self.line))

    def tokenize(self):
        while not self.atEnd():
            self.tokenize_char()

        return self.tokens

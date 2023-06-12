import re

POST_HEADER = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Alex' Blog</title>
    <link rel="stylesheet" href="../index.css">
    <link rel="icon" href="../assets/img/favicon.ico">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@100;300;500;700&family=Lora:wght@400;500;600;700&family=Open+Sans:wght@300;400;500&display=swap" rel="stylesheet">
</head>
<body>
    <header>
        <a href="/" class="logo-link"><div class="logo">Alex's Blog</div></a>
        <nav>
            <ul class="horizontal-list">
                <li><a href="/">Home</a></li>
                <li><a href="/posts">Posts</a></li>
                <li><a href="/projects">Projects</a></li>
                <li><a href="/contact">Contact</a></li>
            </ul>
        </nav>
    </header>
    <main>
        <div class="post">
'''

POST_FOOTER = '''
</div>
'''

POST_BODY_HEADER = '''
<div class="post-content">
'''
POST_BODY_FOOTER = '''
</div>
        </div>
    </main>
    <footer>
        <p>Something about myself</p>
    </footer>
</body>
</html>

'''


def pretty_print(node, indent=0):
    print("  " * indent + str(node.type) + " " + str(node.field))
    for child in node.nodes:
        pretty_print(child, indent + 1)


class AST:
    def __init__(self, type, field):
        self.type = type
        self.field = field
        self.nodes = []

        self.op_to_html = {
            "title": ('''<div class="post-title">''', "</div>"),
            "subtitle": ('''<div class="post-subtitle">''', "</div>"),
            "date": ('''<div class="post-date">''', "</div>"),
            "i": ("<i>", "</i>"),
            "b": ("<strong>", "</strong>"),
            "u": ("<u>", "</u>"),
            "$": ("\(", "\)"),
            "section": ("<h3>", "</h3>"),
            "subsection": ("<h4>", "</h4>")
        }

    def __repr__(self):
        node_strings = "\n".join([repr(n) for n in self.nodes])
        return f"Type: {self.type}\nField: {self.field}\nNodes: {node_strings}"

    def add(self, node):
        self.nodes.append(node)

    def extend(self, nodes):
        self.nodes.extend(nodes)

    def evaluate_nodes(self, h, f):
        return '\n'.join([n.evaluate(h, f) for n in self.nodes])

    def evaluate(self, h, f):
        if self.type == "EXPR":
            contents = self.evaluate_nodes(h, f)
            return h + contents + f
        elif self.type == "OP":
            contents = self.evaluate_nodes(h, f)
            header, footer = self.op_to_html[self.field]
            return header + contents + footer
        elif self.type == "CONTENT":
            return self.field


class Tokenizer:
    def __init__(self, text):
        self.text = text
        self.current = 0
        self.start = 0
        self.length = len(text)
        self.tokens = []
        self.special_chars = set(["{", "}", "@"])

    def next(self):
        self.current += 1

    def curr(self):
        try:
            return self.text[self.current]
        except:
            raise SyntaxError("Unexpected EOF")

    def checkpoint(self):
        self.start = self.current

    def get_chunk(self):
        return self.text[self.start: self.current]

    def atEnd(self):
        return self.current > self.length - 1

    def tokenize_char(self):
        char = self.curr()
        if char == "{":
            self.tokens.append(("LEFT_CURLY", None))
            self.next()
        elif char == "}":
            self.tokens.append(("RIGHT_CURLY", None))
            self.next()
        elif char == "@":
            self.next()
            self.checkpoint()
            while self.curr() != "{":
                self.next()
            op = self.get_chunk()
            if not op:
                raise SyntaxError("No operation specified")
            self.tokens.append(("OP", op))
        else:
            self.checkpoint()
            self.next()
            while (not self.atEnd()) and (self.curr() not in self.special_chars):
                self.next()
            content = self.get_chunk()
            self.tokens.append(("CONTENT", content))

    def tokenize(self):
        while not self.atEnd():
            self.tokenize_char()


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
        self.ast = AST("EXPR", None)

    def next(self):
        self.current += 1

    def curr(self):
        return self.tokens[self.current]

    def match(self, t):
        if not self.atEnd():
            curr_type, _ = self.curr()
            return t == curr_type

    def atEnd(self):
        return self.current > len(self.tokens) - 1

    def parse_op_expr(self):
        if not self.atEnd():
            curr_type, curr_val = self.curr()
            root = AST(curr_type, curr_val)
            self.next()
            self.match("LEFT_CURLY")
            self.next()
            self.parse_expr(self.curr())
            self.match("RIGHT_CURLY")
            return root

    def parse_content_expr(self):
        if not self.atEnd():
            return AST(*self.curr())

    def parse_expr(self, parent):
        if not self.atEnd():
            if self.match("OP"):
                parent.add(self.parse_op_expr())
                self.next()
            elif self.match("CONTENT"):
                parent.add(self.parse_content_expr())
                self.next()
            else:
                print(self.curr())
                print(self.current)
                raise ValueError("something went wrong")

    def parse(self):
        while not self.atEnd():
            self.parse_expr(self.ast)

        return self


def separate_bodies(text):
    try:
        match = re.search(r'^(.*?)---(.*?)$', text, re.DOTALL)
        header, body = match.group(1), match.group(2)
        return header, body
    except:
        raise SyntaxError("No header found")


def translate_head(text):
    tokenizer = Tokenizer(text)
    tokenizer.tokenize()
    parser = Parser(tokenizer.tokens)
    parser.parse()
    return parser.ast.evaluate(POST_HEADER, POST_FOOTER)


def translate_body(text):
    tokenizer = Tokenizer(text)
    tokenizer.tokenize()
    parser = Parser(tokenizer.tokens)
    parser.parse()
    return parser.ast.evaluate(POST_BODY_HEADER, POST_BODY_FOOTER)


def translate(text):
    header, body = separate_bodies(text)
    return translate_head(header) + translate_body(body)


if __name__ == "__main__":
    with open("post_example.elec", "r") as f:
        html = translate(f.read())

    with open("post_translated.html", "w") as f:
        f.write(html)

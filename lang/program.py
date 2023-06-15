from lang.parser import Parser
from lang.tokenizer import Tokenizer


class Env(dict):
    def __init__(self):
        self.update(
            {
                "title": lambda x: '''<div class="post-title">''' + x + "</div>",
                "subtitle": lambda x: '''<div class="post-subtitle">''' + x + "</div>",
                "date": lambda x: '''<div class="post-date">''' + x + "</div>",
                "i": lambda x: "<i>" + x + "</i>",
                "b": lambda t: "<strong>" + t + "</strong>",
                "u": lambda t: "<u>" + t + "</u>",
                "$": lambda t: "\(" + t + "\)",
                "$$": lambda t: r'''$$\\begin{aligned}''' + t + r'''\\end{aligned}$$''',
                "section": lambda t: '''<div class="section">''' + t + "</div>",
                "subsection": lambda t: '''<div class="subsection">''' + t + "</div>",
                "subsubsection": lambda t: '''<div class="subsubsection">''' + t + "</div>",
                "p": lambda t: "<p>" + t + "</p>",
                "code": lambda x: '''<span class="code">''' + x + "</span>",
                "margin": lambda x: '''<span class="tooltip"> * <span class="tooltip-text">''' + x + '''</span></span>''',
                "img": lambda x: '''<img src="''' + x + '''">''',
                "video": lambda x: '''<video controls width="70%"><source src="''' + x + '''"></video>''',
                "link": lambda x, y: '''<a href="''' + x + '''">''' + y + "</a>",
                "+": lambda x, y: f"{float(x) + float(y)}",
                "-": lambda x, y: f"{float(x) - float(y)}",
                "*": lambda x, y: f"{float(x) * float(y)}",
                "/": lambda x, y: f"{float(x) / float(y)}",
                "concat": lambda x, y: f"{x+y}",
                "ul": lambda *x: self.ul(x),
                "ol": lambda *x: self.ol(x),
                "ignore": lambda x: "",
                "center": lambda x: '''<span style="display: inline-block; text-align: center; width: 100%;">''' + x + '''</span>'''
            }
        )

    def ul(self, lst):
        return "<ul>" + ''.join([f"<li>{l}</li>" for l in lst]) + "</ul>"

    def ol(self, lst):
        return "<ol>" + ''.join([f"<li>{l}</li>" for l in lst]) + "</ol>"


class Program():
    def __init__(self, prog, offset=1):
        self.orig = prog
        self.prog = prog
        self.offset = offset

        self.env = Env()

    def get_tokens(self):
        return self.tokenize().prog.tokens

    def get_ast(self):
        return self.tokenize().parse().prog

    def tokenize(self):
        t = Tokenizer(self.orig, self.offset)
        self.prog = t.tokenize()

        return self

    def parse(self):
        p = Parser(self.tokenize().prog)
        self.prog = p.parse()

        return self

    def eval(self):
        return self.tokenize().parse().prog.evaluate(self.env)

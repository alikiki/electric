class AST:
    def __init__(self, type, field):
        self.type = type
        self.field = field
        self.nodes = []

    def add(self, node):
        self.nodes.append(node)

    def extend(self, nodes):
        self.nodes.extend(nodes)

    def evaluate_nodes(self, env):
        return [n.evaluate(env) for n in self.nodes]

    def evaluate(self, env):
        if self.type == "EXPR":
            return ''.join(self.evaluate_nodes(env))
        elif self.type == "OP":
            contents = self.evaluate_nodes(env)
            return env[self.field](*contents)
        elif self.type == "ARG":
            return ''.join(self.evaluate_nodes(env))
        elif self.type == "CONTENT":
            return self.field


class Parser:
    # GRAMMAR:
    #   expr := op_expr || content_expr
    #   op_expr := op "{" args "}"
    #   args := expr (|| expr)*

    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
        self.ast = AST("EXPR", None)

    def prev(self):
        return self.tokens[self.current - 1]

    def next(self):
        self.current += 1

    def curr(self):
        return self.tokens[self.current]

    def valid(self):
        return self.current <= len(self.tokens) - 1

    def match(self, t):
        if self.valid():
            curr_type, _, curr_line = self.curr()
            if curr_type == t:
                self.next()
            else:
                raise ValueError(
                    f"line {curr_line}: expected type {t}, got {curr_type}")

    def move_until(self, t):
        while (self.valid()) and (t != self.curr()[0]):
            self.next()

    def parse_expr(self, parent):
        try:
            self.match("OP")
            parent.add(self.parse_op_expr())
        except:
            try:
                self.match("CONTENT")
                parent.add(self.parse_content_expr())
            except:
                curr_type, curr_val, curr_line = self.curr()
                raise ValueError(
                    f"line {curr_line}: parsing error. current token is {curr_type} with value {curr_val}")

    def parse_op_expr(self):
        t, v, _ = self.prev()
        root = AST(t, v)
        self.match("LEFT_CURLY")

        arg_count = 1
        while (self.curr()[0] != "RIGHT_CURLY"):
            if arg_count > 1:
                self.match("ARG")
            child = AST("ARG", None)
            self.parse_arg_expr(child)
            root.add(child)
            arg_count += 1
        self.match("RIGHT_CURLY")

        return root

    def parse_content_expr(self):
        t, v, _ = self.prev()
        return AST(t, v)

    def parse_arg_expr(self, parent):
        while self.curr()[0] not in ("ARG", "RIGHT_CURLY"):
            self.parse_expr(parent)

    def parse(self):
        while self.valid():
            self.parse_expr(self.ast)

        return self.ast

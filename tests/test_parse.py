import unittest
from lang.parser import Parser, AST


class TestParse(unittest.TestCase):
    def equal(self, ast1, ast2):
        if (ast1.type != ast1.type) or (ast1.field != ast2.field):
            return False
        if (len(ast1.nodes) != len(ast2.nodes)):
            return False

        checks = [self.equal(ast1.nodes[i], ast2.nodes[i])
                  for i in range(len(ast1.nodes))]
        return all(checks)

    def test_flat_op(self):
        tokens = [
            ('OP', 'op', 1),
            ('LEFT_CURLY', None, 1),
            ('CONTENT', 'content', 1),
            ('RIGHT_CURLY', None, 1)
        ]
        p = Parser(tokens)
        p.parse()
        grandchild = AST("ARG", None)
        grandchild.add(AST("CONTENT", "content"))
        child = AST("OP", "op")
        child.add(grandchild)
        gt = AST('EXPR', None)
        gt.add(child)
        self.assertTrue(self.equal(p.ast, gt))

    def test_flat_op_multi_arg(self):
        tokens = [
            ('OP', 'op', 1),
            ('LEFT_CURLY', None, 1),
            ('CONTENT', 'content', 1),
            ('ARG', None, 1),
            ('CONTENT', 'content2', 1),
            ('RIGHT_CURLY', None, 1)
        ]
        p = Parser(tokens)
        p.parse()
        grandchild1 = AST("ARG", None)
        grandchild1.add(AST("CONTENT", "content"))
        grandchild2 = AST("ARG", None)
        grandchild2.add(AST("CONTENT", "content2"))
        child = AST("OP", "op")
        child.extend([grandchild1, grandchild2])
        gt = AST('EXPR', None)
        gt.add(child)
        self.assertTrue(self.equal(p.ast, gt))

    def test_flat_op_then_content(self):
        tokens = [
            ('OP', 'op', 1),
            ('LEFT_CURLY', None, 1),
            ('CONTENT', 'content', 1),
            ('RIGHT_CURLY', None, 1),
            ('CONTENT', 'content2', 1)
        ]
        p = Parser(tokens)
        p.parse()
        grandchild = AST("ARG", None)
        grandchild.add(AST('CONTENT', 'content'))
        child1 = AST("OP", "op")
        child1.add(grandchild)
        child2 = AST("CONTENT", "content2")
        gt = AST('EXPR', None)
        gt.extend([child1, child2])
        self.assertTrue(self.equal(p.ast, gt))

    def test_layer_op(self):
        tokens = [
            ('OP', 'op', 1),
            ('LEFT_CURLY', None, 1),
            ('OP', 'op2', 1),
            ('LEFT_CURLY', None, 1),
            ('CONTENT', 'content', 1),
            ('RIGHT_CURLY', None, 1),
            ('RIGHT_CURLY', None, 1)
        ]
        p = Parser(tokens)
        p.parse()
        gggchild = AST("ARG", None)
        gggchild.add(AST("CONTENT", 'content'))
        ggchild = AST("OP", "op2")
        ggchild.add(gggchild)
        gchild = AST("ARG", None)
        gchild.add(ggchild)
        child = AST("OP", "op")
        child.add(gchild)
        gt = AST('EXPR', None)
        gt.add(child)
        self.assertTrue(self.equal(p.ast, gt))

    def test_layer_op_then_content(self):
        tokens = [
            ('OP', 'op', 1),
            ('LEFT_CURLY', None, 1),
            ('OP', 'op2', 1),
            ('LEFT_CURLY', None, 1),
            ('CONTENT', 'content', 1),
            ('RIGHT_CURLY', None, 1),
            ('CONTENT', 'content2', 1),
            ('RIGHT_CURLY', None, 1)
        ]
        p = Parser(tokens)
        p.parse()
        gggchild = AST("ARG", None)
        gggchild.add(AST("CONTENT", 'content'))
        ggchild1 = AST("OP", "op2")
        ggchild1.add(gggchild)
        ggchild2 = AST("CONTENT", 'content2')
        gchild = AST("ARG", None)
        gchild.extend([ggchild1, ggchild2])
        child = AST("OP", "op")
        child.add(gchild)
        gt = AST('EXPR', None)
        gt.add(child)
        self.assertTrue(self.equal(p.ast, gt))

    def test_content_then_op(self):
        tokens = [
            ('CONTENT', 'content', 1),
            ('OP', 'op', 1),
            ('LEFT_CURLY', None, 1),
            ('CONTENT', 'content2', 1),
            ('RIGHT_CURLY', None, 1)
        ]
        p = Parser(tokens)
        p.parse()
        gchild = AST("ARG", None)
        gchild.add(AST("CONTENT", 'content2'))
        child1 = AST("CONTENT", 'content')
        child2 = AST("OP", 'op')
        child2.add(gchild)
        gt = AST('EXPR', None)
        gt.extend([child1, child2])
        self.assertTrue(self.equal(p.ast, gt))

    def test_two_layer_op(self):
        tokens = [
            ('OP', 'op', 1),
            ('LEFT_CURLY', None, 1),
            ('OP', 'op', 1),
            ('LEFT_CURLY', None, 1),
            ('CONTENT', 'arg1', 1),
            ('RIGHT_CURLY', None, 1),
            ('ARG', None, 1), ('OP', 'op', 1),
            ('LEFT_CURLY', None, 1),
            ('CONTENT', 'arg2', 1),
            ('RIGHT_CURLY', None, 1),
            ('RIGHT_CURLY', None, 1)
        ]
        p = Parser(tokens)
        p.parse()
        gggchild1 = AST("ARG", None)
        gggchild2 = AST("ARG", None)
        gggchild1.add(AST("CONTENT", 'arg1'))
        gggchild2.add(AST("CONTENT", 'arg2'))
        ggchild1 = AST("OP", 'op')
        ggchild2 = AST("OP", 'op')
        ggchild1.add(gggchild1)
        ggchild2.add(gggchild2)
        gchild1 = AST("ARG", None)
        gchild2 = AST("ARG", None)
        gchild1.add(ggchild1)
        gchild2.add(ggchild2)
        child = AST("OP", 'op')
        child.extend([gchild1, gchild2])
        gt = AST('EXPR', None)
        gt.add(child)
        self.assertTrue(self.equal(p.ast, gt))

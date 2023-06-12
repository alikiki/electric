import unittest
from elec_parser import Parser, AST, pretty_print


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
            ('OP', 'op'),
            ('LEFT_CURLY', None),
            ('CONTENT', 'content'),
            ('RIGHT_CURLY', None)
        ]
        p = Parser(tokens)
        p.parse()
        gt = AST('EXPR', None)
        child = AST("OP", "op")
        child.add(AST("CONTENT", "content"))
        gt.add(child)
        self.assertTrue(self.equal(p.ast, gt))

    def test_flat_op_then_content(self):
        tokens = [
            ('OP', 'op'),
            ('LEFT_CURLY', None),
            ('CONTENT', 'content'),
            ('RIGHT_CURLY', None),
            ('CONTENT', 'content2')
        ]
        p = Parser(tokens)
        p.parse()
        gt = AST('EXPR', None)
        child1 = AST("OP", "op")
        child1.add(AST("CONTENT", "content"))
        child2 = AST("CONTENT", "content2")
        gt.extend([child1, child2])
        self.assertTrue(self.equal(p.ast, gt))

    def test_layer_op(self):
        tokens = [
            ('OP', 'op'),
            ('LEFT_CURLY', None),
            ('OP', 'op2'),
            ('LEFT_CURLY', None),
            ('CONTENT', 'content'),
            ('RIGHT_CURLY', None),
            ('RIGHT_CURLY', None)
        ]
        p = Parser(tokens)
        p.parse()
        grandchild = AST("OP", "op2")
        grandchild.add(AST("CONTENT", "content"))
        child = AST("OP", "op")
        child.add(grandchild)
        gt = AST('EXPR', None)
        gt.add(child)
        self.assertTrue(self.equal(p.ast, gt))

    def test_layer_op_then_content(self):
        tokens = [
            ('OP', 'op'),
            ('LEFT_CURLY', None),
            ('OP', 'op2'),
            ('LEFT_CURLY', None),
            ('CONTENT', 'content'),
            ('RIGHT_CURLY', None),
            ('CONTENT', 'content2'),
            ('RIGHT_CURLY', None)
        ]
        p = Parser(tokens)
        p.parse()
        grandchild1 = AST("OP", "op2")
        grandchild1.add(AST("CONTENT", "content"))
        grandchild2 = AST("CONTENT", "content2")
        child = AST("OP", "op")
        child.add(grandchild1)
        child.add(grandchild2)
        gt = AST('EXPR', None)
        gt.add(child)
        self.assertTrue(self.equal(p.ast, gt))

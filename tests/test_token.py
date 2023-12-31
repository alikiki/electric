import unittest
from lang.tokenizer import Tokenizer


class TestToken(unittest.TestCase):
    def test_solo_leftcurly(self):
        text = "{"
        t = Tokenizer(text)
        t.tokenize()
        self.assertEqual(t.tokens[0][0], "LEFT_CURLY")

    def test_solo_rightcurly(self):
        text = "}"
        t = Tokenizer(text)
        t.tokenize()
        self.assertEqual(t.tokens[0][0], "RIGHT_CURLY")

    def test_solo_op(self):
        text = '''@op{content}'''
        t = Tokenizer(text)
        t.tokenize()
        self.assertEqual(t.tokens[0], ('OP', 'op', 1))
        self.assertEqual(t.tokens[1][0], "LEFT_CURLY")
        self.assertEqual(t.tokens[2], ('CONTENT', 'content', 1))
        self.assertEqual(t.tokens[3][0], "RIGHT_CURLY")

    def test_content_after_op(self):
        text = '''@op{content} content'''
        t = Tokenizer(text)
        t.tokenize()
        self.assertEqual(t.tokens[0], ('OP', 'op', 1))
        self.assertEqual(t.tokens[4], ("CONTENT", " content", 1))

    def test_content_before_op(self):
        text = '''content @op{content}'''
        t = Tokenizer(text)
        t.tokenize()
        self.assertEqual(t.tokens[1], ('OP', 'op', 1))
        self.assertEqual(t.tokens[0], ("CONTENT", "content ", 1))

    def test_surrounding_op(self):
        text = '''content @op{content} content'''
        t = Tokenizer(text)
        t.tokenize()
        self.assertEqual(t.tokens[0], ("CONTENT", "content ", 1))
        self.assertEqual(t.tokens[1], ('OP', 'op', 1))
        self.assertEqual(t.tokens[5], ("CONTENT", " content", 1))

    def test_op_with_multiple_arg(self):
        text = '''@op{arg1||arg2}'''
        t = Tokenizer(text)
        t.tokenize()
        self.assertEqual(t.tokens[0], ("OP", "op", 1))
        self.assertEqual(t.tokens[3], ('ARG', None, 1))

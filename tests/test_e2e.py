import unittest
from lang.program import Program


class TestE2E(unittest.TestCase):
    def test_content_only(self):
        prog = Program("content")
        self.assertEqual(prog.eval(), "content")

    def test_op_only_single_arg(self):
        prog = Program("@i{content}")
        self.assertEqual(prog.eval(), "<i>content</i>")

    def test_op_only_double_arg(self):
        prog = Program("@link{some link||some description}")
        self.assertEqual(
            prog.eval(), "<a href=\"some link\">some description</a>")

    def test_op_with_content_single_arg(self):
        prog = Program("@i{some italics} normal text")
        self.assertEqual(
            prog.eval(), "<i>some italics</i> normal text"
        )

    def test_op_with_content_double_arg(self):
        prog = Program("@link{some link||some description} normal text")
        self.assertEqual(
            prog.eval(), "<a href=\"some link\">some description</a> normal text")

    def test_layered_op_single_then_single(self):
        prog = Program("@i{@b{decorated}}")
        self.assertEqual(
            prog.eval(), "<i><strong>decorated</strong></i>"
        )

    def test_layered_single_then_double(self):
        prog = Program("@i{@link{someLink||description}}")
        self.assertEqual(
            prog.eval(), "<i><a href=\"someLink\">description</a></i>"
        )

    def test_layered_double_then_single(self):
        prog = Program("@combine{@b{bold}||@i{italic}}")
        prog.env.update({"combine": lambda x, y: x + y})
        self.assertEqual(
            prog.eval(), "<strong>bold</strong><i>italic</i>"
        )

    def test_layered_double_then_double(self):
        prog = Program("@combine{@combine{1||2}||@combine{3||4}}")
        prog.env.update({"combine": lambda x, y: x + y})
        self.assertEqual(
            prog.eval(), "1234"
        )

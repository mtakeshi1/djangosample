import unittest
from lisp.lisp.interpreter import evaluate


class MyTestCase(unittest.TestCase):

    def test_literals(self):
        result = evaluate('123')
        self.assertEqual('123', result.strip())
        result = evaluate('"123"')
        self.assertEqual('123', result.strip())
        result = evaluate('True')
        self.assertEqual('True', result.strip())
        result = evaluate('()')
        self.assertEqual('[]', result.strip())

    def test_sum(self):
        result = evaluate('(+ 1 2)')
        self.assertEqual('3', result.strip())

    def test_define(self):
        result = evaluate('(def plus_one (x) (+ 1 x))\n(plus_one 3)')
        self.assertEqual('4', result.strip())

    def test_equal_not_equal(self):
        result = evaluate('(== 1 1)')
        self.assertEqual('True', result.strip())
        result = evaluate('(== 2 1)')
        self.assertEqual('False', result.strip())
        result = evaluate('(!= 1 1)')
        self.assertEqual('False', result.strip())
        result = evaluate('(!= 2 1)')
        self.assertEqual('True', result.strip())

    def test_predef(self):
        # result = evaluate('(!= 1 2)').strip()
        # self.assertEqual('True', result)
        # result = evaluate('(== () ())').strip()
        # self.assertEqual('True', result)
        # result = evaluate('(empty ())').strip()
        # self.assertEqual('True', result)
        # result = evaluate('(len ())').strip()
        # self.assertEqual('0', result)
        result = evaluate('(len (a))').strip()
        self.assertEqual('1', result)


if __name__ == '__main__':
    unittest.main()

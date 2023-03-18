import unittest
from lisp.lisp.parser import *
from lisp.lisp.tokenizer import tokenize


class ParserTokenizerTests(unittest.TestCase):

    def test_empty_tuple(self):
        tokens = tokenize('()')
        self.assertEqual(['(', ')'], tokens)
        self.assertEqual(Tuple([]), build_ast(tokens))

        tokens = tokenize(' ()')
        self.assertEqual(['(', ')'], tokens)
        self.assertEqual(Tuple([]), build_ast(tokens))

        tokens = tokenize('() ')
        self.assertEqual(['(', ')'], tokens)
        self.assertEqual(Tuple([]), build_ast(tokens))

        tokens = tokenize('( )')
        self.assertEqual(['(', ')'], tokens)
        self.assertEqual(Tuple([]), build_ast(tokens))

    def test_tuple_single(self):
        tokens = tokenize('(123)')
        self.assertEqual(['(', '123', ')'], tokens)
        self.assertEqual(Tuple([NumberLiteral(123)]), build_ast(tokens))
        tokens = tokenize(' (123)')
        self.assertEqual(['(', '123', ')'], tokens)
        self.assertEqual(Tuple([NumberLiteral(123)]), build_ast(tokens))
        tokens = tokenize('( 123)')
        self.assertEqual(['(', '123', ')'], tokens)
        self.assertEqual(Tuple([NumberLiteral(123)]), build_ast(tokens))
        tokens = tokenize('(123 )')
        self.assertEqual(['(', '123', ')'], tokens)
        self.assertEqual(Tuple([NumberLiteral(123)]), build_ast(tokens))
        tokens = tokenize('(123)     ')
        self.assertEqual(['(', '123', ')'], tokens)
        self.assertEqual(Tuple([NumberLiteral(123)]), build_ast(tokens))

    def test_tuple_tuple(self):
        tokens = tokenize('(  123 ( 456)  )')
        self.assertEqual(['(', '123', '(', '456', ')', ')'], tokens)
        tree = build_ast(tokens)
        self.assertEqual(Tuple([NumberLiteral(123), Tuple([NumberLiteral(456)])]), tree)

    def test_number_literal(self):
        tokens = tokenize('123')
        self.assertEqual(['123'], tokens)
        tree = build_ast(tokens)
        self.assertEqual(NumberLiteral(123), tree)
        tokens = tokenize('123 ')
        self.assertEqual(['123'], tokens)
        tree = build_ast(tokens)
        self.assertEqual(NumberLiteral(123), tree)
        tokens = tokenize(' 123')
        self.assertEqual(['123'], tokens)
        tree = build_ast(tokens)
        self.assertEqual(NumberLiteral(123), tree)

        tokens = tokenize('123.0')
        self.assertEqual(['123.0'], tokens)
        tree = build_ast(tokens)
        self.assertEqual(NumberLiteral(123.0), tree)
        tokens = tokenize('.123')
        self.assertEqual(['.123'], tokens)
        tree = build_ast(tokens)
        self.assertEqual(NumberLiteral(.123), tree)


if __name__ == '__main__':
    unittest.main()

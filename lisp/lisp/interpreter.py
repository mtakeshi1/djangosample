from lisp.lisp.tokenizer import tokenize
from lisp.lisp.parser import build_ast
from lisp.lisp.builtins import natives

all_predefs = ['(def != (a b) (not (== a b)))',
               '(def len (x) (if (== x ()) 0 (+ 1 (len (tail (x))))))',
               '(def empty (x) (== x ()))'

               ]


def evaluate(source):
    tokens = tokenize(source)
    scope = predef()
    stdout = ''
    while len(tokens) > 0:
        ast = build_ast(tokens)
        stdout += str(ast.eval(scope)) + '\n'

    return stdout


def predef():
    scope = natives()
    for source in all_predefs:
        tokens = tokenize(source)
        while len(tokens) > 0:
            ast = build_ast(tokens)
            ast.eval(scope)
    return scope

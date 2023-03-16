from .interpreter import LispError
from .tokenizer import tokenize
from dataclasses import dataclass
from typing import List


def parse(inputtext):
    tokens = tokenize(inputtext)
    # for i in tokens
    for i, token in enumerate(tokens):
        if token == '(':
            1
        elif token == ')':
            1
        elif token == 'True' or token == 'False':
            1

    return 1


class ParseError(LispError):
    def __init__(self, message):
        super().__init__(message)


class TODO(LispError):
    def __init__(self, message):
        super().__init__(message)


@dataclass
class Expression:
    def arity(self):
        return 1

    def eval(self, bindings):
        raise TODO()

    def as_number(self, bindings):
        raise ParseError('not a number ' + str(self))

    def as_boolean(self, bindings):
        raise ParseError('not a boolean: ' + str(self))

    def call(self, bindings):
        return self.eval()


@dataclass
class NumberLiteral(Expression):
    def __init__(self, num_value):
        self.num_value = num_value

    def as_number(self, bindings):
        return self.num_value

    def as_boolean(self, bindings):
        return self.num_value != 0

    def eval(self, bindings):
        return self.num_value


@dataclass
class StringLiteral(Expression):
    def __init__(self, string):
        self.string = string

    def eval(self, bindings):
        return self.string

    def as_boolean(self, bindings):
        return self.string != ''


@dataclass
class BooleanLiteral(Expression):
    def __init__(self, boolean_value):
        self.boolean_value = boolean_value

    def eval(self, bindings):
        return self.boolean_value

    def as_boolean(self, bindings):
        return self.boolean_value

    def as_number(self, bindings):
        return 1 if self.boolean_value else 0


@dataclass
class Symbol(Expression):

    def __init__(self, symbol):
        self.symbol = symbol

    def as_boolean(self, bindings):
        return self.eval(bindings).as_boolean

    def as_number(self, bindings):
        return self.eval(bindings).as_number


@dataclass
class Tuple(Expression):
    def __init__(self, members):
        self.members = members

    def arity(self):
        return len(self.members)

    def eval(self, bindings):
        return [c.eval(bindings) for c in self.members]

    def as_boolean(self, bindings):
        return self.arity() != 0

    def call(self, bindings):
        return 1


def build_ast(tokens: List[str]) -> Expression:
    if len(tokens) == 0:
        raise ParseError('reached EOF')
    head = tokens.pop(0)
    if head == '(':
        tree = []
        while tokens[0] != ')':
            tree.append(build_ast(tokens))
        tokens.pop(0)
        return Tuple(tree)
    elif head == 'True':
        return BooleanLiteral(True)
    elif head == 'False':
        return BooleanLiteral(False)
    elif head.startswith('"') and head.endswith('"'):
        return StringLiteral(head[1:len(head)-1])
    else:
        return 1

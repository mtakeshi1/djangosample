from __future__ import annotations

from .tokenizer import tokenize
from dataclasses import dataclass
from typing import List, Any


class LispError(Exception):
    def __init__(self, message):
        super().__init__(message)


class ParseError(LispError):
    def __init__(self, message):
        super().__init__(message)


class TODO(LispError):
    def __init__(self, message):
        super().__init__(message)


class Expression:
    def arity(self) -> int:
        return 1

    def eval(self, bindings) -> Expression:
        return ErrorExpression('not implemented')

    def as_number(self, bindings) -> int | float:
        raise ParseError('not a number ' + str(self))

    def as_boolean(self, bindings) -> bool:
        raise ParseError('not a boolean: ' + str(self))

    def call(self, bindings, args: List[Expression]) -> Expression:
        return ErrorExpression('not callable')

    def is_terminal(self):
        return False

    def resolve_symbol(self, bindings):
        return self


@dataclass(frozen=True)
class ErrorExpression(Expression):
    error_message: str

    def eval(self, bindings) -> Expression:
        return self

    def is_terminal(self):
        return True


@dataclass(frozen=True)
class NumberLiteral(Expression):
    num_value: int | float

    def as_number(self, bindings):
        return self.num_value

    def as_boolean(self, bindings):
        return self.num_value != 0

    def eval(self, bindings):
        return self

    def is_terminal(self):
        return True

    def __str__(self):
        return str(self.num_value)


@dataclass(frozen=True)
class StringLiteral(Expression):
    string: str

    def eval(self, bindings):
        return self

    def as_boolean(self, bindings):
        return self.string != ''

    def is_terminal(self):
        return True

    def __str__(self):
        return self.string


@dataclass(frozen=True)
class BooleanLiteral(Expression):
    boolean_value: bool

    def eval(self, bindings):
        return self

    def as_boolean(self, bindings) -> bool:
        return self.boolean_value

    def as_number(self, bindings):
        return 1 if self.boolean_value else 0

    def is_terminal(self):
        return True

    def __str__(self):
        return str(self.boolean_value)


@dataclass(frozen=True)
class Symbol(Expression):
    symbol: str

    def eval(self, bindings) -> Expression:
        r: Expression = bindings[self.symbol]
        while not r.is_terminal:
            r = r.eval(bindings)
        return r

    def as_boolean(self, bindings):
        return self.eval(bindings).as_boolean(bindings)

    def as_number(self, bindings):
        return self.eval(bindings).as_number(bindings)

    def resolve_symbol(self, bindings):
        r = self
        while isinstance(r, Symbol):
            r = bindings[r.symbol]
        return r


@dataclass(frozen=True)
class Tuple(Expression):
    members: List[Expression]

    def arity(self):
        return len(self.members)

    def eval(self, bindings) -> Expression:
        if self.arity() == 0:
            return self
        first = self.members[0].eval(bindings)
        # first should resolve to a callable
        return first.call(bindings, self.members[1:])

    def as_boolean(self, bindings):
        return self.eval(bindings).as_boolean(bindings)

    def as_number(self, bindings) -> int | float:
        return self.eval(bindings).as_number(bindings)



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
        return StringLiteral(head[1:len(head) - 1])
    elif head == ')':
        raise ParseError("Unexpected ')'")
    else:
        try:
            v = int(head)
            return NumberLiteral(v)
        except ValueError:
            try:
                v = float(head)
                return NumberLiteral(v)
            except ValueError:
                pass
        return Symbol(head)

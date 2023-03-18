from typing import List, Dict
from lisp.lisp.parser import Expression, Symbol, NumberLiteral, BooleanLiteral, Tuple, StringLiteral
from dataclasses import dataclass


class FunctionCall(Expression):
    def __init__(self, name: str, arg_names: List[Symbol], body: Expression):
        self.name = name
        self.arg_names = [c.symbol for c in arg_names]
        self.function_body = body

    def call(self, bindings, fargs) -> Expression:
        new_scope = dict(bindings)
        if len(fargs) < len(self.arg_names):
            missing = self.arg_names[len(fargs):]
            raise Exception(f"missing args: {missing}")
        for name, exp in zip(self.arg_names, fargs):
            new_scope[name] = exp.resolve_symbol(bindings)
        return self.function_body.eval(new_scope)

    # def eval(self, bindings) -> Expression:


class FunctionDef(Expression):
    def call(self, bindings, fargs) -> Expression:
        name: Symbol = fargs[0]
        arg_names: List[Symbol] = fargs[1].members
        body = fargs[2]
        bindings[name.symbol] = FunctionCall(name.symbol, arg_names, body)
        return StringLiteral('')


class NumberFunction(Expression):
    def __init__(self, name, collector):
        self.name = name
        self.collector = collector

    def call(self, bindings, fargs) -> Expression:
        as_numbers = [c.as_number(bindings) for c in fargs]
        return self.collector(as_numbers)


class IfFunction(Expression):
    def call(self, bindings, fargs) -> Expression:
        if fargs[0].as_boolean(bindings):
            return fargs[1].eval(bindings)
        else:
            return fargs[2].eval(bindings)


class Equals(Expression):
    def call(self, bindings, fargs) -> Expression:
        arg0 = fargs[0].eval(bindings)
        arg1 = fargs[1].eval(bindings)
        return BooleanLiteral(arg0 == arg1)


class NotEquals(Expression):
    def call(self, bindings, fargs) -> Expression:
        arg0 = fargs[0].eval(bindings)
        arg1 = fargs[1].eval(bindings)
        return BooleanLiteral(arg0 != arg1)


class Not(Expression):
    def call(self, bindings, fargs) -> Expression:
        return BooleanLiteral(not fargs[0].as_boolean(bindings))


class Head(Expression):
    def call(self, bindings, args: List[Expression]) -> Expression:
        arg0: Tuple = args[0]
        return arg0.members[0]


class Tail(Expression):
    def call(self, bindings, args: List[Expression]) -> Expression:
        arg0: Tuple = args[0]
        return Tuple(arg0.members[1:])


def natives():
    scope = dict()
    scope['+'] = NumberFunction('+', lambda args: NumberLiteral(sum(args)))
    scope['=='] = Equals()
    scope['not'] = Not()
    scope['if'] = IfFunction()
    scope['-'] = NumberFunction('-', lambda args: NumberLiteral(args[0] - args[1]))
    scope['<'] = NumberFunction('<', lambda args: BooleanLiteral(args[0] < args[1]))
    scope['<='] = NumberFunction('<=', lambda args: BooleanLiteral(args[0] <= args[1]))
    scope['>'] = NumberFunction('>', lambda args: BooleanLiteral(args[0] > args[1]))
    scope['>='] = NumberFunction('>=', lambda args: BooleanLiteral(args[0] >= args[1]))
    # scope['error'] =
    # scope['is_list']
    scope['head'] = Head()
    scope['tail'] = Tail()
    scope['def'] = FunctionDef()
    return scope

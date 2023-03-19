from __future__ import annotations

from .tokenizer import tokenize
from dataclasses import dataclass
from typing import List, Any
from lisp.lisp.lisp_types import *


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

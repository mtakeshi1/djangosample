from typing import List

single_char_tokens = '()'
token_separators = ' \t\n'


def parse_until(txt, i, delimiters):
    escaped = False
    tmp = ''
    while i < len(txt) and (escaped or txt[i] not in delimiters):
        if txt[i] == '\\':
            escaped = True
        else:
            tmp += txt[i]
            escaped = False
        i += 1
    return tmp, i


def tokenize(txt: str, i: int = 0, acc=None) -> List[str]:
    if acc is None:
        acc = []
    if i >= len(txt):
        return acc
    while i < len(txt) and txt[i] in token_separators:
        i += 1
    if i >= len(txt):
        return acc
    if txt[i] in single_char_tokens:
        s = txt[i]
        acc.append(s)
        return tokenize(txt, i + 1, acc)
    elif txt[i] == '"':
        string_literal, i = parse_until(txt, i+1, '"')
        acc.append('"' + string_literal + '"')
        return tokenize(txt, i + 1, acc)

    tmp, i = parse_until(txt, i, token_separators + single_char_tokens)
    acc.append(tmp)
    while i < len(txt) and txt[i] in token_separators:
        i += 1
    return tokenize(txt, i, acc)


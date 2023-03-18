from typing import List, Optional

connectors = ['de', 'com', 'c/', ' e', ' da', ' do', ',', ' ao', 'à']

suffix_connectors = ['suco', 'leite', 'assado', 'com ', 'sugo', 'c/ ', 'iogurte', 'shake', 'acebolado', '(', 'refogado',
                     'e ', 'preto', 'americana', 'vitamina']

meal_separators = ['arroz', 'sopa', 'espaguete', 'macarrão', 'canja', 'lasanha']


def read_file_pages(fname):
    lines = join_well_known(open(fname, 'r').readlines())
    acc = []
    current = []
    for line in lines:
        if line.strip() == 'EDUCAÇÃO INFANTIL':
            if len(current) > 0:
                acc.append(current)
            current = []
        elif line.startswith('SEGUNDA'):
            if len(current) > 0:
                acc.append(current)
            current = [line.strip()]

        elif len(line.strip()) > 0:
            current.append(line.strip())

    if len(current) > 0:
        acc.append(current)
    return acc


def parse_days(entries: List[str]):
    days = entries[:entries.index('LANCHE DA MANHÃ')]
    parsed = []
    for i in range(len(days) // 2):
        day_parts = days[2 * i].split(' ')
        parsed.append((day_parts[-1], days[2 * i + 1]))
    return parsed


def ends_with_connector(s: str) -> bool:
    for c in connectors:
        if s.lower().strip().endswith(c):
            return True
    return False


def join_parenthesis(page: List[str]) -> List[str]:
    acc = []
    i = 0
    r = []
    while i < len(page):
        if page[i].find('(') != -1 and page[i].find(')') == -1:
            tmp = ''
            while page[i].find(')') == -1:
                tmp = tmp + page[i] + ' '
                i += 1
            tmp = tmp + page[i]
            acc.append(tmp)
            i += 1
        else:
            acc.append(page[i])
            i += 1
    i = 0
    while i < len(acc):
        if i < len(acc) - 1 and acc[i + 1].find('(') != -1 and acc[i + 1].find('(') == -1:
            r.append(acc[i] + ' ' + acc[i + 1])
            i += 2
        else:
            r.append(acc[i])
            i += 1
    return r


def join_split_lines(page: List[str]) -> List[str]:
    acc = join_well_known(page)
    acc = join_parenthesis(acc)
    acc = connect_suffixes(acc)
    acc = split_special(acc)
    acc = split_known(acc)
    return acc


def join_well_known(page: List[str]) -> List[str]:
    acc = []
    i = 0
    while i < len(page):
        if i < len(page) - 1 and ends_with_connector(page[i]):
            acc.append(page[i].strip() + ' ' + page[i + 1].strip())
            i += 2
        else:
            acc.append(page[i].strip())
            i += 1
    return acc


def split_meal(s: str, candidates: List[str]) -> List[str]:
    for c in candidates:
        i = s.lower().find(c)
        if i > 0:
            before = split_meal(s[:i], candidates)
            after = split_meal(s[i:], candidates)
            return before + after
    return [s]


def split_known(page: List[str]) -> List[str]:
    acc = []
    for line in page:
        for part in split_meal(line, meal_separators):
            acc.append(part)
    return acc


def split_special(page: List[str]) -> List[str]:
    acc = []
    i = 0
    while i < len(page):
        if page[i].startswith('ALMOÇO '):
            acc.append('ALMOÇO')
            acc.append(page[i][7:])
            i += 1
        elif page[i].startswith('JANTAR '):
            acc.append('JANTAR')
            acc.append(page[i][7:])
            i += 1
        elif page[i].startswith('LANCHE DA TARDE '):
            acc.append('LANCHE DA TARDE')
            acc.append(page[i][16:])
            i += 1
        else:
            acc.append(page[i].strip())
            i += 1
    return acc


def starts_with_any(s: str, candidates: List[str]) -> bool:
    for c in candidates:
        if s.strip().lower().startswith(c):
            return True
    return False


def connect_suffixes(page: List[str]) -> List[str]:
    acc = []
    i = 0
    while i < len(page):
        if i < len(page) - 1 and starts_with_any(page[i + 1], suffix_connectors):
            tmp = page[i].strip() + ' '
            while i < len(page) - 1 and starts_with_any(page[i + 1], suffix_connectors):
                i += 1
                tmp = tmp + page[i].strip() + ' '

            acc.append(tmp.strip())
            i += 1
        else:
            acc.append(page[i])
            i += 1
    return acc


def strip_preffix(page: List[str], preffix: str) -> List[str]:
    acc = []
    for s in page:
        if s.startswith(preffix):
            acc.append(s[len(preffix):])
        else:
            acc.append(s)
    return acc


def only_last_piece(s: str):
    parts = s.split(' ')
    return parts[-1]


def join_days(days: List[str]) -> List[str]:
    acc = []
    for i in range(len(days) // 2):
        acc.append(days[2 * i] + ' ' + days[2 * i + 1])
    return acc


def try_spread(entries: List[str]) -> List[str]:
    acc = []
    current = ''

    for s in entries:
        if starts_with_any(s, meal_separators):
            if len(current) > 0:
                acc.append(current)
            current = s + ' '
        else:
            current += s + ' '

    if len(current) > 0:
        acc.append(current)

    return acc


def parse_sections(page: List[str]):
    lanche_manha_index = page.index('LANCHE DA MANHÃ')
    almoco_index = page.index('ALMOÇO')
    lanche_tarde_index = page.index('LANCHE DA TARDE')
    jantar_index = page.index('JANTAR')

    days = join_days([only_last_piece(d) for d in page[:lanche_manha_index]])
    cafe = page[lanche_manha_index + 1:almoco_index]
    cafe_map = {days[i]: cafe[i] for i in range(len(days))}
    almoco = try_spread(page[almoco_index + 1:lanche_tarde_index])
    almoco_map = {days[i]: almoco[i] for i in range(len(days))}
    lanche_tarde = page[lanche_tarde_index + 1: jantar_index]
    lanche_map = {days[i]: lanche_tarde[i] for i in range(len(days))}
    janta = try_spread(page[jantar_index + 1:])
    janta_map = {days[i]: janta[i] for i in range(len(days))}
    return days, cafe_map, almoco_map, lanche_map, janta_map


sections = read_file_pages('resources/cardapio-marco.txt')
for entry in sections:
    days, cafe, almoco, lanche, janta = parse_sections(join_split_lines(entry))
    print('dias')
    print(days)

    if len(days) != len(cafe):
        print('cafe da manha')
        print(cafe)
        raise Exception("erro cafe da manha")

    if len(almoco) != len(days):
        print('almoco')
        print(almoco)
        raise Exception("erro almoco")

    if len(lanche) != len(days):
        print('lanche da tarde')
        print(lanche)
        raise Exception("erro lanche")

    if len(janta) != len(days):
        print('janta')
        print(janta)
        raise Exception("erro janta")
    print("----------------------------------------------------------")

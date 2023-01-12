from grammar import Grammar
from item import Item


def read_pif(file_name):
    tokens = []
    with open(file_name) as pif:
        lines = pif.readlines()
        for line in lines:
            tokens.append(line.strip('()').split(',')[0].strip("'"))

    return tokens


def read_pif2(file_name):
    tokens = []
    with open(file_name) as pif:
        lines = pif.readlines()
        for line in lines:
            tokens.append(line.split(' ')[0])

    return tokens


if __name__ == '__main__':
    grammar = Grammar.get_grammar_from_file("grammars/grammar_robert.txt", True)
    # print(grammar.get_terminals)
    # print(grammar.get_nonterminals)
    # print(grammar.get_productions)
    # print(grammar.get_starting_symbol)

    # print(grammar.get_productions_for_nonterminal("decllist"))

    # print(grammar.verify_CFG())
    # print(grammar.closure([Item('S', ['SS'])]))

    # for state in grammar.col_can():
    #     print(str(state))

    # for prod in grammar.get_productions:
    #     print(str(prod))
    # print([str(prod) for prod in grammar.get_productions])
    # print(str(grammar.construct_parsing_table()))

    # print(str(read_pif('PIF_robert.OUT')))
    grammar.parse(read_pif('PIF_robert.out'))
    # grammar.parse(read_pif2('PIF_andrei.out'))

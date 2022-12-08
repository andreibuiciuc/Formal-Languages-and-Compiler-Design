from grammar import Grammar
from item import Item

if __name__ == '__main__':
    grammar = Grammar.get_grammar_from_file("grammar_test.txt", True)
    # print(grammar.get_terminals)
    # print(grammar.get_nonterminals)
    # print(grammar.get_productions)
    # print(grammar.get_starting_symbol)

    # print(grammar.get_productions_for_nonterminal("decllist"))

    # print(grammar.verify_CFG())
    # print(grammar.closure([Item('S', ['SS'])]))

    for state in grammar.col_can():
        print(str(state))

    for prod in grammar.get_productions:
        print(str(prod))
    # print([str(prod) for prod in grammar.get_productions])
    print(str(grammar.construct_parsing_table()))

    grammar.parse(['a', 'b', 'b', 'c'])

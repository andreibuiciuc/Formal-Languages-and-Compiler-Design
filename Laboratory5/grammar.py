from enum import Enum

class GrammarUtils(Enum):
    LINE_SEPARATOR = " "
    RIGHT_SIDE_SEPARATOR = "|"
    ASSIGNMENT_OPERATOR = "::="

class Grammar:
    def __init__(self, nonterminals, terminals, starting_symbol, productions):
        self.__terminals = terminals
        self.__nonterminals = nonterminals
        self.__starting_symbol = starting_symbol
        self.__productions = productions

    @property
    def get_terminals(self):
        return self.__terminals

    @property
    def get_nonterminals(self):
        return self.__nonterminals

    @property
    def get_starting_symbol(self):
        return self.__starting_symbol

    @property
    def get_productions(self):
        return self.__productions


    @staticmethod
    def get_grammar_from_file(file_name):
        with open(file_name) as f:
            lines = f.readlines()
        nonterminals = lines[0].strip().split(GrammarUtils.LINE_SEPARATOR.value)
        terminals = lines[1].strip().split(GrammarUtils.LINE_SEPARATOR.value)
        starting_symbol = lines[2].strip()
        productions = dict()
        for index in range(3, len(lines)):
            current_line = lines[index].strip()
            first_index = current_line.find(GrammarUtils.ASSIGNMENT_OPERATOR.value)
            production_left = current_line[0:first_index].strip()
            production_right = current_line[first_index + 3:]
            production_right = [x.strip() for x in production_right.split(GrammarUtils.RIGHT_SIDE_SEPARATOR.value)]
            productions[production_left] = production_right
        return Grammar(nonterminals, terminals, starting_symbol, productions)

    def get_productions_for_nonterminal(self, nonterminal):
        if nonterminal not in self.__productions:
            raise KeyError("Nonterminal does not exist")
        return self.__productions[nonterminal]

    def verify_CFG(self):
        for production_left in self.__productions.keys():
            if len(production_left.split(GrammarUtils.LINE_SEPARATOR.value)) > 1:
                return False
        return True

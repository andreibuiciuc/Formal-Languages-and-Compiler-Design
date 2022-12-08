from enum import Enum
from copy import deepcopy

from parsing_table import ParsingTable, Action, ActionType
from state import State
from item import Item


class GrammarUtils(Enum):
    LINE_SEPARATOR = " "
    RIGHT_SIDE_SEPARATOR = "|"
    ASSIGNMENT_OPERATOR = "::="
    EMPTY_STRING = ""


production_id = 0
def next_production_id():
    global production_id
    production_id += 1
    return production_id

class Production:
    def __init__(self, lhs, rhs):
        self.production_id = next_production_id()
        self.lhs = lhs
        self.rhs = rhs

    def __eq__(self, other):
        return self.lhs == other.lhs and self.rhs == other.rhs

    def __str__(self):
        return str(self.production_id) + '.  ' + self.lhs + " ::= " + str(self.rhs)

class Grammar:
    def __init__(self, nonterminals, terminals, starting_symbol, productions, enhance=False):
        self.__terminals = terminals
        self.__nonterminals = nonterminals
        self.__starting_symbol = starting_symbol
        self.__productions_for: dict = productions
        self.__states: list[State] = []
        self.__parsing_table = None
        if enhance:
            self._enhance_grammar()
        self.__set_productions()

    def __set_productions(self):
        self.__productions = []
        for lhs, right_hand_sides in self.__productions_for.items():
            for rhs in right_hand_sides:
                self.__productions.append(Production(lhs, rhs))

    def _enhance_grammar(self):
        self.__productions_for['S'] = [[self.__starting_symbol]]
        self.__starting_item = Item('S', [self.__starting_symbol])
        self.__starting_production = Production('S', [self.__starting_symbol])
        self.__starting_symbol = 'S'

    def _get_terminals_and_nonterminals(self):
        return self.__terminals + self.__nonterminals

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
    def get_grammar_from_file(file_name, enhance=False):
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
            production_right = [[y for y in x.split()] for x in production_right]
            productions[production_left] = production_right
        return Grammar(nonterminals, terminals, starting_symbol, productions, enhance)

    def get_productions_for_nonterminal(self, nonterminal):
        if nonterminal not in self.__productions_for:
            raise KeyError("Nonterminal does not exist")
        return self.__productions_for[nonterminal]

    def verify_CFG(self):
        for production_left in self.__productions_for.keys():
            if len(production_left.split(GrammarUtils.LINE_SEPARATOR.value)) > 1:
                return False
        return True

    def closure(self, items: list[Item]):
        result: set[Item] = set(items)
        done = False

        while not done:
            done = True
            new_items: set[Item] = set()
            for item in result:
                first_after_dot = item.first_after_dot()
                if first_after_dot not in self.__productions_for:  # first symbol after dot is terminal
                    continue
                for rhs in self.__productions_for[first_after_dot]:
                    new_item = Item(first_after_dot, rhs)
                    if new_item not in result:
                        new_items.add(new_item)
                        done = False

            result = result.union(new_items)

        return result

    def go_to(self, state: State, element):
        items_set: set[Item] = set()
        for item in state.get_items():
            first_after_dot = item.first_after_dot()
            if first_after_dot and element == first_after_dot.strip('"'):
                current_item = item.get_item_copy()
                current_item.advance_dot()
                items_set.add(current_item)

        return self.closure(list(items_set))

    def col_can(self):
        state_set: set[State] = set()
        state_set.add(State(self.closure([self.__starting_item])))
        done = False

        while not done:
            done = True
            new_states: set[State] = deepcopy(state_set)
            for state in state_set:
                for element in self._get_terminals_and_nonterminals():
                    next_state_items = State(self.go_to(state, element))
                    if len(next_state_items.get_items()) > 0 and next_state_items not in new_states:
                        new_states.add(next_state_items)
                        done = False

            state_set = new_states

        self.__states = list(state_set)
        return self.__states

    def get_production_for_item(self, item: Item) -> Production:
        production_to_find = Production(item.get_lhs(), item.get_rhs())
        for production in self.__productions:
            if production == production_to_find:
                return production

    def construct_parsing_table(self):
        if len(self.__states) == 0:
            self.col_can()

        number_of_conflicts = 0
        parsing_table = ParsingTable(list(self.__states), self._get_terminals_and_nonterminals())
        for state in self.__states:
            items_dot_end: list[Item] = []
            items_dot_not_end: list[Item] = []

            for item in state.get_items():
                if item.is_dot_at_the_end():
                    items_dot_end.append(item)
                else:
                    items_dot_not_end.append(item)

            if len(items_dot_end) > 0:
                if len(items_dot_end) > 1:
                    print('######################REDUCE REDUCE CONFLICT...')
                    number_of_conflicts += 1
                    print(str(state))
                    for item in items_dot_end:
                        print(self.get_production_for_item(item))
                    # return
                if len(items_dot_not_end) > 0:
                    print('######################REDUCE SHIFT CONFLICT...')
                    number_of_conflicts += 1
                    print('REDUCE: ' + str(state) + ' R' + str(self.get_production_for_item(items_dot_end[0])))
                    print('SHIFT: ')
                    for item in items_dot_not_end:
                        print(str(self.get_production_for_item(item)))
                    # return
                production = self.get_production_for_item(items_dot_end[0])

                if production == self.__starting_production:
                    parsing_table.add_action(state, Action(ActionType.ACCEPT))
                else:
                    parsing_table.add_action(state, Action(ActionType.REDUCE, production.production_id))
            else:
                parsing_table.add_action(state, Action(ActionType.SHIFT))
                for symbol in self._get_terminals_and_nonterminals():
                    new_state = State(self.go_to(state, symbol))
                    if len(new_state.get_items()) == 0:
                        continue
                    for obtained_state in self.__states:
                        if new_state == obtained_state:
                            new_state.set_id(obtained_state.get_id())

                    parsing_table.set_goto(state.get_id(), symbol, new_state.get_id())

        if number_of_conflicts > 0:
            print('Found ' + str(number_of_conflicts) + ' conflicts')
            exit(0)

        self.__parsing_table = parsing_table
        return parsing_table

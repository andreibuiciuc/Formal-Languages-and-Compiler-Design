import unittest

from grammar import Grammar, Production
from item import Item
from parsing_table import ParsingTable
from state import State


class TestGrammar(unittest.TestCase):
    def setUp(self):
        self.grammar = Grammar(
            nonterminals=["S", "X"],
            terminals=["a", "b"],
            starting_symbol="S",
            productions={
                "S": [["X", "a"], ["b"]],
                "X": [["a", "S"], ["b", "S"], ["X", "X"]]
            }
        )

    def test_get_terminals(self):
        self.assertEqual(self.grammar.get_terminals, ["a", "b"])

    def test_get_nonterminals(self):
        self.assertEqual(self.grammar.get_nonterminals, ["S", "X"])

    def test_get_starting_symbol(self):
        self.assertEqual(self.grammar.get_starting_symbol, "S")

    def test_get_productions(self):
        self.assertEqual(
            self.grammar.get_productions,
            [
                Production("S", ["X", "a"]),
                Production("S", ["b"]),
                Production("X", ["a", "S"]),
                Production("X", ["b", "S"]),
                Production("X", ["X", "X"]),
            ]
        )

    def test_closure(self):
        # Define a grammar with a few productions
        grammar = Grammar(
            nonterminals=['E', 'T', 'F'],
            terminals=['i', '+', '*', '(', ')'],
            starting_symbol='E',
            productions={
                'E': [['T', 'E1']],
                'E1': [['+', 'T', 'E1'], ['empty']],
                'T': [['F', 'T1']],
                'T1': [['*', 'F', 'T1'], ['empty']],
                'F': [['(', 'E', ')'], ['i']],
            }
        )

        # Define a set of items to use as input to the closure function
        items = [
            Item('E', ['T', 'E1'], 0),
            Item('F', ['(', 'E', ')'], 0),
            Item('E1', ['+', 'T', 'E1'], 0),
        ]

        # Compute the closure of the input items
        closure = grammar.closure(items)

        # Assert that the closure contains the expected items
        assert Item('E', ['T', 'E1'], 0) in closure
        assert Item('T', ['F', 'T1'], 0) in closure
        assert Item('F', ['(', 'E', ')'], 0) in closure
        assert Item('E1', ['+', 'T', 'E1'], 0) in closure
        assert Item('F', ['i'], 0) in closure

        assert len(closure) == 5

    def test_go_to(self):
        # create a test grammar
        grammar = Grammar(['E', 'E\'', 'T', 'T\'', 'F'], ['+', '*', '(', ')', 'id', 'num'], 'E', {
            'E': [['T', 'E\'']],
            'E\'': [['+', 'T', 'E\''], ['EPSILON']],
            'T': [['F', 'T\'']],
            'T\'': [['*', 'F', 'T\''], ['EPSILON']],
            'F': [['(', 'E', ')'], ['id'], ['num']]
        })

        # create a test state with some items
        items = {}
        state = State({Item('E', ['T', 'E\''], 0), Item('E\'', ['+', 'T', 'E\''], 0), Item('T', ['F', 'T\''], 0),
                       Item('T\'', ['*', 'F', 'T\''], 0), Item('F', ['(', 'E', ')'], 0), Item('F', ['id'], 0),
                       Item('F', ['num'], 0)})

        resulted_items = grammar.go_to(state, '+')

        # create a test set of items that the go_to function should return for the symbol '+'
        expected_items = set()
        self.assertIn(Item('F', ['id'], 0), resulted_items)
        self.assertIn(Item('F', ['num'], 0), resulted_items)
        self.assertIn(Item('E\'', ['+', 'T', 'E\''], 1), resulted_items)
        self.assertIn(Item('F', ['(', 'E', ')'], 0), resulted_items)
        self.assertIn(Item('T', ['F', 'T\''], 0), resulted_items)

        # create a test set of items that the go_to function should return for the symbol 'T'
        expected_items = set()
        expected_items.add(Item('E', ['T', 'E\''], 1))
        expected_items.add(Item('T', ['F', 'T\''], 1))

    def test_col_can(self):
        # create a test grammar
        grammar = Grammar(['A', 'B'], ['a', 'b'], 'A', {
            'A': [['A', 'B'], ['b']],
            'B': [['a']],
        }, True)

        col_can = grammar.col_can()

        states = [State({Item('A', ['b'], 0), Item('S', ['A'], 0), Item('A', ['A', 'B'], 0)}),
                  State({Item('A', ['A', 'B'], 1), Item('B', ['a'], 0), Item('S', ['A'], 1)}),
                  State({Item('A', ['A', 'B'], 2)}), State({Item('A', ['b'], 1)}), State({Item('B', ['a'], 1)})]

        for state in states:
            self.assertIn(state, col_can)

    def test_parse(self):
        # create a test grammar
        grammar = Grammar(['A', 'B'], ['a', 'b'], 'A', {
            'A': [['A', 'B'], ['b']],
            'B': [['a']],
        }, True)

        self.assertIsNone(grammar.parse(['b', 'b']))
        result = grammar.parse(['b', 'a', 'a'])
        self.assertIsNotNone(result)

        self.assertEqual(result.value, 'A')
        self.assertEqual(len(result.siblings), 2)
        self.assertEqual(result.siblings[0].value, 'A')
        self.assertEqual(len(result.siblings[0].siblings), 2)
        self.assertEqual(result.siblings[0].siblings[0].value, 'A')
        self.assertEqual(len(result.siblings[0].siblings[0].siblings), 1)
        self.assertEqual(result.siblings[0].siblings[0].siblings[0].value, 'b')
        self.assertEqual(len(result.siblings[0].siblings[1].siblings), 1)
        self.assertEqual(result.siblings[0].siblings[1].siblings[0].value, 'a')
        self.assertEqual(result.siblings[0].siblings[1].value, 'B')
        self.assertEqual(result.siblings[1].value, 'B')
        self.assertEqual(len(result.siblings[1].siblings), 1)
        self.assertEqual(result.siblings[1].siblings[0].value, 'a')





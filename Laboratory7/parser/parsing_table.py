from state import State
from enum import Enum


class ActionType(Enum):
    SHIFT = "SHIFT"
    REDUCE = "REDUCE"
    ACCEPT = "ACCEPT"


class Action:
    def __init__(self, action_type: ActionType, reduce_index=None):
        self.action_type = action_type
        self.reduce_index = reduce_index

    def __str__(self):
        result = self.action_type.value
        if self.action_type == ActionType.REDUCE:
            result += "(" + str(self.reduce_index) + ")"
        return result


class ParsingTable:
    def __init__(self, set_of_states: list[State], symbols: list[str]):
        self._states: list[State] = set_of_states
        self._symbols = symbols
        self._action: dict = {}
        self._goto: dict = {}

    def add_action(self, state: State, action: Action):
        if state.get_id() not in self._action:
            self._action[state.get_id()] = []
        self._action[state.get_id()].append(action)

    def get_action(self, state_id) -> list[Action]:
        return self._action[state_id]

    def set_goto(self, state_id, symbol, new_state_index):
        self._goto[(state_id, symbol)] = new_state_index

    def get_goto(self, state_id, symbol):
        if (state_id, symbol) not in self._goto:
            return None
        return self._goto[(state_id, symbol)]

    def __str__(self):
        result = []
        for state in self._states:
            actions_str = ''
            for action in self._action[state.get_id()]:
                actions_str += str(action) + ';'
            result.append(str(state) + '->' + actions_str + '\n')
            for symbol in self._symbols:
                if (state.get_id(), symbol) in self._goto:
                    result.append('goto(' + str(state.get_id()) + ', ' + symbol + ') = '
                                  + str(self._goto[(state.get_id(), symbol)]) + '\n')

        return ''.join(result)

from item import Item

state_id = 0


def get_next_id():
    global state_id
    state_id += 1
    return state_id


class State:
    def __init__(self, items: set[Item]):
        self._items = items
        self._id = get_next_id()

    def get_items(self):
        return self._items

    def get_id(self):
        return self._id

    def set_id(self, sid):
        self._id = sid

    def __hash__(self):
        return sum(hash(x) for x in self._items)

    def __eq__(self, other):
        for item in self._items:
            if item not in other.get_items():
                return False

        for item in other.get_items():
            if item not in self._items:
                return False

        return True

    def __str__(self):
        string_representation = str(self._id) + '  @  '
        for item in self._items:
            string_representation += str(item) + ';\t'
        return string_representation

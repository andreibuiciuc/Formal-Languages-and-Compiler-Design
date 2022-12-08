class Item:
    def __init__(self, lhs, rhs, dot_position=0):
        self._lhs = lhs
        self._rhs = rhs
        self._dot_position = dot_position

    def get_lhs(self):
        return self._lhs

    def get_rhs(self):
        return self._rhs

    def get_dot_position(self):
        return self._dot_position

    def first_after_dot(self):
        return self._rhs[self._dot_position] if self._dot_position < len(self._rhs) else None

    def advance_dot(self):
        self._dot_position = self._dot_position + 1

    def is_dot_at_the_end(self):
        return self._dot_position == len(self._rhs)

    def get_item_copy(self):
        return Item(self._lhs, self._rhs, self._dot_position)

    def __hash__(self):
        return hash((self._lhs, *self._rhs, self._dot_position))

    def __eq__(self, other):
        return self._lhs == other.get_lhs() and self._rhs == other.get_rhs() \
               and self._dot_position == other.get_dot_position()

    def __str__(self):
        rhs = ''
        for i in range(self._dot_position):
            rhs += self._rhs[i]
        rhs += '.'
        for i in range(self._dot_position, len(self._rhs)):
            rhs += self._rhs[i]
        return self._lhs + " -> " + rhs

class Node:
    def __init__(self, value, father=None, siblings=None):
        self.value = value
        self.father = father
        self.siblings = siblings or []

    def add_sibling(self, sibling):
        self.siblings.append(sibling)

    def __str__(self):
        # Print the value of the current node
        s = f'Value: {self.value}\n'

        # Print the father of the current node
        if self.father:
            s += f'Father: {self.father.value}\n'
        else:
            s += 'Father: None\n'

        # Print the siblings of the current node
        s += 'Siblings: ['
        for sibling in self.siblings:
            s += f'{str(sibling)}, '
        s += ']\n'

        return s


def print_tree(node, level=0):
    # Print the current node and its level in the tree
    print(f'{"|   " * level}{node.value}')

    # Recursively print the children of the current node
    for child in node.siblings:
        print_tree(child, level + 1)

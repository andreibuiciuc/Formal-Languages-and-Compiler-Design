from symbol_table import SymbolTable

symbol_table = SymbolTable()

symbol_table.insert_element('a', 10)
found_value = symbol_table.find_element('a')
assert found_value == 10

deleted_value = symbol_table.remove_element('a')
assert deleted_value == 10

found_value = symbol_table.find_element('a')
assert found_value == None

symbol_table.insert_element('a', 10)
symbol_table.insert_element('b', 20) # same hash => in the same bucket a -> b -> None

found_value_a = symbol_table.find_element('a')
assert found_value_a == 10
found_value_b = symbol_table.find_element('b')
assert found_value_b == 20

deleted_value_a = symbol_table.remove_element('a')
assert deleted_value_a == 10
found_value_a = symbol_table.find_element('a')
assert found_value_a is None
found_value_b = symbol_table.find_element('b')
assert found_value_b == 20

symbol_table.insert_element('a', 10)
symbol_table.insert_element('c', 30) # same hash => in the same bucket b -> a -> c -> None
deleted_value_a = symbol_table.remove_element('a')
assert(deleted_value_a == 10)
found_value_a = symbol_table.find_element('a')
assert found_value_a is None
found_value_b = symbol_table.find_element('b')
assert found_value_b == 20
found_value_c = symbol_table.find_element('c')
assert found_value_c == 30


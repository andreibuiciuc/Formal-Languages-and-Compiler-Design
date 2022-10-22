from hash_table.hash_table import HashTable

class SymbolTable:
    def __init__(self):
        self.__elements = HashTable()

    def insert_element(self, key, value):
        return self.__elements.insert_element(key=key, value=value)
    
    def remove_element(self, key):
        return self.__elements.remove_element(key=key)

    def find_element(self, key):
        return self.__elements.find_element(key=key)

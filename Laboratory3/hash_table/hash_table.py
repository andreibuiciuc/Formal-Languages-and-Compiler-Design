CAPACITY = 10

class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

class HashTable:
    def __init__(self):
        self.__capacity = CAPACITY
        self.__size = 0
        self.__elements = [None] * self.__capacity
    
    def __hash_function(self, key):
        # Hash function to generate a hash for a given key
        # Parameters: key -> a string
        # Return: hash value

        hashsum = 0
        for index, char in enumerate(key):
            hashsum = hashsum + (index + len(key)) ** ord(char)
            hashsum = hashsum % self.__capacity
        return hashsum

    def insert_element(self, key, value):
        # Insertion in the hash table
        # Parameters: key -> string, value
        if self.find_element(key) is not None:
            return

        self.__size = self.__size + 1
        index = self.__hash_function(key)
        current_node = self.__elements[index]

        if current_node is None:
            self.__elements[index] = Node(key, value)
        else:
            # Collision
            # We have to iterate to the end of the linked list and add the new node
            prev_node = current_node
            while current_node is not None:
                prev_node = current_node
                current_node = current_node.next
            prev_node.next = Node(key, value)

    def remove_element(self, key):
        # Removal of an element from the hash table
        # Parameters: key -> string
        # Return: the deleted value associated with the given key

        index = self.__hash_function(key)
        current_node = self.__elements[index]
        prev_node = None

        while current_node is not None and current_node.key != key:
            prev_node = current_node
            current_node = current_node.next

        if current_node is None:
            return None
        
        self.__size = self.__size - 1
        deleted_value = current_node.value

        if prev_node is None:
            self.__elements[index] = current_node.next
        else:
            prev_node.next = prev_node.next.next

        return deleted_value

    def find_element(self, key):
        # Searching for an element in the hash table based on its key
        # Parameters: key -> string
        # Return: the value of the node with the given key, otherwise None

        index = self.__hash_function(key)
        current_node = self.__elements[index]
        
        while current_node is not None and current_node.key != key:
            current_node = current_node.next

        if current_node is None:
            return None
        else:
            return current_node.value

    def get_position(self, key):
        # Retrieves the position of an element in the hash table and also in the inner linked list
        # Parameters: key -> string
        # Return a tuple containing the position in the table and in the innner linked list
        if self.find_element(key) != None:
            index_in_table = self.__hash_function(key)
            index_in_list = 0

            current_node = self.__elements[index_in_table]
            while current_node is not None and current_node.key != key:
                index_in_list = index_in_list + 1
                current_node = current_node.next
            
            return [index_in_table, index_in_list]
        return [-1, -1]

    def get_string_representation(self):
        string_representation = ""
        index = 0
        while index < len(self.__elements):
            string_representation = string_representation + str(index) + ": ["
            current_node = self.__elements[index]
            while current_node is not None:
                string_representation = string_representation + current_node.key + ", "
                current_node = current_node.next
            string_representation = string_representation + "]\n"
            index = index + 1
        return string_representation

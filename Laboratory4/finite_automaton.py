from enum import Enum

LINE_SEPARATOR = " "
EMPTY_STRING = ""

class TextFilepath(Enum):
   # Finite automaton filepaths
   FINITE_AUTOMATON_1 = "./in/FA.in"

class FiniteAutomaton:
    def __init__(self):
        self.__alphabet = set()
        self.__states = set()
        self.__initial_state = EMPTY_STRING
        self.__final_states = set()
        self.__transitions = dict()

    def __read_finite_automaton_file(self, finite_automaton_filepath):
        file = open(finite_automaton_filepath)

        # Read the line containing the states
        states_line = file.readline()[0:-1]
        self.__states = set(states_line.split(LINE_SEPARATOR))

        # Read the line containing the alphabet
        alphabet_line = file.readline()[0:-1]
        self.__alphabet = set(alphabet_line.split(LINE_SEPARATOR))

        # Read the line containing the initial state
        self.__initial_state = file.readline()[0]

        # Read the line containing the final states
        final_states_line = file.readline()[0:-1]
        self.__final_states = set(final_states_line.split(LINE_SEPARATOR))

        # Read the remaining lines, containing the transitions
        remaining_lines = file.readlines()
        for line in remaining_lines:

            source, alpha, destination = line.split(LINE_SEPARATOR)
            if destination[-1] == '\n': 
                destination = destination[:-1] 
            if source in self.__states and alpha in self.__alphabet and destination in self.__states:
              
                transition = (source, alpha)
                if transition in self.__transitions:
                    self.__transitions[transition].append(destination)
                else:
                    self.__transitions[transition] = [destination]
        
    def __check_if_finite_automaton_is_deterministic(self):
        for transition in self.__transitions:
            if len(self.__transitions[transition]) != 1:
                return False
        return True

    def __check_if_sequence_is_accepted(self, sequence):
        if sequence == EMPTY_STRING:
            return self.__initial_state in self.__final_states

        current_state = self.__initial_state
        
        for element in sequence:
            if element not in self.__alphabet:
                return False   
            transition = (current_state, element)
            if transition in self.__transitions:
                current_state = self.__transitions[transition][0]
            else:
                return False

        if current_state in self.__final_states:
            return True

        return False                    

    def __diplay_states(self, is_final_states=False):
        
        states_to_print = self.__states
        if is_final_states:
            states_to_print = self.__final_states

        for state in states_to_print:
            print(state, end=LINE_SEPARATOR)

    def __display_alphabet(self):
        for element in self.__alphabet:
            print(element, end=LINE_SEPARATOR)

    def __display_transitions(self):
        for transition in self.__transitions:
            transition_representation = "(" + transition[0] + ", " + transition[1] + ") -> "
            for t in self.__transitions[transition]:
                transition_representation += t + LINE_SEPARATOR
            print(transition_representation)

    @staticmethod
    def print_menu():
        print("1. Display states.")
        print("2. Display alphabet.")
        print("3. Display transitions.")
        print("4. Display initial state.")
        print("5. Display final states.")
        print("6. Check sequence.")
        print("0. Exit.")

    def start(self):
        print("Reading finite automaton from file...")
        self.__read_finite_automaton_file(TextFilepath.FINITE_AUTOMATON_1.value)
        print("Finished reading finite automaton.\n")

        is_deterministic = self.__check_if_finite_automaton_is_deterministic()
        if not is_deterministic:
            print("Finite automaton is not deterministic.\n")
        else:
            print("Finite automaton is deterministic.\n")

        done = False
        self.print_menu()
        while not done:
            option = int(input("\nEnter your option: "))
            if option == 0:
                done = True
            elif option == 1:
                print("States: ", end=EMPTY_STRING)
                self.__diplay_states(is_final_states=False)
            elif option == 2:
                print("Alphabet: ", end=EMPTY_STRING)
                self.__display_alphabet()
            elif option == 3:
                print("Transitions: ")
                self.__display_transitions()
            elif option == 4:
                print("Initial state: " + self.__initial_state, end=EMPTY_STRING)
            elif option == 5:
                print("Final states: ", end=EMPTY_STRING)
                self.__diplay_states(is_final_states=True)
            elif option == 6 and is_deterministic is True:
                sequence = input("Enter the sequence: ")
                result = self.__check_if_sequence_is_accepted(sequence)
                if result:
                    print("Sequence is valid.")
                else:
                    print("Sequence is not valid.")
            else:
                print("Option not valid. Try again.")

finite_automaton = FiniteAutomaton()
finite_automaton.start()

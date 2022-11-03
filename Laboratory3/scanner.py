import re
from symbol_table import SymbolTable

P1_TXT_FILEPATH = "D:\\uni-projects\\formal-languages\\Formal-Languages-and-Compiler-Design\\Laboratory3\\p1.txt"
P2_TXT_FILEPATH = "D:\\uni-projects\\formal-languages\\Formal-Languages-and-Compiler-Design\\Laboratory3\\p2.txt"
P3_TXT_FILEPATH = "D:\\uni-projects\\formal-languages\\Formal-Languages-and-Compiler-Design\\Laboratory3\\p3.txt"
PERR_TXT_FILEPATH = "D:\\uni-projects\\formal-languages\\Formal-Languages-and-Compiler-Design\\Laboratory3\\perr.txt"

ST_OUT_FILEPATH = "D:\\uni-projects\\formal-languages\\Formal-Languages-and-Compiler-Design\\Laboratory3\\ST.out"
PIF_OUT_FILEPATH = "D:\\uni-projects\\formal-languages\\Formal-Languages-and-Compiler-Design\\Laboratory3\\PIF.out"

RESERVED_WORDS = ["@let", "@check", "@otherwise", "@iterate", "@stop", "@print", "@enter", "@while", '->', '<-']
OPERATORS = ["+", "-", "*", "/", "%", "=", "==", "is", "!=", "is not", "<", "<=", ">", ">=", "not", "and", "or", "++", "--"]
SEPARATORS = ["\n", "\t", ":", " ", "(", ")", ","]

NUMERIC_REGEX = "^0|[+|-][1-9]([0-9])*|[1-9]([0-9])*|[+|-][1-9]([0-9])*"
CHAR_REGEX = "^\'[a-zA-Z0-9_?!#*./%+=<>;)(}{ ]\'"
STRING_REGEX = "^\"[a-zA-Z0-9_?!#*./%+=<>;)(}{ ]+\""
IDENTIFIER_REGEX = "^[a-zA-Z]([a-z|A-Z|0-9])*$"

IDENTIFIER_CODE = "ID"
CONSTANT_CODE = "CONST"

class Scanner:
    def __init__(self):
        self.__symbol_table = SymbolTable()
        # pairs (token, position in Symbol Table)
        self.__pif = []

    def __insert_into_pif(self, token, index):
        self.__pif.append((token, index))

    @staticmethod
    def is_constant(token):
        return bool(re.match(NUMERIC_REGEX, token)) or bool(re.match(CHAR_REGEX, token)) or bool(re.match(STRING_REGEX, token))

    @staticmethod
    def is_reserved_word(token):
        return RESERVED_WORDS.__contains__(token)

    @staticmethod
    def is_operator(token):
        return OPERATORS.__contains__(token)

    @staticmethod
    def is_separator(token):
        return SEPARATORS.__contains__(token)

    @staticmethod
    def is_identifier(token):
        return bool(re.match(IDENTIFIER_REGEX, token))

    def __get_string_constant(self, line, index):
        string_constant = line[index]
        index = index + 1
        done = False
        while not done:
            string_constant = string_constant + line[index]
            if line[index] == "\"":
                done = True
            index = index + 1

        return string_constant

    def __get_operator(self, line, index):
        operator = line[index] + line[index + 1]
        if self.is_operator(operator):
            return operator
        return line[index]

    def __get_token(self, line, index):
        token = ""
        while index < len(line) and not self.is_separator(line[index]) \
            and not (line[index] == "!" or self.is_operator(line[index])) \
            and line[index] != ' ':
            token = token + line[index]
            index = index + 1
        return token

    def __tokenize(self, line):
        tokens = []
        i = 0
        while i < len(line):
            if self.is_separator(line[i]) and line[i] != ' ':
                tokens.append(line[i])
            elif line[i] == "\"":
                string_constant = self.__get_string_constant(line, i)
                tokens.append(string_constant)
                i = i + len(string_constant) - 1
            elif line[i] == "!" or self.is_operator(line[i]):
                operator = self.__get_operator(line, i)
                tokens.append(operator)
                i = i + len(operator) - 1
            elif line[i] != ' ':
                token = self.__get_token(line, i)
                tokens.append(token)
                i = i + len(token) - 1
            i = i + 1
        return tokens

    def __insert_into_pif(self, tokens_and_line):
        is_valid = True
        for pair in tokens_and_line:
            token, line_number = pair[0], pair[1]

            if self.is_operator(token) or self.is_reserved_word(token) or self.is_separator(token):
                self.__pif.append([token, [-1, -1]])
            elif self.is_identifier(token):
                self.__symbol_table.insert_element(token, None)
                sym_table_position = self.__symbol_table.get_position(token)
                self.__pif.append([IDENTIFIER_CODE, sym_table_position])
            elif self.is_constant(token):
                self.__symbol_table.insert_element(token, None)
                sym_table_position = self.__symbol_table.get_position(token)
                self.__pif.append([CONSTANT_CODE, sym_table_position])
            else:
                is_valid = False
                print("Error: line " + str(line_number) + ", token: " + token)
        
        if is_valid:
            print("Lexically correct")
        else:
            print("Lexically incorrect")

    def scan(self, program_file_path):
        file = open(program_file_path, 'r')
        current_line_number = 1
        tokens_and_line = []

        for line in file:
            tokens = self.__tokenize(line)
            for token in tokens:
                tokens_and_line.append([token, current_line_number])
            current_line_number = current_line_number + 1                

        self.__insert_into_pif(tokens_and_line)

    def get_results(self):
        symbol_table_string_representation = self.__symbol_table.get_string_representation()
        f = open(ST_OUT_FILEPATH, "w")
        f.write(symbol_table_string_representation)
        f = open(PIF_OUT_FILEPATH, "w")
        f.write(str(self.__pif))

scanner = Scanner()
scanner.scan(P1_TXT_FILEPATH)
scanner.get_results()
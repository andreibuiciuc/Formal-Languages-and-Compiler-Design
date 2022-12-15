import re
from enum import Enum

from symbol_table import SymbolTable

class TextFilepath(Enum):
    # Programs filepaths
    P1_TXT_FILEPATH = "./programs/p1.txt"
    P2_TXT_FILEPATH = "./programs/p2.txt"
    P3_TXT_FILEPATH = "./programs/p3.txt"
    PERR_TXT_FILEPATH = "./programs/perr.txt"
    # Symbol table and PIF filepaths
    ST_OUT_FILEPATH = "./out/ST.out"
    PIF_OUT_FILEPATH = "./out/PIF.out"

class ScannerUtils(Enum):
    RESERVED_WORDS = ["@let", "@check", "@otherwise", "@iterate", "@stop", "@print", "@enter", "@while"]
    OPERATORS = ["+", "-", "*", "/", "%", "=", "==", "!=", "<", "<=", ">", ">=", "&&", "||", "++", "--"]
    SEPARATORS = ["\n", "\t", ":", " ", "(", ")", ","]
    # Regex for constants and identifiers
    NUMERIC_REGEX = "^0|[+|-]*[1-9]([0-9])*$"
    CHAR_REGEX = "^\'[a-zA-Z0-9_?!#*./%+=<>;)(}{ ]\'"
    STRING_REGEX = "^\"[a-zA-Z0-9_?!#*./%+=<>;)(}{ ]*\""
    BOOLEAN_REGEX = "^(true)|(false)$"
    IDENTIFIER_REGEX = "^[a-zA-Z][a-zA-Z0-9]{0,30}"
    # Codes and default index for PIF
    IDENTIFIER_CODE = "ID"
    CONSTANT_CODE = "CONST"
    DEFAULT_INDEX = [-1, -1]

class Scanner:
    def __init__(self):
        self.__symbol_table = SymbolTable()
        self.__pif = []
        self.__is_lexically_correct = True

    @staticmethod
    def is_constant(token):
        return bool(re.match(ScannerUtils.NUMERIC_REGEX.value, token)) or \
               bool(re.match(ScannerUtils.CHAR_REGEX.value, token)) or \
               bool(re.match(ScannerUtils.STRING_REGEX.value, token)) or \
               bool(re.match(ScannerUtils.BOOLEAN_REGEX.value, token)) 

    @staticmethod
    def is_reserved_word(token):
        return token in ScannerUtils.RESERVED_WORDS.value

    @staticmethod
    def is_operator(token):
        return token in ScannerUtils.OPERATORS.value

    @staticmethod
    def is_separator(token):
        return token in ScannerUtils.SEPARATORS.value

    @staticmethod
    def is_identifier(token):
        return bool(re.match(ScannerUtils.IDENTIFIER_REGEX.value, token))

    @staticmethod
    def __print_lexical_error(line_number, token):
        if token[-1] == '\n':
            token = token[0:-1]
        print("Lexical error -> line: " + str(line_number) + ", token: " + token)

    def __get_pif_string_representation(self):
        pif_string_representation = ""
        for pair in self.__pif:
            code, index = pair
            if code == '\n':
                code = "new_line"
            index_str = "(" + str(index[0]) + ", " + str(index[1]) + ")"
            pif_string_representation += code + index_str.rjust(30 - len(code)) + "\n"
        return pif_string_representation

    def __get_string_constant(self, line, index):
        string_constant = line[index]
        index = index + 1
        done = False
        while not done and index < len(line):
            string_constant = string_constant + line[index]
            if line[index] == "\"":
                done = True
            else:
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
        # Splits the given line into tokens
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

    def __check_tokens_by_line(self, token, line_number):
        if self.is_reserved_word(token) or self.is_operator(token) or self.is_separator(token):
            # Check if the current token is a reserved word, an operator or a separator.
            # If so, the value inserted in PIF will be the pair [token, DEFAULT_INDEX]
            self.__pif.append([token, ScannerUtils.DEFAULT_INDEX.value])
        elif self.is_identifier(token) and not self.is_constant(token):
            # Check if the current token is an identifier.
            # If not in the Symbol table already, add it and insert into PIF the pair [ID, position]
            sym_table_position = self.__symbol_table.get_position(token)
            if (sym_table_position == ScannerUtils.DEFAULT_INDEX.value):
                self.__symbol_table.insert_element(token, None)
                sym_table_position = self.__symbol_table.get_position(token)
            self.__pif.append([ScannerUtils.IDENTIFIER_CODE.value, sym_table_position])
        elif self.is_constant(token):
            # Check if the current token is a constant.
            # If not in the Symbol table already, add it and insert into PIF the pair [CONSTANT, position]
            sym_table_position = self.__symbol_table.get_position(token)
            if (sym_table_position == ScannerUtils.DEFAULT_INDEX.value):
                self.__symbol_table.insert_element(token, None)
                sym_table_position = self.__symbol_table.get_position(token)
            self.__pif.append([ScannerUtils.CONSTANT_CODE.value, sym_table_position])
        else:
            # The token cannot be classified
            self.__is_lexically_correct = False
            self.__print_lexical_error(line_number, token)

    def scan(self, program_file_path):
        file = open(program_file_path, 'r')
        current_line_number = 1

        for line in file:
            tokens = self.__tokenize(line)
            for token in tokens:
                self.__check_tokens_by_line(token, current_line_number)                
            current_line_number = current_line_number + 1

        if self.__is_lexically_correct:
            print("Lexically correct.")
        else:
            print("Lexically incorrect.")

    def get_results(self):
        # Write the Symbol Table string representation to the output file
        symbol_table_string_representation = self.__symbol_table.get_string_representation()
        f = open(TextFilepath.ST_OUT_FILEPATH.value, "w")
        f.write(symbol_table_string_representation)

        # Write the PIF string representation to the output file
        pif_string_representation = self.__get_pif_string_representation()
        f = open(TextFilepath.PIF_OUT_FILEPATH.value, "w")
        f.write(str(pif_string_representation))

scanner = Scanner()
scanner.scan(TextFilepath.P1_TXT_FILEPATH.value)
scanner.get_results()
import sys

class Token:
    def __init__(self, token_type, value):
        self.token_type = token_type
        self.value = value
    
    def __repr__(self):
        return f"<{self.token_type}, {self.value}>"

# lexer class using state transitions (no libraries this time)
class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.position = 0  
        self.tokens = []  
        self.current_char = self.source_code[self.position] if self.source_code else None
        self.last_token_type = None  

    def advance(self):
        self.position += 1
        if self.position < len(self.source_code):
            self.current_char = self.source_code[self.position]
        else:
            self.current_char = None

    def scan(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.advance()
            # identifiers (A-Z)
            elif self.current_char.isalpha() and self.current_char.isupper():
                self.tokens.append(self.state_identifier())
            # assignment operator =
            elif self.current_char == '=':
                if self.last_token_type != "ID":  # Check if '=' has a preceding identifier
                    self.tokens.append(Token("ERROR", "Missing identifier before '='"))
                self.tokens.append(Token("ASSIGNMENT_OP", "="))
                self.advance()
            # matrix dimensions 
            elif self.current_char == '(':
                self.tokens.append(self.state_matrix())
            # operators 'x' and '+'
            elif self.current_char == 'x':
                self.tokens.append(Token("OP_MUL", "x"))
                self.advance()
            elif self.current_char == '+':
                self.tokens.append(Token("OP_ADD", "+"))
                self.advance()
            # keyword 'display'
            elif self.current_char == 'd':
                self.tokens.append(self.state_display())
            # all unknown chars are treated as errors
            else:
                self.tokens.append(Token("ERROR", f"Unknown character '{self.current_char}'"))
                self.advance()   

        return self.tokens

    # (single capital letters A-Z)
    def state_identifier(self):
        identifier = self.current_char
        self.advance()  
        self.last_token_type = "ID"  
        return Token("ID", identifier)

    # matrix dimensions 
    def state_matrix(self):
        matrix_value = self.current_char 
        self.advance()

        while self.current_char is not None and (self.current_char.isdigit() or self.current_char in ',)'):
            matrix_value += self.current_char
            self.advance()

        return Token("MATRIX", matrix_value)

    # keyword 'display'
    def state_display(self):
        display_keyword = ""
        for expected_char in "display":
            if self.current_char == expected_char:
                display_keyword += self.current_char
                self.advance()
            else:
                return Token("ERROR", f"Invalid keyword: '{display_keyword}'")

        self.last_token_type = "DISPLAY"
        return Token("DISPLAY", "display")


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 scanner.py <source_code_file>")
        return
    
    file_path = sys.argv[1]
    with open(file_path, 'r') as file:
        source_code = file.read()

    lexer = Lexer(source_code)
    tokens = lexer.scan()

    for token in tokens:
        print(token)

if __name__ == "__main__":
    main()

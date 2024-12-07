import sys

class Token:
    def __init__(self, token_type, value):
        self.token_type = token_type
        self.value = value
    
    def __repr__(self):
        return f"<{self.token_type}, {self.value}>"

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.ast = None
        self.errors = []  # To track parsing errors

    def current_token(self):
        return self.tokens[self.current_token_index] if self.current_token_index < len(self.tokens) else None

    def advance(self):
        self.current_token_index += 1

    def match(self, expected_type):
        token = self.current_token()
        if token and token.token_type == expected_type:
            self.advance()
            return token
        else:
            error_message = f"Expected {expected_type}, but got {token}"
            self.errors.append(error_message)
            return None

    def parse(self):
        self.ast = {"Program": []}
        try:
            while self.current_token():
                statement = self.parse_statement()
                if statement:
                    self.ast["Program"].append(statement)
        except SyntaxError as e:
            self.errors.append(str(e))
        return self.ast

    def parse_statement(self):
        token = self.current_token()
        if token.token_type == "ID":
            return self.parse_assignment_or_multiplication()
        elif token.token_type == "DISPLAY":
            return self.parse_display()
        else:
            self.errors.append(f"Unexpected token: {token}")
            self.advance()  # Skip invalid token
            return None

    def parse_assignment_or_multiplication(self):
        id_token = self.match("ID")
        if not self.match("ASSIGNMENT_OP"):
            return None  # Missing '=' error already added in `match`
        
        if self.current_token() and self.current_token().token_type == "MATRIX":  # Matrix assignment
            matrix = self.parse_matrix()
            return {
                "MatrixAssignment": {
                    "ID": {"Value": id_token.value if id_token else None},
                    "Matrix": [{"Row": row} for row in matrix]
                }
            }
        elif self.current_token() and self.current_token().token_type == "ID":  # Matrix multiplication
            left_operand = self.match("ID").value if self.current_token() else None
            operator = self.match("OP_MUL").value if self.current_token() else None
            right_operand = self.match("ID").value if self.current_token() else None
            return {
                "MatrixMultiplicationAssignment": {
                    "ID": {"Value": id_token.value if id_token else None},
                    "Multiplication": {
                        "Operand1": f"ID ({left_operand})" if left_operand else None,
                        "Operator": operator,
                        "Operand2": f"ID ({right_operand})" if right_operand else None
                    }
                }
            }
        else:
            self.errors.append(f"Invalid statement after ID {id_token.value if id_token else None}")
            return None

    def parse_matrix(self):
        matrix_rows = []
        while self.current_token() and self.current_token().token_type == "MATRIX":
            matrix_rows.append(self.match("MATRIX").value)
        return matrix_rows

    def parse_display(self):
        if not self.match("DISPLAY"):
            return None
        id_token = self.match("ID")
        if not id_token:
            self.errors.append("Missing ID in display statement.")
            return None
        return {
            "DisplayStatement": {
                "Display": "display",
                "ID": {"Value": id_token.value}
            }
        }

def load_tokens(file_path):
    tokens = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            token_type, token_value = line[1:-1].split(", ")
            tokens.append(Token(token_type, token_value))
    return tokens

def print_tree(node, indent=0, file=None):
    """Recursively prints the AST in a tree-like format."""
    if isinstance(node, dict):
        for key, value in node.items():
            if file:
                file.write(" " * indent + key + "\n")
            else:
                print(" " * indent + key)
            print_tree(value, indent + 4, file)
    elif isinstance(node, list):
        for item in node:
            print_tree(item, indent, file)
    else:
        if file:
            file.write(" " * indent + str(node) + "\n")
        else:
            print(" " * indent + str(node))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 parser.py <token_file>")
        sys.exit(1)
    
    token_file = sys.argv[1]
    tokens = load_tokens(token_file)
    
    parser = Parser(tokens)
    ast = parser.parse()

    if parser.errors:
        print("Errors detected:")
        for error in parser.errors:
            print(f"- {error}")
    else:
        with open("generated_ast.txt", "w") as f:
            f.write("Generated Abstract Syntax Tree (AST):\n")
            print_tree(ast, file=f)

        print("\nGenerated Abstract Syntax Tree (AST):")
        print_tree(ast)

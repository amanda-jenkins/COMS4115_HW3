import json
import sys

class CodeGeneratorC:
    def __init__(self, ast):
        self.ast = ast
        self.output = []
        self.displayed_matrices = set()  # To track already displayed matrices

    def generate_code(self):
        if not self.ast or "Program" not in self.ast:
            print("Invalid AST provided. Code generation aborted.")
            return ""

        self.output.append("#include <stdio.h>\n")
        self.output.append("// Function to print a matrix")
        self.output.append("void printMatrix(int rows, int cols, int matrix[rows][cols]) {")
        self.output.append("    for (int i = 0; i < rows; i++) {")
        self.output.append("        for (int j = 0; j < cols; j++) {")
        self.output.append("            printf(\"%d \", matrix[i][j]);")
        self.output.append("        }")
        self.output.append("        printf(\"\\n\");")
        self.output.append("    }")
        self.output.append("}\n")

        self.output.append("int main() {")
        for node in self.ast["Program"]:
            if "MatrixAssignment" in node:
                self.handle_matrix_assignment(node["MatrixAssignment"])
            elif "MatrixMultiplicationAssignment" in node:
                self.handle_matrix_multiplication(node["MatrixMultiplicationAssignment"])
            elif "DisplayStatement" in node:
                self.handle_display(node["DisplayStatement"])
        self.output.append("    return 0;")
        self.output.append("}")

        return "\n".join(self.output)

    def handle_matrix_assignment(self, assignment):
        matrix_id = assignment["ID"]["Value"]
        rows = [row["Row"] for row in assignment["Matrix"]]
        rows_as_lists = [f"{{{row.strip('()')}}}" for row in rows]
        num_rows = len(rows)
        num_cols = len(rows[0].split(","))
        matrix_declaration = f"int {matrix_id}[{num_rows}][{num_cols}] = {{\n    " + ",\n    ".join(rows_as_lists) + "\n};"
        self.output.append(f"    {matrix_declaration}")

    def handle_matrix_multiplication(self, multiplication):
        result_id = multiplication["ID"]["Value"]
        operand1 = multiplication["Multiplication"]["Operand1"].split()[1]
        operand2 = multiplication["Multiplication"]["Operand2"].split()[1]

        self.output.append(f"    int {result_id}[2][2] = {{0}};")
        self.output.append(f"    for (int i = 0; i < 2; i++) {{")
        self.output.append(f"        for (int j = 0; j < 2; j++) {{")
        self.output.append(f"            for (int k = 0; k < 2; k++) {{")
        self.output.append(f"                {result_id}[i][j] += {operand1}[i][k] * {operand2}[k][j];")
        self.output.append(f"            }}")
        self.output.append(f"        }}")
        self.output.append(f"    }}")

    def handle_display(self, display):
        matrix_id = display["ID"]["Value"]
        if matrix_id in self.displayed_matrices:
            print(f"Skipping redundant display statement for matrix '{matrix_id}'.")
            return  # Skip redundant display
        self.displayed_matrices.add(matrix_id)
        self.output.append(f"    printf(\"Matrix {matrix_id}:\\n\");")
        self.output.append(f"    printMatrix(2, 2, {matrix_id});")

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 code_gen.py <ast_json_file>")
        sys.exit(1)

    ast_file = sys.argv[1]
    with open(ast_file, "r") as f:
        ast = json.load(f)

    generator = CodeGeneratorC(ast)
    generated_code = generator.generate_code()

    if generated_code:
        with open("output_code.c", "w") as f:
            f.write(generated_code)
        print("Code generation completed successfully. Output saved to 'output_code.c'.")

if __name__ == "__main__":
    main()

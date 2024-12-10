#!/bin/bash

# Check if a source code file was provided as an argument
if [ "$#" -ne 1 ]; then
  echo "Usage: ./run_compiler.sh <source_code_file>"
  exit 1
fi

SOURCE_FILE=$1

# Check if the file exists
if [ ! -f "$SOURCE_FILE" ]; then
  echo "Error: File '$SOURCE_FILE' not found!"
  exit 1
fi

# Step 1: Run the scanner to tokenize the input
echo "Running scanner..."
python3 scanner.py "$SOURCE_FILE" > tokens.txt

if [ $? -ne 0 ]; then
  echo "Error: Scanner failed."
  exit 1
fi

# Step 2: Run the parser with the generated tokens
echo "Running parser..."
python3 parser1.py tokens.txt > parser_output.txt 2>&1

if [ $? -ne 0 ]; then
  echo "Error: Parser failed:"
  cat parser_output.txt
  exit 1
fi

# Check for parser errors in output
if grep -q "Errors detected:" parser_output.txt; then
  echo "Parser reported errors:"
  cat parser_output.txt
  exit 1
fi

# Notify user about the generated AST file
echo "Parsing completed successfully. The AST is saved to 'generated_ast.json'."

# Step 3: Run the code generation stage
echo "Running code generation..."
python3 code_gen.py generated_ast.json

if [ $? -ne 0 ]; then
  echo "Error: Code generation failed."
  exit 1
fi

echo "Code generation completed successfully."

# Step 4: Compile the generated C code
echo "Compiling C code..."
gcc -o output_code output_code.c

if [ $? -ne 0 ]; then
  echo "Error: Compilation of C code failed."
  exit 1
fi

# Step 5: Run the compiled executable
echo "Running the compiled program..."
./output_code

if [ $? -ne 0 ]; then
  echo "Error: Execution of compiled program failed."
  exit 1
fi

echo "Program executed successfully. Output displayed above."

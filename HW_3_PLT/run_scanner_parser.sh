#!/bin/bash

# Check if a source code file was provided as an argument
if [ "$#" -ne 1 ]; then
  echo "Usage: ./run_scanner_parser.sh <source_code_file>"
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
python3 parser1.py tokens.txt

if [ $? -ne 0 ]; then
  echo "Error: Parser failed."
  exit 1
fi

# Notify user about the generated AST file
echo "Parsing completed successfully IF the program is without error and the AST is saved to 'generated_ast.txt'."

#!/bin/bash

# Check if a source code file was provided as an argument
if [ "$#" -ne 1 ]; then
  echo "Usage: ./run_scanner.sh <source_code_file>"
  exit 1
fi

# Assign the first argument as the input file
SOURCE_FILE=$1

# Check if the file exists
if [ ! -f "$SOURCE_FILE" ]; then
  echo "Error: File '$SOURCE_FILE' not found!"
  exit 1
fi

# Run the Python scanner script with the source file as input
python3 scanner.py "$SOURCE_FILE"

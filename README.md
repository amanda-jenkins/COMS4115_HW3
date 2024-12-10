# COMS4115_HW3 Programming Assignment 3: Code Generation
# Team: Amanda Jenkins (alj2155) 

## Overview
In the code generation stage, I take the Abstract Syntax Tree (AST) from my custom matrix operation language (inspired by Python)and translate it into low level-C code (my target language).

 The high-level operations of my matrix language like matrix initialization, multiplication, and displaying results, are transformed into C constructs. By doing this, I bridge the gap between the high-level language I created and an executable format and target language where the program can run efficiently on platforms that support C.

## 5 sample input programs

### Sample Program 1: Valid Matrix Declaration, Multiplication, and Display of Results


Input Program (example.txt):
```
A = (2,2)
    (3,4)
B = (5,6)
    (7,8)
C = A x B
display C
```


Expected Output:
```
Matrix C:
32 28 
55 50 
Program executed successfully. Output displayed above.
```

### 2. Sample Program 2: Missing Identifier(s) Before Assignment Operator

Input Program (example.txt):
```
 = (2,2)
    (3,4)
B = (5,6)
    (7,8)
C = A x B
display C
```


Expected Output:
```
Parser reported errors. See details below:
Errors detected:
- Unexpected token: <ERROR, Missing identifier before '='>
- Unexpected token: <ASSIGNMENT_OP, =>
- Unexpected token: <MATRIX, (2,2)>
- Unexpected token: <MATRIX, (3,4)>
``` 

Does not compile but reports errors from the specific stage that has errors and shows unexpected tokens are such errors, modeling after how compilers error-check programs.

### 3. Redudant Code Elimination for Efficiency

Input Program (example.txt):
```
A = (2,2)
    (3,4)
B = (5,6)
    (7,8)
C = A x B
display C
display C
```

Expected Output:
```
Matrix C:
24 28 
43 50 
Program executed successfully. Output displayed above.
```



### 4. Unknown Symbols in Program

Input Program (example.txt):
```
A = (2,2)&
    (3,4) %
B = (5,6)$
    (7,8)     
    ?
C = A x B
display C
```

Expected Output:
```
Parser reported errors:
Errors detected:
- Unexpected token: <ERROR, Unknown character '&'>
- Unexpected token: <MATRIX, (3,4)>
- Unexpected token: <ERROR, Unknown character '%'>
- Unexpected token: <ERROR, Unknown character '$'>
- Unexpected token: <MATRIX, (7,8)>
- Unexpected token: <ERROR, Unknown character '?'>
```
Does not compile but reports errors from the specific stage that has errors and shows unexpected tokens are such errors, modeling after how compilers error-check programs.



### 5. Matrix Multiplication with Multiple Displays & Redundancy 
Input Program (example.txt): 

```
A = (2,2)
    (3,4) 
B = (5,6)
    (7,8)   
C = A x B
display C
display A
display B
display B
```

Expected Output: 
```
Matrix C:
24 28 
43 50 
Matrix A:
2 2 
3 4 
Matrix B:
5 6 
7 8 
Program executed successfully. Output displayed above.
```

## Running Code 

To test the programs using the compiler pipeline, follow these steps:
1. Prepare the Input File: Save program in a example.txt file which is the source code file.
2. Run the Compiler Script (run_complier.sh): 
    * cd into folder "HW_3_PLT" if you have not already
    * chmod +x run_complier.sh
    * run_compiler.sh to process the input file.
        *  For example, ./run_compiler.sh example.txt
3. Output - the script will go through the following steps:

Scanning: Tokenizes the input file into recognizable components.
Parsing: Generates an Abstract Syntax Tree (AST) or reports syntax errors.
Code Generation: Creates the corresponding C code if no errors are found.
Execution: Runs the compiled program to produce the final output.

## Detailed description of each step

### 1. Scanning (Lexical Analysis)
The scanner reads the source code file and breaks it into meaningful units called tokens. Each token represents a fundamental building block of the program, such as identifiers, operators, or matrix definitions.

The scanner identifies components like: Matrix identifiers (e.g., A, B, C); Assignment operators (=); Matrix values ((1,2), (3,4)); Operators for multiplication (x) and addition (+); Keywords like display. The following token types and their respective regular expressions are defined in the language:

* ID: Matches matrix identifiers, which are single capital letters (e.g., A, B, C).
Regex: [A-Z]

* ASSIGN: Assignment operator (=).
Regex: =

* MATRIX: Matches matrix elements in the format (n,m) where n and m are digits.
Regex: \(\[0-9]+,[0-9]+\)

* OP_MUL: Matrix multiplication operator (x).
Regex: x

* DISPLAY: The display keyword used to output matrix results.
Regex: display

* WHITESPACE: Matches spaces and newlines (ignored for now).
Regex: \s+

Output: A tokens.txt file containing the list of tokens, such as: 
```
<ID, A>
<ASSIGNMENT_OP, =>
<MATRIX, (2,2)>
<MATRIX, (3,4)>
<ID, B>
<ASSIGNMENT_OP, =>
<MATRIX, (5,6)>
<MATRIX, (7,8)>
<ID, C>
<ASSIGNMENT_OP, =>
<ID, A>
<OP_MUL, x>
<ID, B>
<DISPLAY, display>
<ID, C>
<DISPLAY, display>
<ID, A>
<DISPLAY, display>
<ID, B>
<DISPLAY, display>
<ID, B>
```

### 2. Parsing (Syntactic Analysis)
The parser reads the tokens from the scanner and builds an Abstract Syntax Tree (AST), representing the hierarchical structure of the program. It also validates the syntax of the input program.

The parser checks:
 * Whether matrices are correctly defined (e.g., all rows have the same number of elements).
 * Whether operators like x are used with valid operands.
 * Whether keywords like display are followed by valid identifiers. 

Error Handling:
* If any syntax errors are found (e.g., missing assignment operator or invalid characters), the parser stops and reports the errors, such as:
Unexpected token: <ERROR, Unknown character '?'>

Output: generated_ast.json file, containing the AST:
```
{
    "Program": [
        {
            "MatrixAssignment": {
                "ID": {
                    "Value": "A"
                },
                "Matrix": [
                    {
                        "Row": "(2,2)"
                    },
                    {
                        "Row": "(3,4)"
                    }
                ]
            }
        },
        {
            "MatrixAssignment": {
                "ID": {
                    "Value": "B"
                },
                "Matrix": [
                    {
                        "Row": "(5,6)"
                    },
                    {
                        "Row": "(7,8)"
                    }
                ]
            }
        },
        {
            "MatrixMultiplicationAssignment": {
                "ID": {
                    "Value": "C"
                },
                "Multiplication": {
                    "Operand1": "ID (A)",
                    "Operator": "x",
                    "Operand2": "ID (B)"
                }
            }
        },
        {
            "DisplayStatement": {
                "Display": "display",
                "ID": {
                    "Value": "C"
                }
            }
        },
        {
            "DisplayStatement": {
                "Display": "display",
                "ID": {
                    "Value": "A"
                }
            }
        },
        {
            "DisplayStatement": {
                "Display": "display",
                "ID": {
                    "Value": "B"
                }
            }
        },
        {
            "DisplayStatement": {
                "Display": "display",
                "ID": {
                    "Value": "B"
                }
            }
        }
    ]
}
```

### 3. Code Generation

The code generator converts the AST into low level C code (target langauge) that performs the specified matrix operations and outputs results as defined in the program.

The Generator:
* Translates matrix definitions into int arrays in C.
* Converts operations like matrix multiplication (x) into nested for loops in C.
* Handles display statements by generating code to print matrices using a helper function.

Optimizations:
* Redundant or dead code (e.g., multiple display statements for the same matrix) is removed.
* Simplifies operations where possible (e.g., multiplication with a zero matrix).

Output: An output_code.c file, for example: 
```
#include <stdio.h>

void printMatrix(int rows, int cols, int matrix[rows][cols]) {
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            printf("%d ", matrix[i][j]);
        }
        printf("\n");
    }
}

int main() {
    int A[2][2] = {{2,2}, {3,4}};
    int B[2][2] = {{5,6}, {7,8}};
    int C[2][2] = {{0}};
    for (int i = 0; i < 2; i++) {
        for (int j = 0; j < 2; j++) {
            for (int k = 0; k < 2; k++) {
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }
    printf("Matrix C:\n");
    printMatrix(2, 2, C);
    return 0;
}

```

### 4. Code Compliation & Execution by Compiler Architecture 
The compiled executable is run to produce the final output of the program.

The executable performs the operations specified in the input program (e.g., matrix multiplication, addition) and displays the results.

Output:

The results of the matrix operations are printed to the console. For example:
```
Matrix C:
26 32 
47 58 

```


## Video Demo
https://drive.google.com/drive/folders/1__LbbpuB-oCH9xWtK1Mj0aJcUBXXx9Kj?usp=sharing

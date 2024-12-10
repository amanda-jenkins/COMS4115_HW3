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
    * chmod +x run_complier.sh
    * run_compiler.sh to process the input file.
        *  For example, ./run_compiler.sh example.txt
3. Output - the script will go through the following steps:

Scanning: Tokenizes the input file into recognizable components.
Parsing: Generates an Abstract Syntax Tree (AST) or reports syntax errors.
Code Generation: Creates the corresponding C code if no errors are found.
Compilation: Compiles the generated C code into an executable file.
Execution: Runs the compiled program to produce the final output.

## Detailed description of each step


## Video Demo
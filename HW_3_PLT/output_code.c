#include <stdio.h>

// Function to print a matrix
void printMatrix(int rows, int cols, int matrix[rows][cols]) {
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            printf("%d ", matrix[i][j]);
        }
        printf("\n");
    }
}

int main() {
    int A[2][2] = {
    {9,2},
    {3,4}
};
    int B[2][2] = {
    {5,6},
    {10,8}
};
    int C[2][2] = {0};
    for (int i = 0; i < 2; i++) {
        for (int j = 0; j < 2; j++) {
            for (int k = 0; k < 2; k++) {
                C[i][j] += (A)[i][k] * (B)[k][j];
            }
        }
    }
    printf("Matrix C:\n");
    printMatrix(2, 2, C);
    return 0;
}
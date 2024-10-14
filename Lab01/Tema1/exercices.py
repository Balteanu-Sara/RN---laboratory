import pathlib
import math
import copy

###ex1
def parsing(equation : str) -> tuple[list[float], float]:
    equation=equation.replace(" ", "");
    coefficients=[]
    coef=''
    i=0

    while i<len(equation):
        character=equation[i]

        if character=='x' or character=='y' or character=='z':
            if coef=='' or coef=='+': coefficients.append(1.0)
            elif coef=='-' : coefficients.append(-1.0)
            else:  coefficients.append(float(coef))
            coef=''
        elif character == '=' :
            constant=float(equation[i+1:])
            break
        else: coef=coef+character

        i=i+1

    return coefficients, constant

def load_system(path: pathlib.Path) -> tuple[list[list[float]], list[float]]:
    A=[]
    B=[]

    with path.open() as file:
        for line in file:
            coefficients, constant = parsing(line)
            A.append(coefficients)
            B.append(constant)
    return A, B

A, B = load_system(pathlib.Path("system.txt"))
print(f"A={A} B={B}")


###ex2
def determinant(matrix: list[list[float]]) -> float:
    elem1=matrix[0][0]*(matrix[1][1]*matrix[2][2] - matrix[1][2]*matrix[2][1])
    elem2=matrix[0][1]*(matrix[1][0]*matrix[2][2] - matrix[1][2]*matrix[2][0])
    elem3=matrix[0][2]*(matrix[1][0]*matrix[2][1] - matrix[1][1]*matrix[2][0])
    return elem1-elem2+elem3

def trace(matrix: list[list[float]]) -> float:
    return matrix[0][0]+matrix[1][1]+matrix[2][2]

def norm(vector: list[float]) -> float:
    return math.sqrt(vector[0]*vector[0] + vector[1]*vector[1] + vector[2]*vector[2])

def transpose(matrix: list[list[float]]) -> list[list[float]]:
    T=[[0,0,0], [0,0,0], [0,0,0]]

    T[0]=[matrix[0][0], matrix[1][0], matrix[2][0]]
    T[1]=[matrix[0][1], matrix[1][1], matrix[2][1]]
    T[2]=[matrix[0][2], matrix[1][2], matrix[2][2]]
    return T

def multiply(matrix: list[list[float]], vector: list[float]) -> list[float]:
    M=[]

    prod1=matrix[0][0]*vector[0] + matrix[0][1]*vector[1] + matrix[0][2]*vector[2]
    prod2=matrix[1][0]*vector[0] + matrix[1][1]*vector[1] + matrix[1][2]*vector[2]
    prod3=matrix[2][0]*vector[0] + matrix[2][1]*vector[1] + matrix[2][2]*vector[2]

    M.append(prod1)
    M.append(prod2)
    M.append(prod3)
    return M

print(f"determinant(A)={determinant(A)}")
print(f"trace(A)={trace(A)}")
print(f"norm(B)={norm(B)}")
print(f"transpose(A)={transpose(A)}")
print(f"multiply(A,B)={multiply(A,B)}")


###ex3
def solve_cramer(matrix: list[list[float]], vector: list[float]) -> list[float]:
    S =[]
    detA=determinant(matrix)
    if detA == 0:
        raise ValueError("The system doesn't have a unique solution.")

    for i in range(len(vector)):
        temp=copy.deepcopy(matrix)

        for j in range(3):
            temp[j][i] = vector[j]

        tempDet=determinant(temp)
        #print(f"{tempDet}")
        S.append(tempDet/detA)

    return S

solution=solve_cramer(A,B)
print(f"Solution of the system is x={solution[0]}, y={solution[1]} and z={solution[2]}.")


###ex4
def minor(matrix: list[list[float]], i: int, j: int) -> list[list[float]]:
    min=[]
    for r in range(len(matrix)):
        row=[]
        for c in range(len(matrix[r])):
            if r!=i and c!=j: row.append(matrix[r][c])
        min.append(row)
    return min

def cofactor(matrix: list[list[float]]) -> list[list[float]]:
    cof=[]
    for i in range(len(matrix)):
        row=[]
        for j in range(len(matrix[i])):
            min=minor(matrix,i,j)
            if (i+j) % 2 == 0:
                element = min[0][0]*min[1][1]-min[0][1]*min[1][0]
            else: element = -min[0][0]*min[1][1]+min[0][1]*min[1][0]
            row.append(element)
        cof.append(row)

    return cof

def adjoint(matrix: list[list[float]]) -> list[list[float]]:
    cof=cofactor(matrix)
    return transpose(cof)

def solve(matrix: list[list[float]], vector: list[float]) -> list[float]:
    S=[]

    detA=determinant(matrix)
    matrixInv=adjoint(matrix)

    for i in range(len(matrixInv)):
        for j in range(len(matrixInv[i])):
            matrixInv[i][j] = matrixInv[i][j] * (1/detA)

    S=multiply(matrixInv, vector)

    return S

solution=solve_cramer(A,B)
print(f"Solution of the system is x={solution[0]}, y={solution[1]} and z={solution[2]}.")
def display_board(matrix):
    '''Permet d'afficher la matrice avec le champ de vue'''
    for i in matrix:
        for j in i:
            if j == 1:
                print("\033[31m1\033[0m", "", end="")
            else:
                print("\033[30m0\033[0m", "", end="")
        print()


def line_replace(column, line, director_coefficient, matrix):
    '''Permet de tracer les lignes de vues avec l'algo de Bresenham'''
    if matrix == 0:
        matrix = [[0] * line for i in range(column)]
    if director_coefficient < 0 and director_coefficient > (-1):
        n = 0
        y = 0
        for j in range(min(line, column)):
            y = y + director_coefficient
            matrix[n][j] = 1
            if y <= (-1):
                n = n + 1
                y = y + 1
        return matrix
    if director_coefficient >= 0 and director_coefficient < 1:
        n = column - 1
        y = 0
        for j in range(min(line, column)):
            y = y + director_coefficient
            matrix[n][j] = 1
            if y >= 1:
                n = n - 1
                y = y - 1
        return matrix
    if director_coefficient < (-1):
        n = 0
        y = 0
        for j in range(min(line, column)):
            y = y + (1 / director_coefficient)
            matrix[j][n] = 1
            if y <= (-1):
                n = n + 1
                y = y + 1
        return matrix
    if director_coefficient > 1:
        n = 0
        y = 0
        for j in range(min(line, column)):
            y = y + (1 / director_coefficient)
            matrix[column - 1 - j][n] = 1
            if y >= 1:
                n = n + 1
                y = y - 1
        return matrix


# POUR TESTER LE PROGRAMME :

M1 = line_replace(40, 50, -0.2, 0)
M2 = line_replace(40, 50, -4, M1)
M3 = line_replace(40, 50, -1.2, M2)
M4 = line_replace(40, 50, -0.62, M3)
print(display_board(M4))

# Marche pour des matrices carrées, on ne peut pas déplacer la position du personnage

from math import floor, sqrt, tan


# Création et affichage de matrices de terrain

def create_matrix(column, line):
    '''Permet de créer une matrice de taille column x ligne
        Retourne une liste de listes'''
    matrix = [[0] * line for i in range(column)]
    return matrix


def display_board(matrix):
    '''Permet d'afficher la matrice avec le champ de vue'''
    for i in matrix:
        for j in i:
            if j == "m":
                print("\033[37m#\033[0m", "", end="")
            elif j == "g":
                print("\033[37m/\033[0m", "", end="")
            elif j == '@':
                print("\033[32m@\033[0m", "", end="")
            elif j == 0:
                print("\033[30m0\033[0m", "", end="")
            else:
                print("\033[31m*\033[0m", "", end="")
        print()


def put_wall(direction, length, begin_x, begin_y, wall_type, matrix):
    """Permet de placer un mur sur la matrice de terrain
        Retourne la matrice modifiée
    l pour left, r pour right, t pour top, b pour bottom, glass pour une vitre, wall pour un mur opaque"""
    if wall_type == "glass":
        if direction == "r":
            for i in range(length):
                matrix[begin_y][begin_x + i] = "g"
        elif direction == "l":
            for i in range(length):
                matrix[begin_y][begin_x - i] = "g"
        elif direction == "t":
            for i in range(length):
                matrix[begin_y - i][begin_x] = "g"
        elif direction == "b":
            for i in range(length):
                matrix[begin_y + i][begin_x] = "g"
    if wall_type == "wall":
        if direction == "r":
            for i in range(length):
                matrix[begin_y][begin_x + i] = "m"
        elif direction == "l":
            for i in range(length):
                matrix[begin_y][begin_x - i] = "m"
        elif direction == "t":
            for i in range(length):
                matrix[begin_y - i][begin_x] = "m"
        elif direction == "b":
            for i in range(length):
                matrix[begin_y + i][begin_x] = "m"


# Tracer les lignes de vues avec l'algorithme de Bresenham
def line_replace1(director_coefficient, matrix, position_character_x, position_character_y):
    '''Traite l'octant 1 et 5
    Retourne la matrice modifiée'''
    column = len(matrix)
    line = len(matrix[1])
    position_x = position_character_x
    position_y = position_character_y
    distance_y = 0
    distance_y_2 = 0
    distance_x = 0
    distance_x_2 = 0
    limit = floor(2 * min(column, line) / 5)
    n = position_y
    n_2 = n
    y = 0
    y_2 = y
    for j in range(line - position_x):
        y += director_coefficient
        if matrix[n][j + position_x - 1] != "m" and matrix[n][j + position_x - 1] != "g":
            matrix[n][j + position_x - 1] = limit + 1 - j
        if matrix[n][j + position_x - 1] != "m":
            distance_x += 1
            if sqrt((distance_x ** 2) + (distance_y ** 2)) >= limit:
                break
            if y <= -1:
                n += 1
                if matrix[n][j + position_x - 1] != "m" and matrix[n][j + position_x - 1] != "g":
                    matrix[n][j + position_x - 1] = limit + 1 - j
                if matrix[n][j + position_x - 1] != "m":
                    y += + 1
                    distance_y += 1
                    if sqrt((distance_x ** 2) + (distance_y ** 2)) >= limit:
                        break
                else:
                    break
        else:
            break
    for j in range(line - position_x):
        y_2 -= director_coefficient
        if matrix[column - n_2][line - (j + position_x - 1)] != "m" and matrix[column - n_2][
            line - (j + position_x - 1)] != "g":
            matrix[column - n_2][line - (j + position_x - 1)] = limit + 1 - j
        if matrix[column - n_2][line - (j + position_x - 1)] != "m":
            distance_x_2 += 1
            if sqrt((distance_x_2 ** 2) + (distance_y_2 ** 2)) >= limit:
                break
            if y_2 >= 1:
                n_2 += 1
                if matrix[column - n_2][line - (j + position_x - 1)] != "m" and matrix[column - n_2][
                    line - (j + position_x - 1)] != "g":
                    matrix[column - n_2][line - (j + position_x - 1)] = limit + 1 - j
                if matrix[column - n_2][line - (j + position_x - 1)] != "m":
                    y_2 -= 1
                    distance_y_2 += 1
                    if sqrt((distance_x_2 ** 2) + (distance_y_2 ** 2)) >= limit:
                        break
                else:
                    break
        else:
            break
    return matrix


def line_replace2(director_coefficient, matrix, position_character_x, position_character_y):
    '''Traite l'octant 2 et 6
        Retourne la matrice modifiée'''
    column = len(matrix)
    line = len(matrix[1])
    position_x = position_character_x
    position_y = position_character_y
    distance_y = 0
    distance_y_2 = 0
    distance_x = 0
    distance_x_2 = 0
    limit = floor(2 * min(column, line) / 5)

    n = column - position_y
    n_2 = n
    y = 0
    y_2 = y
    for j in range(line - position_x):
        y += director_coefficient
        if matrix[n][j + position_x - 1] != "m" and matrix[n][j + position_x - 1] != "g":
            matrix[n][j + position_x - 1] = limit + 1 - j
        if matrix[n][j + position_x - 1] != "m":
            distance_x += 1
            if sqrt((distance_x ** 2) + (distance_y ** 2)) >= limit:
                break
            if y >= 1:
                n -= 1
                if matrix[n][j + position_x - 1] != "m" and matrix[n][j + position_x - 1] != "g":
                    matrix[n][j + position_x - 1] = limit + 1 - j
                if matrix[n][j + position_x - 1] != "m":
                    y -= 1
                    distance_y += 1
                    if sqrt((distance_x ** 2) + (distance_y ** 2)) >= limit:
                        break
                else:
                    break
        else:
            break
    for j in range(line - position_x):
        y_2 -= director_coefficient
        if matrix[column - n_2][line - (j + position_x - 1)] != "m" and matrix[column - n_2][
            line - (j + position_x - 1)] != "g":
            matrix[column - n_2][line - (j + position_x - 1)] = limit + 1 - j
        if matrix[column - n_2][line - (j + position_x - 1)] != "m":
            distance_x_2 += 1
            if sqrt((distance_x_2 ** 2) + (distance_y_2 ** 2)) >= limit:
                break
            if y_2 <= -1:
                n_2 -= 1
                if matrix[column - n_2][line - (j + position_x - 1)] != "m" and matrix[column - n_2][
                    line - (j + position_x - 1)] != "g":
                    matrix[column - n_2][line - (j + position_x - 1)] = limit + 1 - j
                if matrix[column - n_2][line - (j + position_x - 1)] != 2:
                    y_2 += 1
                    distance_y_2 += 1
                    if sqrt((distance_x_2 ** 2) + (distance_y_2 ** 2)) >= limit:
                        break
                else:
                    break
        else:
            break
    return matrix


def line_replace3(director_coefficient, matrix, position_character_x, position_character_y):
    '''Traite l'octant 3 et 7
        Retourne la matrice modifiée'''
    column = len(matrix)
    line = len(matrix[1])
    position_x = position_character_x
    position_y = position_character_y
    distance_y = 0
    distance_y_2 = 0
    distance_x = 0
    distance_x_2 = 0
    limit = floor(2 * min(column, line) / 5)
    n = position_x
    n_2 = n
    y = 0
    y_2 = y
    for j in range(line - position_x):
        y += 1 / director_coefficient
        if matrix[j + position_y - 1][n] != "m" and matrix[j + position_y - 1][n] != "g":
            matrix[j + position_y - 1][n] = limit + 1 - j
        if matrix[j + position_y - 1][n] != "m":
            distance_y += 1
            if sqrt((distance_x ** 2) + (distance_y ** 2)) >= limit:
                break
            if y <= -1:
                n += 1
                if matrix[j + position_y - 1][n] != "m" and matrix[j + position_y - 1][n] != "g":
                    matrix[j + position_y - 1][n] = limit + 1 - j
                if matrix[j + position_y - 1][n] != "m":
                    y += 1
                    distance_x += 1
                    if sqrt((distance_x ** 2) + (distance_y ** 2)) >= limit:
                        break
                else:
                    break
        else:
            break

    for j in range(line - position_x):
        y_2 -= 1 / director_coefficient
        if matrix[line - (j + position_y - 1)][column - n_2] != "m" and matrix[line - (j + position_y - 1)][
            column - n_2] != "g":
            matrix[line - (j + position_y - 1)][column - n_2] = limit + 1 - j
        if matrix[line - (j + position_y - 1)][column - n_2] != "m":
            distance_y_2 += 1
            if sqrt((distance_x_2 ** 2) + (distance_y_2 ** 2)) >= limit:
                break
            if y_2 >= 1:
                n_2 += 1
                if matrix[line - (j + position_y - 1)][column - n_2] != "m" and matrix[line - (j + position_y - 1)][
                    column - n_2] != "g":
                    matrix[line - (j + position_y - 1)][column - n_2] = limit + 1 - j
                if matrix[line - (j + position_y - 1)][column - n_2] != "m":
                    y_2 -= 1
                    distance_x_2 += 1
                    if sqrt((distance_x_2 ** 2) + (distance_y_2 ** 2)) >= limit:
                        break
                else:
                    break
        else:
            break
    return matrix


def line_replace4(director_coefficient, matrix, position_character_x, position_character_y):
    '''Traite l'octant 4 et 8
        Retourne la matrice modifiée'''
    column = len(matrix)
    line = len(matrix[1])
    position_x = position_character_x
    position_y = position_character_y
    distance_y = 0
    distance_y_2 = 0
    distance_x = 0
    distance_x_2 = 0
    limit = floor(2 * min(column, line) / 5)
    n = column - position_x
    n_2 = n
    y = 0
    y_2 = y
    for j in range(line - position_x):
        y += (1 / director_coefficient)
        if matrix[j + position_y - 1][n] != "m" and matrix[j + position_y - 1][n] != "g":
            matrix[j + position_y - 1][n] = limit + 1 - j
        if matrix[j + position_y - 1][n] != "m":
            distance_y += 1
            if sqrt((distance_x ** 2) + (distance_y ** 2)) >= limit:
                break
            if y >= 1:
                n -= 1
                if matrix[j + position_y - 1][n] != "m" and matrix[j + position_y - 1][n] != "g":
                    matrix[j + position_y - 1][n] = limit + 1 - j
                if matrix[j + position_y - 1][n] != "m":
                    y -= 1
                    distance_x += 1
                    if sqrt((distance_x ** 2) + (distance_y ** 2)) >= limit:
                        break
                else:
                    break
        else:
            break
    for j in range(line - position_x):
        y_2 -= 1 / director_coefficient
        if matrix[line - (j + position_y - 1)][column - n_2] != "m" and matrix[line - (j + position_y - 1)][
            column - n_2] != "g":
            matrix[line - (j + position_y - 1)][column - n_2] = limit + 1 - j
        if matrix[line - (j + position_y - 1)][column - n_2] != "m":
            distance_y_2 += 1
            if sqrt((distance_x_2 ** 2) + (distance_y_2 ** 2)) >= limit:
                break
            if y_2 <= -1:
                n_2 -= 1
                if matrix[line - (j + position_y - 1)][column - n_2] != "m" and matrix[line - (j + position_y - 1)][
                    column - n_2] != "g":
                    matrix[line - (j + position_y - 1)][column - n_2] = limit + 1 - j
                if matrix[line - (j + position_y - 1)][column - n_2] != "m":
                    y_2 += 1
                    distance_x_2 += 1
                    if sqrt((distance_x_2 ** 2) + (distance_y_2 ** 2)) >= limit:
                        break
                else:
                    break
        else:
            break
    return matrix


def line_replace5(matrix, position_character_x, position_character_y):
    '''Traite la droite de coeff directeur 1
    Retourne la matrice modifiée'''
    column = len(matrix)
    line = len(matrix[1])
    x = position_character_x
    y = position_character_y
    counter1 = 0
    counter2 = 0
    limit = floor(2 * min(column, line) / 5)
    for i in range(min(x, y)):
        if matrix[y - i][x - i] != "m" and matrix[y - i][x - i] != "g":
            matrix[y - i][x - i] = limit + 1 - i
        if matrix[y - i][x - i] != "m":
            counter1 += 1
            if counter1 >= limit:
                break
        else:
            break
    for i in range(min(x, y)):
        if matrix[y + i][x + i] != "m" and matrix[y + i][x + i] != "g":
            matrix[y + i][x + i] = limit + 1 - i
        if matrix[y + i][x + i] != "m":
            counter2 += 1
            if counter2 >= limit:
                break
        else:
            break
    return matrix


def line_replace6(matrix, position_character_x, position_character_y):
    '''Traite la droite de coefficient directeur -1
    Retourne la matrice modifiée'''
    column = len(matrix)
    line = len(matrix[1])
    x = position_character_x
    y = position_character_y
    counter1 = 0
    counter2 = 0
    limit = floor(2 * min(column, line) / 5)
    for i in range(min(x, y)):
        if matrix[y - i][x + i] != "m" and matrix[y - i][x + i] != "g":
            matrix[y - i][x + i] = limit + 1 - i
        if matrix[y - i][x + i] != "m":
            counter1 += 1
            if counter1 >= limit:
                break
        else:
            break
    for i in range(min(x, y)):
        if matrix[y + i][x - i] != "m" and matrix[y + i][x - i] != "g":
            matrix[y + i][x - i] = limit + 1 - i
        if matrix[y + i][x - i] != "m":
            counter2 += 1
            if counter2 >= limit:
                break
        else:
            break
    return matrix


def final_replace(director_coefficient, matrix, position_character_x, position_character_y):
    '''Permet de construire le champ de vision'''
    if -1 < director_coefficient < 0:
        line_replace1(director_coefficient, matrix, position_character_x, position_character_y)
    elif 0 <= director_coefficient < 1:
        line_replace2(director_coefficient, matrix, position_character_x, position_character_y)
    elif director_coefficient < -1:
        line_replace3(director_coefficient, matrix, position_character_x, position_character_y)
    elif director_coefficient > 1:
        line_replace4(director_coefficient, matrix, position_character_x, position_character_y)
    elif director_coefficient == -1:
        line_replace5(matrix, position_character_x, position_character_y)
    elif director_coefficient == 1:
        line_replace6(matrix, position_character_x, position_character_y)
    return matrix


def line_number(matrix):
    '''Permet de déterminer un nombre approximatif de droites permettant de recouvrir le champs de vision'''
    column = len(matrix)
    line = len(matrix[1])
    return floor(3 * min(column, line) / 2)


def field_of_view(matrix, line_number, position_character_x, position_character_y):
    '''Permet de construire le champ de vision'''
    for i in range(line_number):
        matrix = final_replace(tan(0.01745 * (90 - i * (180 / line_number))), matrix, position_character_x,
                               position_character_y)
    matrix[position_character_y][position_character_x] = "@"
    return matrix


# POUR TESTER LE PROGRAMME :


columns = 30
lines = 30
position_characters_x = floor(lines / 2)
position_characters_y = floor(columns / 2)
board = create_matrix(columns, lines)
put_wall("r", 10, 6, 10, "wall", board)
put_wall("b", 9, 20, 3, "wall", board)
put_wall("b", 4, 20, 12, "glass", board)
put_wall("b", 4, 20, 16, "wall", board)
board1 = field_of_view(board, line_number(board), position_characters_x, position_characters_y)
display_board(board1)

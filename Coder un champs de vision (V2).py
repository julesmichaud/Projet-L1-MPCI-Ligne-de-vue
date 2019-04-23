from math import floor, tan
from random import randrange


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
            if j == 1:
                print("\033[31m*\033[0m", "", end="")
            elif j == '@':
                print("\033[32m@\033[0m", "", end="")
            else:
                print("\033[30m0\033[0m", "", end="")
        print()



# Pour tracer la ligne de vue

def line_replace(director_coefficient, matrix):
    '''Permet de tracer les lignes de vues avec l'algo de Bresenham'''
    column = len(matrix)
    line = len(matrix[1])
    position_x = floor(line / 2)
    position_y = floor(column / 2)
    counter = 0
    counter_2 = 0
    limit = floor(2 * min(column, line) / 5)

    if director_coefficient < 0 and director_coefficient > (-1):
        n = position_y
        n_2 = n
        y = 0
        y_2 = y
        for j in range(line - position_x):
            y = y + director_coefficient
            matrix[n][j + position_x - 1] = 1
            counter += 1
            if counter >= limit:
                break
            if y <= (-1):
                n = n + 1
                y = y + 1
                counter += 1
                if counter >= limit:
                    break
        for j in range(line - position_x):
            y_2 = y_2 - director_coefficient
            matrix[column - n_2][line - (j + position_x - 1)] = 1
            counter_2 += 1
            if counter_2 >= limit:
                break
            if y_2 >= (1):
                n_2 = n_2 + 1
                y_2 = y_2 - 1
                counter_2 += 1
                if counter_2 >= limit:
                    break

    if director_coefficient >= 0 and director_coefficient < 1:
        n = column - position_y
        n_2 = n
        y = 0
        y_2 = y
        for j in range(line - position_x):
            y = y + director_coefficient
            matrix[n][j + position_x - 1] = 1
            counter += 1
            if counter >= limit:
                break
            if y >= (1):
                n = n - 1
                y = y - 1
                counter += 1
                if counter >= limit:
                    break
        for j in range(line - position_x):
            y_2 = y_2 - director_coefficient
            matrix[column - n_2][line - (j + position_x - 1)] = 1
            counter_2 += 1
            if counter_2 >= limit:
                break
            if y_2 <= (-1):
                n_2 = n_2 - 1
                y_2 = y_2 + 1
                counter_2 += 1
                if counter_2 >= limit:
                    break

    if director_coefficient < (-1):
        n = position_x
        n_2 = n
        y = 0
        y_2 = y
        for j in range(line - position_x):
            y = y + (1 / director_coefficient)
            matrix[j + position_y - 1][n] = 1
            counter += 1
            if counter >= limit:
                break
            if y <= (-1):
                n = n + 1
                y = y + 1
                counter += 1
                if counter >= limit:
                    break
        for j in range(line - position_x):
            y_2 = y_2 - (1 / director_coefficient)
            matrix[line - (j + position_y - 1)][column - n_2] = 1
            counter_2 += 1
            if counter_2 >= limit:
                break
            if y_2 >= (1):
                n_2 = n_2 + 1
                y_2 = y_2 - 1
                counter_2 += 1
                if counter_2 >= limit:
                    break

    if director_coefficient > 1:
        n = column - position_x
        n_2 = n
        y = 0
        y_2 = y
        for j in range(line - position_x):
            y = y + (1 / director_coefficient)
            matrix[j + position_y - 1][n] = 1
            counter += 1
            if counter >= limit:
                break
            if y >= 1:
                n = n - 1
                y = y - 1
                counter += 1
                if counter >= limit:
                    break
        for j in range(line - position_x):
            y_2 = y_2 - (1 / director_coefficient)
            matrix[line - (j + position_y - 1)][column - n_2] = 1
            counter_2 += 1
            if counter_2 >= limit:
                break
            if y_2 <= (-1):
                n_2 = n_2 - 1
                y_2 = y_2 + 1
                counter_2 += 1
                if counter_2 >= limit:
                    break

    if director_coefficient == -1:
        y = position_y
        x = position_x
        for i in range(min(x, y)):
            matrix[y - i][x - i] = 1
            counter += 1
            if counter >= limit:
                break
        for i in range(min(x, y)):
            matrix[y + i][x + i] = 1
            counter_2 += 1
            if counter_2 >= limit:
                break

    if director_coefficient == 1:
        y = position_y
        x = position_x
        for i in range(min(x, y)):
            matrix[y - i][x + i] = 1
            counter += 1
            if counter >= limit:
                break
        for i in range(min(x, y)):
            matrix[y + i][x - i] = 1
            counter_2 += 1
            if counter_2 >= limit:
                break

    matrix[position_y][position_x] = '@'
    return matrix


def field_of_view(matrix, line_number):
    '''Permet de construire le champ de vision'''
    for i in range(line_number):
        matrix = line_replace(tan(0.01745 * (90 - i * (180 / line_number))), matrix)
    return matrix


# POUR TESTER LE PROGRAMME :

column = 50
line = 50
line_number = 75
M = create_matrix(column, line)
L = field_of_view(M, line_number)
display_board(L)

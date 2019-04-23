#Fonctionne pour tout type de matrices, déplacement du personnage possible

from PIL import Image, ImageEnhance
from math import sqrt, exp


#Création et affichage de matrices de terrain/ images

img = Image.open("sprites_proj.png")  # Déplacer l'image en question dans le dossier avec l'algorithme
print(img)
finish = Image.open("Imagevide.png")  # Pareil


def create_matrix(column, line):
    '''Permet de créer une matrice de taille column x ligne
    Retourne une liste de listes'''
    lst = [["i"] * line for i in range(column)]
    return lst


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
            elif j == "i":
                print("\033[30m0\033[0m", "", end="")
            else:
                print("\033[31m*\033[0m", "", end="")
        print()


def display_image(lst):
    '''Permet d'afficher une image avec le module PIL'''
    glass = img.crop((31, 36, 45, 50))
    invisible = img.crop((45, 36, 59, 50))
    wall = img.crop((31, 22, 45, 36))
    visible = img.crop((31, 50, 45, 64))
    character = img.crop((33, 2, 47, 16))
    # Création d'un dictionnaire pour simplifier le programme
    img_table = {"m": wall, "g" : glass, "@" : character, "i" : invisible}
    for i, val in enumerate(lst):
        for j, val2 in enumerate(val):
            if isinstance(val2, float):
                # Vérifie si val2 est un flottant car dans ce cas là on est dans le visible
                # Change ensuite la luminosité du visible
                tile = visible
                # ImageEnhance.Brightness(tile) associe la luminosité à tile (l'image visible)
                enhancer = ImageEnhance.Brightness(tile)
                # comme val2 prend différentes valeurs (un coeff spécifique, voir ligne_of_sight) la luminosité
                # va être modifier au fur et à mesure.
                tile = enhancer.enhance(val2)
            else:
                # renvoie la valeur pour la clé donnée, si la clé n'existe pas
                # renvoie visible
                tile = img_table.get(val2, visible)
            finish.paste(tile, (14 * j, 14 * i, 14 * j + 14, 14 * i + 14))
    finish.show()


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
    return matrix


#Tracer les lignes de vues avec l'algorithme de Bresenham

def line_first_octant(start, end):
    """calcul les pixels par lesquels la droite reliant start: (x1, x2) et end: (y1, y2) passe
    On considère que le coefficient directeur de la droite est compris entre 0 et 1, que x1 < x2 et y1 < y2
    Retourne une liste de coordonnées de pixels
    >>> points1 = line_first_octant((0, 0), (15, 20))
    >>> points2 = line_first_octant((15, 20), (0, 0))
    >>> assert (set(points1) == set(points2)"""

    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1
    points = list()
    y = y1
    e = dx
    for x in range(x1, x2 + 1):
        points.append((x, y))
        e -= 2 * dy
        if e < 0:
            e += 2 * dx
            y += 1
    return points


def line_of_sight(start, end, board, limit):
    """calcul les pixels par lesquel la droite reliant start: (x1, x2) et end: (y1, y2) passe,
    Pour toute valeur de coefficient directeur et pour tous points start et end
    Retourne une liste de coordonnées de pixels
    >>> points1 = line_of_sight((0, 0), (5, 2))
    >>> points2 = line_of_sight((5, 2), (0, 0))
    >>> assert (set(points1) == set(points2)"""
    #Dans ce programme, on parle d'octants, on prendra pour octant1 les droites de coefficient directeur compris entre
    #O et 1 et on tournera ensuite dans le sens trigonométrique pour les numéro des autres octants.

    # Conditions initiales
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1

    # Permet de traiter les droites dans les octants 2, 3, 6 et 7
    is_steep = abs(dy) > abs(dx)

    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    # Pour traiter les droites dans les octants 3, 4, 5 et 6
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True

    # On recalcule les variations des coordonnées
    dx = x2 - x1
    dy = y2 - y1

    # On calcule l'erreur commise avec le compteur
    error = dx
    ystep = 1 if y1 < y2 else -1

    # On trace la ligne de vue sur le modèle de la fonction line_first_octant
    y = y1
    points = []
    for x in range(x1, x2 + 1):
        coord = (y, x) if is_steep else (x, y)
        points.append(coord)
        error -= 2 * abs(dy)
        if error < 0:
            y += ystep
            error += 2 * dx

    # On met les coordonnées dans l'ordre (en partant de start) si on se trouvait dans les octants 3, 4, 5 ou 6
    if swapped:
        points.reverse()

    # glass permet de compter le nombre de vitre pour ensuite diminuer la luminosité selon le nombre de vitre rencontrées
    points2 = []
    glass = 0
    u, v = start
    for k, p in enumerate(points):
        i, j = p
        if sqrt((i - u) ** 2 + (j - v) ** 2) < limit:
            # On arrête la vue si on rencontre un mur
            if board[j][i] == "m":
                return points2
            # On n'ajoute pas le point de ligne de vue si on se trouve sur une vitre
            # On ajoute 1 à glass à chaque vitre rencontrée pour ensuite renvoyer la position + le brouillard associée,
            # selon le nombre de vitre rencontrées
            elif board[j][i] == "g":
                glass += 1
            else:
                fog = compute_fog(expfog, i, j)
                fog -= glass * 0.3
                points2.append((p, fog))
    return points2


def champ_de_vision(start, board, limit):
    '''Permet de tracer toutes les lignes de vue qui compose le champ de vision
    Retourne une liste de liste de toutes les droites avec les points vus'''
    res = list()
    #On trace une droite depuis la position du personnage vers chaque point des bords de la matrice
    for i in range(len(board[0])):
        res.append(line_of_sight(start, (i, 0), board, limit))
        res.append(line_of_sight(start, (i, len(board) - 1), board, limit))
    for j in range(len(board)):
        res.append(line_of_sight(start, (0, j), board, limit))
        res.append(line_of_sight(start, (len(board[0]) - 1, j), board, limit))
    return res


#Superposer la matrice de terrain et les lignes de vues

def superpose(board, points):
    '''Permet de superposer sur une matrice tous les points vus d'une droite'''
    for (x, fog) in points:
        i, j = x
        # Idem que pour la fonction précédente
        board[j][i] = fog
    return board


def superpose_champ_de_vison(board, points):
    '''Permet de superposer sur une matrice tous les points vus d'un champ de vision'''
    for x in points:
        for (y, fog) in x:
            i, j = y
            # on remplace par le coefficient du brouillard
            board[j][i] = fog
    return board


#Traitement de la luminosité


def linfog(d):
    """donne l'équation linéaire pour permettre de diminuer la luminosité au fur et à mesure,
    et donne un coefficient pour chaque pixel"""
    fog = 1. - (d / min(line, column))
    return 0 if fog < 0 else fog


def expfog(d):
    """exactement comme linfog mais sous forme d'exponentielle"""
    fog = exp(-2*d / min(line, column))
    return 0 if fog < 0 else fog


def compute_fog(f, i, j):
    """Permet de donner la distance depuis le personnage de chaque pixel,
    pour ensuite lui associer la fonction expfog ou linfog"""
    dx,dy = j-p , i-h
    d = sqrt(dx*dx + dy*dy)
    return f(d)



#Un exemple de commandes permettant d'utiliser une grande partie des fonctions précédentes
line = 30
column = 30
limite = int(2 * min(column, line) / 5)
start = (int(column / 2), int(line / 2 ))
h, p = start
M = create_matrix(line, column)
put_wall("r", 18, 0, 11, "wall", M)
put_wall("r", 3, 7, 11, "glass", M)
put_wall("r", 23, 0, 18, "wall", M)
put_wall("t", 3, 23, 18, "wall", M)
put_wall("t", 3, 23, 15, "glass", M)
put_wall("t", 2, 23, 12, "wall", M)
put_wall("r", 7, 23, 10, "wall", M)
put_wall("t", 12, 17, 11, "wall", M)
put_wall("t", 4, 17, 9, "glass", M )
put_wall("r", 3, 12, 18, "glass", M)
L = champ_de_vision(start, M, limite)
superpose_champ_de_vison(M, L)
M[p][h] = "@"
display_image(M)
display_board(M)

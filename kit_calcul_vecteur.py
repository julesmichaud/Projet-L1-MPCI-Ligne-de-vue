
def calcule_vecteur(point1, point2):
    """prend deux listes  avec les coordonnées des points et retourne les coordonnées du vecteur"""
    x_vecteur = point2[0] - point1[0]
    y_vecteur = point2[1] - point1[1]
    return [x_vecteur, y_vecteur]


def calcule_produit_scalaire(vecteur1, vecteur2):
    return vecteur1[0] * vecteur2[0] + vecteur1[1] * vecteur2[1]


def calcule_vecteurs_triangle(triangle):
    """crée un dictionnaire qui associe à chaque point du triangle (clef) le vecteur le reliant au point suivant (valeur)"""
    # pour avoir un point et le vecteur associé pour pouvoir calculer l'intersection
    dico_point_vecteur = dict()
    vecteur1 = calcule_vecteur(triangle[0], triangle[1])
    dico_point_vecteur[triangle[0]] = vecteur1
    vecteur2 = calcule_vecteur(triangle[1], triangle[2])
    dico_point_vecteur[triangle[1]] = vecteur2
    vecteur3 = calcule_vecteur(triangle[2], triangle[0])
    dico_point_vecteur[triangle[2]] = vecteur3
    return dico_point_vecteur


def calcule_ensemble_des_cotes_des_triangles(liste_de_triangle):
    """calcule les vecteurs de côtés de tous les triangles d'une liste et retourne un dico avec un point comme clef et le vecteur comme valeur"""
    dictionnaire_des_vecteurs = dict()
    for i in liste_de_triangle:
        dictionnaire_des_vecteurs_intermediaire = calcule_vecteurs_triangle(i)
        dictionnaire_des_vecteurs.update(dictionnaire_des_vecteurs_intermediaire)
    return dictionnaire_des_vecteurs


# fonctions inutiles


def calcule_normale(liste):  # pour un vecteur orienté vers le haut la normale est orientée vers la gauche
    """prend une  liste des coordonnées d'un vecteur et retourne sa normale"""
    x_normale = -liste[1]
    y_normale = liste[0]
    return [x_normale, y_normale]


def calcule_normales_triangle(liste_de_liste):  # les triangles doivent être rentrés dans le sens horaire pour avoir les normales à l'exterieur
    """prend un triangle et retourne les coordonnées de ses normales dans l'ordre des points"""
    normale_1 = calcule_normale(calcule_vecteur(liste_de_liste[0], liste_de_liste[1]))
    normale_2 = calcule_normale(calcule_vecteur(liste_de_liste[1], liste_de_liste[2]))
    normale_3 = calcule_normale(calcule_vecteur(liste_de_liste[2], liste_de_liste[0]))
    return [normale_1, normale_2, normale_3]

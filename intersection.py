from kit_calcul_vecteur import calcule_normales_triangle
from kit_calcul_vecteur import calcule_normale
from kit_calcul_vecteur import calcule_vecteurs_triangle
from kit_calcul_vecteur import calcule_vecteur
from kit_calcul_vecteur import calcule_ensemble_des_cotes_des_triangles
from kit_calcul_vecteur import calcule_produit_scalaire


def verifie_itersection(vecteur_segment_centre, placement_personnage, vecteur_directeur_segment, point_segment):
    """calcule les T pour que les segment s'intersectent, retourne True si les segments ne se coupent pas"""
    ray_x = vecteur_segment_centre[0]
    ray_y = vecteur_segment_centre[1]
    segm_x = vecteur_directeur_segment[0]
    segm_y = vecteur_directeur_segment[1]
    scalaire_carré = (calcule_produit_scalaire(vecteur_segment_centre, vecteur_directeur_segment)) ** 2
    norme_carre_vecteur_segment_centre = ray_x ** 2 + ray_y ** 2
    norme_carre_vecteur_directeur_segment = segm_x ** 2 + segm_y ** 2
    if scalaire_carré == norme_carre_vecteur_directeur_segment * norme_carre_vecteur_segment_centre: 
        # vérifie si les deux vecteurs sont colinéaires ou non
        return True
    else:
        # si il ne sont pas colinéaires, on calcule les T1 et T2 correspondants
        
        #calcul de T2
        
        numéra = ray_x * (point_segment[1] - placement_personnage[1]) - ray_y * (
                    point_segment[0] - placement_personnage[0])
        dénomin = ray_y * segm_x - segm_y * ray_x
        T2 = numéra / dénomin
        
        #calcul de T1 en différenciant les cas si les vecteurs ont des coordonnées égales à 0
        
        if ray_x != 0 and ray_y == 0 or ray_x != 0 and ray_y != 0:
            T1 = (segm_x * T2 + point_segment[0] - placement_personnage[0]) / ray_x

        if ray_x == 0 and ray_y != 0:
            T1 = (segm_y * T2 - placement_personnage[1] + point_segment[1])

        if ray_x == 0 and ray_y == 0:
            return True
        
        #vérification que l'intersction est bien sur le côté du triangle et du "bon côté" du personnage
        
        if T1 >= 0 and 0 < T2 < 1:
            return False

        return True


def visible(dictionnaire_de_vecteur, emplacement_personnage, point_a_verifier):
    # il faut appliquer les fonction calcule_ensemble_des_côtés_des_triangles d'abord pour avoir le dictionnaire
    
    vecteur_segment_centre = calcule_vecteur(emplacement_personnage, point_a_verifier)
    
    # vérifie s'il existe une intersection entre le rayon et un triangle, si c'est le cas, renvoie False
    
    for i in dictionnaire_de_vecteur:
        print(verifie_itersection(vecteur_segment_centre, emplacement_personnage, dictionnaire_de_vecteur[i], i))
        if not(verifie_itersection(vecteur_segment_centre, emplacement_personnage, dictionnaire_de_vecteur[i], i)):
            return False
    return True





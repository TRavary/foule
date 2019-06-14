import math
from graphics import *
class PointFloat:
    def __init__(self,x = 0 ,y = 0):
        self.x = float(x)
        self.y = float(y)

    def __repr__(self):
        return "("+str(self.x)+","+str(self.y)+")"


def distance(a,b):
    return math.sqrt((b.x-a.x)**2+(b.y-a.y)**2)


def generer_segment(debut,fin,pas):
    segment = []
    d = distance(debut,fin)
    if d == 0:
        return [debut]

    addvec = lambda p,v:PointFloat(p.x+v.x,p.y+v.y)
    vec = PointFloat(  (fin.x-debut.x)*pas/d,(fin.y-debut.y)*pas/d)
    point_suivant = debut
    while distance(point_suivant,fin)>=pas:
        segment.append(point_suivant)
        point_suivant = addvec(point_suivant,vec)
    return segment

def generer_mur(debut,fin,epaisseur):
    return [Obstacle(point,epaisseur) for point in generer_segment(debut,fin,2*epaisseur)]


def nom_couleur(couleur):
    couleurs = {
        "noir":noir,
        "blanc":blanc,
        "bleu":bleu,
        "rouge":rouge,
        "jaune":jaune,
        "vert":vert,
        "rose":rose,
        "orange":orange,
        "violet":violet,
    }
    for nom_couleur in couleurs:
        if couleurs[nom_couleur] == couleur:
            return nom_couleur
    return "couleur inconnue"


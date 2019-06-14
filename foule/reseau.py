from modele import *
from outils import *


class SommetReseau:
    def __init__(self,position):
        self.position = position
        self.parent = None
        self.voisins = set()
        self.distanceSortie = float('inf')
        self.vu = False

    @property
    def x(self):
        return self.position.x

    @property
    def y(self):
        return self.position.y

    @property
    def point(self):
        return Point(int(self.position.x),int(self.position.y))

    def ajouter_voisin(self,voisin):
        self.voisins.append(voisin)

    def afficher(self,couleur):
        affiche_cercle_plein(self.point,2,couleur)

    def key(self):
        return (round(self.position.x,4),round(self.position.y,4))


class Reseau:
    def __init__(self,personnage,pas):
        self.personnage = personnage
        self.L = self.personnage.monde.L
        self.H = self.personnage.monde.H
        self.pas = pas
        self.sorties = [SommetReseau(sortie) for sortie in personnage.sorties]

        self.creer_reseau()
        self.calculer_distances()



    def creer_reseau(self):
        self.sommets = dict()
        #creation des sommets
        for i in range(int(self.L/self.pas)+1):
            for j in range(int(self.H/self.pas)+1):
                sommet = SommetReseau(PointFloat(self.pas*i,self.pas*j))
                if self.in_reseau(sommet):
                    self.sommets[sommet.key()] = sommet

        #ajout des sorties
        for sortie in self.sorties:
            self.sommets[sortie.key()] = sortie
            for voisin in self.points_proches(sortie):
                if sortie != voisin:
                    sortie.voisins.add(voisin)
                    voisin.voisins.add(sortie)

        #mise à jour des voisins
        for sommet in self.sommets.values():
            i, j = sommet.position.x/self.pas, sommet.position.y/self.pas
            for di in range(-1,2):
                for dj in range(-1,2):
                    if di != 0 or dj != 0:
                        voisin = SommetReseau(PointFloat(self.pas*(i+di),self.pas*(j+dj)))
                        if voisin.key() in self.sommets:
                            voisin = self.sommets[voisin.key()]
                            sommet.voisins.add(voisin)


    def calculer_distances(self):
        a_traiter = []
        for sortie in self.sorties:
            sortie.distanceSortie = 0
            sortie.vu = true
            a_traiter.append(sortie)

        while a_traiter:
            a_traiter.sort(key = lambda sommet:sommet.distanceSortie,reverse = true)
            sommet = a_traiter.pop()
            sommet.vu = true
            for voisin in sommet.voisins:
                if not(voisin.vu) and not(voisin in a_traiter):
                    a_traiter.append(voisin)
                if voisin.distanceSortie > distance(voisin,sommet)+sommet.distanceSortie:
                    voisin.distanceSortie = distance(voisin,sommet)+sommet.distanceSortie
                    voisin.parent = sommet

    def in_reseau(self,sommet):
        p = sommet.position
        return -self.pas <= p.x and p.x <= self.L+self.pas and -self.pas <= p.y and p.y <= self.H+self.pas and not(self.personnage.monde.collision_obstacles(self.personnage,p))


    def points_proches(self,sommet):
        i,j = int(sommet.position.x/self.pas), int(sommet.position.y/self.pas)
        for di in range(2):
            for dj in range(2):
                point_proche = SommetReseau(PointFloat(self.pas*(i+di),self.pas*(j+dj)))
                if point_proche.key() in self.sommets:
                    yield self.sommets[point_proche.key()]

    def plus_proche(self,position):
        pps = [point for point in self.points_proches(SommetReseau(position))]
        if not(len(pps)):
            print(position)
        return min(self.points_proches(SommetReseau(position)),key = lambda sommet:distance(position,sommet.position))

    def afficher_chemin(self,position):
        sommet = self.plus_proche(position)
        while sommet.parent:
            affiche_ligne(sommet.point,sommet.parent.point,noir)
            sommet = sommet.parent

    def afficher(self):
        couleurs = [couleur(188,16,6),couleur(191,42,5),couleur(195,69,4),couleur(198,95,4),couleur(202,122,3),couleur(205,148,2),couleur(209,175,2),couleur(212,201,1),couleur(216,228,0),couleur(220,255,0)]
        dmax = max([sommet.distanceSortie for sommet in self.sommets.values()])
        for sommet in self.sommets.values():
            sommet.afficher(couleurs[min(int(sommet.distanceSortie*len(couleurs)/dmax),9)])
            #sommet.afficher(noir)

    def distance_sortie(self,position):
        point_proche = self.plus_proche(position)
        return distance(position,point_proche)+point_proche.distanceSortie

    @staticmethod
    def key(personnage,pas):
        key_sorties = [SommetReseau(sortie).key() for sortie in personnage.sorties]
        return (pas,tuple(key_sorties),personnage.rayon)

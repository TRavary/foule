from graphics import *

class PointFloat:
    def __init__(self,x = 0 ,y = 0):
        self.x = float(x)
        self.y = float(y)

    def __repr__(self):
        return "("+str(self.x)+","+str(self.y)+")"


def distance(a,b):
    return math.sqrt((b.x-a.x)**2+(b.y-a.y)**2)

class Personnage:
    def __init__(self,monde,position,sorties = [],rayon = 10):
        """ sorties : liste de pointfloat"""
        self.position = position
        self.rayon = 10
        self.monde = monde
        self.sorties = sorties

    def collision(self,personnage,position_personnage):
        return distance(self.centre,position_personnage)<(self.rayon+personnage.rayon)


class Obstacle:
    def __init__(self,centre,rayon):
        self.centre = centre
        self.rayon = rayon

    def collision(self,personnage,position_personnage):
        return distance(self.centre,position_personnage)<(self.rayon+personnage.rayon)

    def afficher(self):
        centre = Point(int(self.centre.x),int(self.centre.y))
        affiche_cercle_plein(centre,self.rayon,noir)

class Monde:
    def __init__(self,L,H):
        self.L = L
        self.H = H
        self.personnages = []
        self.obstacles = []

    def ajouter_personnage(self,personnage):
        if not(self.collision(personnage,personnage.position)):
            self.personnages.append(personnage)
        else:
            print("Impossible de rajouter le personnage à cet emplacement")

    def ajouter_obstacle(self,obstacle):
        for personnage in self.personnages:
            if obstacle.collision(personnage,personnage.position):
                print("Impossible de rajouter l'obstacle à cet emplacement")
                return
        self.obstacles.append(obstacle)

    def collision(self,personnage,position_personnage):
        for autre_personnage in self.personnages:
            if autre_personnage != personnage and autre_personnage.collision(personnage,position_personnage):
                return true
        for obstacle in self.obstacles:
            if obstacle.collision(personnage,position_personnage):
                return true
        return false

    def afficher(self):
        for obstacle in self.obstacles:
            obstacle.afficher()


class SommetReseau:
    def __init__(self,position):
        self.position = position
        self.parent = None
        self.voisins = set()
        self.distanceSortie = float('inf')
        self.vu = false

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
        return 0 <= p.x and p.x <= self.L and 0 <= p.y and p.y <= self.H and not(self.personnage.monde.collision(self.personnage,p))


    def points_proches(self,sommet):
        i,j = int(sommet.position.x/self.pas), int(sommet.position.y/self.pas)
        for di in range(2):
            for dj in range(2):
                point_proche = SommetReseau(PointFloat(self.pas*(i+di),self.pas*(j+dj)))
                if point_proche.key() in self.sommets:
                    yield self.sommets[point_proche.key()]

    def plus_proche(self,position):
        return min(self.points_proches(SommetReseau(position)),key = lambda sommet:distance(position,sommet.position))


    def afficher(self):
        couleurs = [couleur(188,16,6),couleur(191,42,5),couleur(195,69,4),couleur(198,95,4),couleur(202,122,3),couleur(205,148,2),couleur(209,175,2),couleur(212,201,1),couleur(216,228,0),couleur(220,255,0)]
        dmax = max([sommet.distanceSortie for sommet in self.sommets.values()])
        for sommet in self.sommets.values():
            sommet.afficher(couleurs[min(int(sommet.distanceSortie*len(couleurs)/dmax),9)])
            #sommet.afficher(noir)



def test_1():
    L = 800
    H = 600
    init_fenetre(L,H)
    affiche_auto_off()
    remplir_fenetre(blanc)

    monde = Monde(L,H)
    personnage = Personnage(monde,PointFloat(0,0),[PointFloat(L,0),PointFloat(60,H)])

    monde.ajouter_personnage(personnage)
    for i in range(10):
        monde.ajouter_obstacle(Obstacle(PointFloat(650,i*50),20))

    for i in range(5):
        monde.ajouter_obstacle(Obstacle(PointFloat(i*100,600-i*100),50))
    monde.ajouter_obstacle(Obstacle(Point(600,400),100))

    R = Reseau(personnage,20)
    R.afficher()
    monde.afficher()
    sommet = R.plus_proche(personnage.position)
    while sommet.parent:
        affiche_ligne(sommet.point,sommet.parent.point,noir)
        sommet = sommet.parent

    affiche_tout()
    attendre_echap()

def test_2():
    L = 1000
    H = 800
    init_fenetre(L,H)
    remplir_fenetre(blanc)
    affiche_auto_off()


    monde = Monde(L,H)
    personnage = Personnage(monde,PointFloat(0,0),[])

    while pas_echap():
        if touche_enfoncee('K_RETURN'):
            R = Reseau(personnage,8)
            R.afficher()
            monde.afficher()
            sommet = R.plus_proche(personnage.position)
            while sommet.parent:
                affiche_ligne(sommet.point,sommet.parent.point,noir)
                sommet = sommet.parent
            affiche_tout()
        elif touche_enfoncee('K_o'):
            print("En attente d'un obstacle")
            clic = wait_clic()
            obstacle =Obstacle(clic,50)
            monde.ajouter_obstacle(obstacle)
            obstacle.afficher()
            affiche_tout()
        elif touche_enfoncee('K_s'):
            print("En attente d'une sortie")
            clic = wait_clic()
            personnage.sorties.append(clic)
            print("Sortie sauvegardée")
        attendre(100)

test_2()
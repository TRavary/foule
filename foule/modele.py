from graphics import *
from reseau import *
from outils import *


class Personnage:
    def __init__(self,monde,position,sorties = [],rayon = 10,couleur = bleu):
        """ sorties : liste de pointfloat"""
        self.position = position
        self.rayon = rayon
        self.monde = monde
        self.sorties = sorties
        self.reseau = None
        self.couleur = couleur

        self.trace = False

        self.vitesse = 5.0
        self.deplacer = self.deplacer_contourne
        self.last_direction = "moins"

    @property
    def x(self):
        return self.position.x

    @property
    def y(self):
        return self.position.y

    def collision(self,personnage,position_personnage):
        return distance(self.position,position_personnage)<(self.rayon+personnage.rayon)

    def est_sorti(self):
        for sortie in self.sorties:
            if distance(sortie,self.position)< self.rayon/2:
                return true
        return false


    def afficher(self):
        position = Point(int(self.x),int(self.y))
        affiche_cercle_plein(position,self.rayon,self.couleur)
        for sortie in self.reseau.sorties:
            sortie.afficher(rouge)

        if self.trace:
            self.reseau.afficher()
            self.reseau.afficher_chemin(self.position)
            affiche_cercle(position,self.rayon + 2,self.couleur)


    def deplacer_stop_si_bloque(self):
        plus_proche = self.reseau.plus_proche(self.position)
        parent_plus_proche = plus_proche.parent
        if not(parent_plus_proche) or distance(self,parent_plus_proche) ==0:
            return
        coef = self.vitesse /distance(self,parent_plus_proche)
        dx, dy = coef * (parent_plus_proche.x-self.x), coef * (parent_plus_proche.y-self.y)
        position_visee = PointFloat(self.x+dx,self.y+dy)
        if not(self.monde.collision(self,position_visee)):
            self.position = position_visee

    def deplacer2(self):
        plus_proche = self.reseau.plus_proche(self.position)
        parent_plus_proche = plus_proche.parent
        if not(parent_plus_proche) or distance(self,parent_plus_proche) ==0:
            return
        coef = self.vitesse /distance(self,parent_plus_proche)
        dx, dy = coef * (parent_plus_proche.x-self.x), coef * (parent_plus_proche.y-self.y)
        position_visee = PointFloat(self.x+dx,self.y+dy)

        nouvelle_position = None
        vec = PointFloat(-dx,-dy)
        delta = 0.25
        ndelta = 0
        theta = 15   #angle en degré

        def cosdeg(angle):
            return math.cos(theta*math.pi/180)
        def sindeg(angle):
            return math.sin(theta*math.pi/180)
        def similitude(p,v,coef,angle):
            return PointFloat(  p.x + coef*(v.x*cosdeg(angle)-v.y*sindeg(angle)),p.y + coef*(v.x*sindeg(angle)+v.y*cosdeg(angle)))


        if self.trace:
            print("Personnage en ",self.position)
            print("\tposition visée :",position_visee)
        while not(nouvelle_position) and ndelta < 5:
            positions_potentielles = [similitude(position_visee,vec,ndelta*delta,k*theta) for k in range(-int(180/theta),int(180/theta))]
            positions_potentielles = [position for position in positions_potentielles if not(self.monde.collision(self,position)) and distance(self,position)<self.vitesse]
            if positions_potentielles:
                nouvelle_position = min(positions_potentielles,key = lambda position:self.reseau.distance_sortie(position))
            ndelta +=1

        if not(nouvelle_position):
            nouvelle_position = self.position
        self.position = nouvelle_position

    def deplacer_contourne(self):
        plus_proche = self.reseau.plus_proche(self.position)
        parent_plus_proche = plus_proche.parent
        if not(parent_plus_proche) or distance(self,parent_plus_proche) ==0:
            return
        coef = self.vitesse /distance(self,parent_plus_proche)
        dx, dy = coef * (parent_plus_proche.x-self.x), coef * (parent_plus_proche.y-self.y)
        position_visee = PointFloat(self.x+dx,self.y+dy)

        if not(self.monde.collision(self,position_visee)):
            self.position = position_visee
            return

        theta = 20
        ct = math.cos(theta*math.pi/180)
        st = math.sin(theta*math.pi/180)
        rotation_plus = lambda v:PointFloat(v.x*ct-v.y*st,v.x*st+v.y*ct)
        rotation_moins= lambda v:PointFloat(v.x*ct+v.y*st,-v.x*st+v.y*ct)

        addvec = lambda p,v:PointFloat(p.x+v.x,p.y+v.y)
        vplus  = PointFloat(dx,dy)
        vmoins = PointFloat(dx,dy)
        for n_rotations in range(1,int(180/theta)+1):
            vplus = rotation_plus(vplus)
            vmoins = rotation_moins(vmoins)
            positionplus = addvec(self.position,vplus)
            positionmoins = addvec(self.position,vmoins)
            valideplus = not(self.monde.collision(self,positionplus))
            validemoins = not(self.monde.collision(self,positionmoins))
            if valideplus and validemoins:
                if self.last_direction == "plus":
                    self.position = positionplus
                    return
                elif self.last_direction == "moins":
                    self.position = positionmoins
                    return
                elif random.randint(0,1):
                    self.position = positionplus
                    self.last_direction = "plus"
                    return
                else:
                    self.position = positionmoins
                    self.last_direction = "moins"
                    return
            elif valideplus:
                self.position = positionplus
                self.last_direction = "plus"
                return
            elif validemoins:
                self.position = positionmoins
                self.last_direction = "moins"
                return

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
        self.reseaux = dict()
        self.fluxs = []

        self.etape = 0

    def ajouter_flux(self,flux):
        self.fluxs.append(flux)
        personnage = flux.creer_personnage()
        self.push_reseau(personnage)


    def generer_personnages(self):
        for flux in self.fluxs:
            flux.generer_personnage()

    def ajouter_personnage(self,personnage):
        if not(self.collision(personnage,personnage.position)):
            self.push_reseau(personnage)
            self.personnages.append(personnage)
        else:
            print("Impossible de rajouter le personnage à cet emplacement")

    def ajouter_obstacle(self,obstacle):
        for personnage in self.personnages:
            if obstacle.collision(personnage,personnage.position):
                print("Impossible de rajouter l'obstacle à cet emplacement")
                return
        self.obstacles.append(obstacle)

    def collision_obstacles(self,personnage,position_personnage):
        for obstacle in self.obstacles:
            if obstacle.collision(personnage,position_personnage):
                return true
        return false

    def collision_personnages(self,personnage,position_personnage):
        for autre_personnage in self.personnages:
            if autre_personnage != personnage and autre_personnage.collision(personnage,position_personnage):
                return true
        return false

    def collision_bord(self,personnage,position_personnage):
        if position_personnage.x < 0 or position_personnage.x > self.L:
            return true
        if position_personnage.y < 0 or position_personnage.y > self.H:
            return true
        return false

    def collision(self,personnage,position_personnage):
        return self.collision_obstacles(personnage,position_personnage) or self.collision_personnages(personnage,position_personnage) or self.collision_bord(personnage,position_personnage)

    def push_reseau(self,personnage):
        pas = 10
        key_reseau = Reseau.key(personnage,pas)
        if not(key_reseau in self.reseaux):
            self.reseaux[key_reseau] = Reseau(personnage,8)
        personnage.reseau = self.reseaux[key_reseau]

    def supprimer_personnage(self,personnage):
        self.personnages.remove(personnage)

    def update_sorties_personnages(self):
        for personnage in self.personnages:
            if personnage.est_sorti():
                self.supprimer_personnage(personnage)

    def afficher(self):
        remplir_fenetre(blanc)
        for obstacle in self.obstacles:
            obstacle.afficher()
        for personnage in self.personnages:
            personnage.afficher()
        affiche_tout()

    def deplacer_personnages(self):
        for personnage in self.personnages:
            personnage.deplacer()

    def etape_suivante(self):
        #print("Etape ",self.etape)
        self.deplacer_personnages()
        self.generer_personnages()
        self.update_sorties_personnages()
        self.etape += 1

class Flux:
    def __init__(self,monde,ntour = 50, entrees = [], sorties = [],rayon = 10, couleur = bleu):
        """ génère des personnages à chaque tour de jeu ayant une entrée et une liste de sortie
        la couleur est la même pour les personnages d'un même flux
         sorties : liste de pointfloat
         entrees : liste de pointfloat """
        self.entrees = entrees
        self.sorties = sorties
        self.monde = monde
        self.couleur = couleur
        self.ntour = ntour
        self.rayon_personnage = rayon

        self.ntour_min = 1
        self.ntour_max = 200
        self.ntour_modif = 5

    def set_tour(self,tour):
        self.ntour = tour

    def ajouter_entree(self,entree):
        self.entrees.append(entree)

    def ajouter_sortie(self,sortie):
        self.sorties.append(sortie)

    def creer_personnage(self):
        return Personnage(self.monde,PointFloat(0,0),self.sorties,self.rayon_personnage,self.couleur)

    def generer_personnage(self):
        if self.ntour == self.ntour_max:
            return
        itour = random.randint(0,self.ntour)
        if itour == 0:  # création d'un personnage à l'une des entrées possibles
            personnageFictif = self.creer_personnage()
            entreesActive = [ entree for entree in self.entrees if not self.monde.collision(personnageFictif,entree)]
            if entreesActive : # il y a une entree de disponible
                ientree = random.randint(0,len(entreesActive)-1)
                personnageFictif.position = entreesActive[ientree]
                self.monde.ajouter_personnage(personnageFictif)

    def augmenter_debit(self):
        self.ntour = max(self.ntour-self.ntour_modif,self.ntour_min)

    def diminuer_debit(self):
        self.ntour = min(self.ntour+self.ntour_modif,self.ntour_max)






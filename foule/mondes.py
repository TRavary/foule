from modele import *
from outils import *


def monde_0():
    L = 1000
    H = 500
    monde = Monde(L,H)

    monde.ajouter_obstacle(Obstacle(PointFloat(3*L/4,0),220))
    monde.ajouter_obstacle(Obstacle(PointFloat(3*L/4,H),220))
    monde.ajouter_obstacle(Obstacle(PointFloat(L/2+10,H/2),50))


    bord_gauche = [PointFloat(0,y) for y in range(0,H,10)]
    bord_droit = [PointFloat(L,y) for y in range(0,H,10)]

    rayon = 15
    nb_perso_vers_droite = 200
    nb_perso_vers_gauche = 0
    for k in range(nb_perso_vers_droite):
        print("creation personnage vers droite ",k)
        x = random.random()*L/2
        y = random.random()*H
        monde.ajouter_personnage( Personnage(monde,PointFloat(x,y),bord_droit,rayon,bleu) )

    for k in range(nb_perso_vers_gauche):
        print("creation personnage vers gauche",k)
        x = L-random.random()*L/4
        y = random.random()*H
        monde.ajouter_personnage( Personnage(monde,PointFloat(x,y),bord_gauche,rayon,vert) )
    return monde

def monde_1():
    L = 1000
    H = 500
    monde = Monde(L,H)

    monde.ajouter_obstacle(Obstacle(PointFloat(3*L/4,0),220))
    monde.ajouter_obstacle(Obstacle(PointFloat(3*L/4,H),220))

    bord_gauche = [PointFloat(0,y) for y in range(0,H,10)]
    bord_droit = [PointFloat(L,y) for y in range(0,H,10)]

    rayon = 15
    nb_perso_vers_droite = 200
    nb_perso_vers_gauche = 0
    for k in range(nb_perso_vers_droite):
        print("creation personnage vers droite ",k)
        x = random.random()*L/2
        y = random.random()*H
        monde.ajouter_personnage( Personnage(monde,PointFloat(x,y),bord_droit,rayon,bleu) )

    for k in range(nb_perso_vers_gauche):
        print("creation personnage vers gauche",k)
        x = L-random.random()*L/4
        y = random.random()*H
        monde.ajouter_personnage( Personnage(monde,PointFloat(x,y),bord_gauche,rayon,vert) )
    return monde

def monde_2():
    L = 1000
    H = 500
    monde = Monde(L,H)

    monde.ajouter_obstacle(Obstacle(PointFloat(3*L/4,0),220))
    monde.ajouter_obstacle(Obstacle(PointFloat(3*L/4,H),220))
    monde.ajouter_obstacle(Obstacle(PointFloat(L/2+10,H/2),50))


    bord_gauche = [PointFloat(0,y) for y in range(0,H,10)]
    bord_droit = [PointFloat(L,y) for y in range(0,H,10)]

    rayon = 15
    nb_perso_vers_droite = 200
    nb_perso_vers_gauche = 0
    for k in range(nb_perso_vers_droite):
        print("creation personnage vers droite ",k)
        x = random.random()*L/2
        y = random.random()*H
        monde.ajouter_personnage( Personnage(monde,PointFloat(x,y),bord_droit,rayon,bleu) )

    for k in range(nb_perso_vers_gauche):
        print("creation personnage vers gauche",k)
        x = L-random.random()*L/4
        y = random.random()*H
        monde.ajouter_personnage( Personnage(monde,PointFloat(x,y),bord_gauche,rayon,vert) )
    return monde

def monde_3():
    L = 1000
    H = 500
    monde = Monde(L,H)

    bord_gauche = [PointFloat(0,y) for y in range(0,H,10)]
    bord_droit = [PointFloat(L,y) for y in range(0,H,10)]

    rayon = 10
    nb_perso_vers_droite = 100
    nb_perso_vers_gauche = 100
    for k in range(nb_perso_vers_droite):
        print("creation personnage vers droite ",k)
        x = random.random()*L/2
        y = random.random()*H
        monde.ajouter_personnage( Personnage(monde,PointFloat(x,y),bord_droit,rayon,bleu) )

    for k in range(nb_perso_vers_gauche):
        print("creation personnage vers gauche",k)
        x = L-random.random()*L/2
        y = random.random()*H
        monde.ajouter_personnage( Personnage(monde,PointFloat(x,y),bord_gauche,rayon,vert) )
    return monde

def monde_4():
    L = 1000
    H = 500
    monde = Monde(L,H)

    for i in range(8):
        monde.ajouter_obstacle(Obstacle(PointFloat(200,i*50),25))
    for i in range(0,12):
        monde.ajouter_obstacle(Obstacle(PointFloat(200+i*50,400),25))
        monde.ajouter_obstacle(Obstacle(PointFloat(L-i*50,200),25))

    bord_droit = [PointFloat(L,y) for y in range(0,150,10)]


    rayon = 10
    nb_perso_vers_droite = 100
    for k in range(nb_perso_vers_droite):
        print("creation personnage vers droite ",k)
        x = random.random()*L/5
        y = random.random()*H
        monde.ajouter_personnage( Personnage(monde,PointFloat(x,y),bord_droit,rayon,bleu) )
    return monde


def monde_5():
    L = 1000
    H = 500
    monde = Monde(L,H)

    bord_gauche = generer_segment(PointFloat(0,0),Point(0,H),10)
    bord_droit = generer_segment(PointFloat(L,0),Point(L,H),10)

    taille = 20
    frequence = 15

    monde.ajouter_flux(Flux(monde,frequence,bord_gauche,bord_droit,taille,bleu))
    monde.ajouter_flux(Flux(monde,frequence,bord_droit,bord_gauche,taille,vert))
    return monde


def monde_T_1():
    L = 700
    H = 700
    monde = Monde(L,H)

    largeur_porte = 80
    ecart = 20

    taille = 10
    frequence = 15

    bord_gauche_haut = generer_segment(PointFloat(0,H/2+ecart/2),Point(0,H/2+ecart/2+largeur_porte),10)
    bord_droit_haut = generer_segment(PointFloat(L,H/2+ecart/2),Point(L,H/2+ecart/2+largeur_porte),10)

    bord_gauche_bas = generer_segment(PointFloat(0,H/2-ecart/2),Point(0,H/2-ecart/2-largeur_porte),10)
    bord_droit_bas = generer_segment(PointFloat(L,H/2-ecart/2),Point(L,H/2-ecart/2-largeur_porte),10)

    bord_haut_gauche = generer_segment(PointFloat(L/2-ecart/2,H),Point(L/2-ecart/2-largeur_porte,H),10)
    bord_haut_droit = generer_segment(PointFloat(L/2+ecart/2,H),Point(L/2+ecart/2+largeur_porte,H),10)

    bord_bas_gauche = generer_segment(PointFloat(L/2-ecart/2,0),Point(L/2-ecart/2-largeur_porte,0),10)
    bord_bas_droit = generer_segment(PointFloat(L/2+ecart/2,0),Point(L/2+ecart/2-largeur_porte,0),10)




    monde.ajouter_flux(Flux(monde,frequence,bord_gauche_bas,bord_droit_bas,taille,bleu))
    monde.ajouter_flux(Flux(monde,frequence,bord_droit_haut,bord_gauche_haut,taille,vert))

    monde.ajouter_flux(Flux(monde,frequence,bord_bas_droit,bord_haut_droit,taille,jaune))
    monde.ajouter_flux(Flux(monde,frequence,bord_haut_gauche,bord_bas_gauche,taille,orange))


    return monde


def monde_T_2():
    L = 700
    H = 700
    monde = Monde(L,H)

    largeur_porte = 80
    ecart = 20

    taille = 10
    frequence = 15


    monde.ajouter_obstacle(Obstacle(PointFloat(L/2,H/2),150))


    bord_gauche_haut = generer_segment(PointFloat(0,H/2+ecart/2),Point(0,H/2+ecart/2+largeur_porte),10)
    bord_droit_haut = generer_segment(PointFloat(L,H/2+ecart/2),Point(L,H/2+ecart/2+largeur_porte),10)

    bord_gauche_bas = generer_segment(PointFloat(0,H/2-ecart/2),Point(0,H/2-ecart/2-largeur_porte),10)
    bord_droit_bas = generer_segment(PointFloat(L,H/2-ecart/2),Point(L,H/2-ecart/2-largeur_porte),10)

    bord_haut_gauche = generer_segment(PointFloat(L/2-ecart/2,H),Point(L/2-ecart/2-largeur_porte,H),10)
    bord_haut_droit = generer_segment(PointFloat(L/2+ecart/2,H),Point(L/2+ecart/2+largeur_porte,H),10)

    bord_bas_gauche = generer_segment(PointFloat(L/2-ecart/2,0),Point(L/2-ecart/2-largeur_porte,0),10)
    bord_bas_droit = generer_segment(PointFloat(L/2+ecart/2,0),Point(L/2+ecart/2-largeur_porte,0),10)

    monde.ajouter_flux(Flux(monde,frequence,bord_gauche_bas,bord_droit_bas,taille,bleu))
    monde.ajouter_flux(Flux(monde,frequence,bord_droit_haut,bord_gauche_haut,taille,vert))

    monde.ajouter_flux(Flux(monde,frequence,bord_bas_droit,bord_haut_droit,taille,jaune))
    monde.ajouter_flux(Flux(monde,frequence,bord_haut_gauche,bord_bas_gauche,taille,orange))


    return monde


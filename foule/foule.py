from modele import *
from mondes import *
import graphics

def simule_foule(monde):
    init_fenetre(monde.L,monde.H)
    remplir_fenetre(blanc)
    affiche_auto_off()
    monde.afficher()

    print("Creation terminée")

    trace_personnage = None
    flux_select = None

    touches_enfoncee_avant = dict()
    touches = ['K_p','K_a','K_z','K_KP_PLUS','K_KP_MINUS']
    for i in range(0,10):
        touches.append('K_KP'+str(i))
    for touche in touches:
        touches_enfoncee_avant[touche] = False

    def touche_relachee(touche):
        return not(touche_enfoncee(touche)) and touches_enfoncee_avant[touche]

    en_pause = False
    while 1:
        if not(en_pause):
            monde.etape_suivante()
        monde.afficher()
        clic = last_clic()
        if clic:
            if trace_personnage:
                trace_personnage.trace = False
            trace_personnage = None
            for personnage in monde.personnages:
                if distance(clic,personnage)<personnage.rayon:
                    personnage.trace = True
                    trace_personnage = personnage

        for touche in touches_enfoncee_avant:
            if touche_enfoncee(touche):
                touches_enfoncee_avant[touche] = True
        if touche_relachee('K_p'):
            touches_enfoncee_avant['K_p'] = False
            if en_pause:
                print("Execution redémarrée")
            else:
                print("Execution en pause : appuyer sur 'p' pour redémarrer")
            en_pause = not(en_pause)
        for i in range(0,len(monde.fluxs)):
            if touche_relachee('K_KP'+str(i)):
                touches_enfoncee_avant['K_KP'+str(i)] = False
                flux_select = monde.fluxs[i]
                print("Flux selectionné : ",i,"(",nom_couleur(flux_select.couleur),")" )

        if touche_relachee('K_KP_PLUS') or touche_relachee('K_z'):
            touches_enfoncee_avant['K_KP_PLUS'] = False
            touches_enfoncee_avant['K_z'] = False
            if flux_select:
                flux_select.augmenter_debit()
                print("Débit augmenté : Flux ",nom_couleur(flux_select.couleur))

        if touche_relachee('K_KP_MINUS') or touche_relachee('K_a'):
            touches_enfoncee_avant['K_KP_MINUS'] = False
            touches_enfoncee_avant['K_a'] = False
            if flux_select:
                flux_select.diminuer_debit()
                print("Débit diminué : Flux ",nom_couleur(flux_select.couleur))

        attendre(10)

    affiche_tout()



simule_foule(monde_T_2())

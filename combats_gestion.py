#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  5 19:10:53 2025

@author: Drayen
"""
from random import choice as rnd_choice , randint as rnd_randint
from math import sqrt
from json import load as JsonLoad

from rich import print as cstmprint
from rich.table import Table
from rich.text import Text

from pyjdr.Messages import Error
from pyjdr.dice_roller import Roll
from pyjdr.str_op import normalize
from pyjdr.creatures_definition import (player ,
                                         monster ,
                                         get_monster ,
                                         create_monster ,
                                         get_simplify_type ,
                                         get_monster_list)
from pyjdr.affichage_joueur_monstres import afficher_creature
from pyjdr.sauvegarde_et_chargement import getpath
path = getpath()


def creation_monstres() :
    nb = input("nb monstres : ")
    while not nb.isdigit() :
        Error("ValueError",f"the number of monsters must be an integer, not '{type(eval(nb))}'")
    nb = int(nb)
    for i in range(nb) :
        monstre = input(f"nom du monstre numéro {i+1} : ")
        monstre_classe = get_monster(monstre)
        if monstre_classe is None :
            create_monster(monstre)



def create_monster_package() :
    packs = [
        ("n x gobelin de base","nb"),
        ("n x ange","nb"),
        ("n x cube gelatineux","nb"),
        #("un dragon","element")
        ]
    print("packs disponibles : ")
    for i in range(len(packs)) :
        print(f"\t {i} - {packs[i][0]}")
    choix = input("votre choix : ")
    while not choix.isdigit() or int(choix) >= len(packs) :
        Error("ValueError",f"invalid value '{choix}'")
        choix = input("votre choix : ")
    choix = int(choix)

    if packs[choix][1] == "nb" :
        nb = input("nombre de monstres : ")
        while not nb.isdigit() :
            Error("ValueError",f"invalid value '{choix}' for input 'nombre de monstres'")
            nb = input("nombre de monstres : ")
        nb = int(nb)

        print(packs[choix][0].split("n x ")[1])
        print(normalize( packs[choix][0].split("n x ")[1] ))

        monstres = [ get_monster( normalize( packs[choix][0].split("n x ")[1] ) ) for _ in range(nb) ]
        if None in monstres :
            Error("NameError","any monster match to the one chosen, back to main core")
            return None

    return monstres , nb

def combat(etat_de_jeu) :
    print("\n\n--------------------------------------------------")
    cstmprint("un [red]combat[/red] a été [red]lancé[/red]")
    print("- le terrain est un rectangle dont les dimesions sont en mètres",
          "\n - les déplacements se font dans un cercle de 20m de rayon",
          "\n - les attaques se font dans un cercle de 2m de rayon")
    print("\n")
    # =============================================================================
    #     initialisation des paramètres de combat
    # =============================================================================

    # lst des persos
    persos = [ e for e in etat_de_jeu['personnages'] if e.Get("vie")[0] > 0 ]
    nb_persos = len( persos )

    # lst des monstres
    is_monster_package = input("voulez-vous utiliser un pack de monstres par défaut (o/n) ? ").lower() == "o"
    if is_monster_package :
        monstres , nb_monstres = create_monster_package()
        if monstres is None : return

    else :
        monstres = []
        with open(f"{path}/monstres/monstres_liste.json","r") as file :
            liste = JsonLoad(file)


        nb_monstres = input("nombre de monstres à affronter : ")
        while not nb_monstres.isdigit() :
            Error("ValueError",f"invalid value '{nb_monstres}' for input 'nombre de monstres'")
            nb_monstres = input("nombre de monstres à affronter : ")
        nb_monstres = int(nb_monstres)

        for i in range(nb_monstres) :
            nom = input(f"nom du monstre {i+1} (l si comme precedent) : ")
            if nom in ("l","L") :
                monstres.append(get_monster(monstres[-1].nom))
            else :
                nom = normalize(nom, liste)# ma fonction à moi (avec détection de faute de frappe si nom pas connu et que joueur veut)
                monstre_temp = get_monster(nom)
                if monstre_temp is None :
                    monstre_temp = create_monster(nom)
                monstres.append(monstre_temp)

    print("")
    # !!! don't delete this, it's for the next release :
    # difficulte_monstre = input("dificulté de l'algorithme de combat des monstres (0:facile à 1:moyen) : ") #2:dur
    # while not difficulte_monstre.isdigit() and int(difficulte_monstre) in range(2) :
    #     Error("ValueError",f"the value must be between 0 and 1, not '{difficulte_monstre}'")
    #     difficulte_monstre = input("diificulté de l'algorithme de combat des monstres (0:facile à 1:moyen) : ") #2:dur
    # difficulte_monstre = int(difficulte_monstre)

    print("difficulté des monstres : facile, la seule dispo")
    difficulte_monstre = 0

    if difficulte_monstre == 0 :
        choix_action_monstre = choix_action_monstre_simple

    print("")
    # le terrain
    long = input("longueur du terrain : ")
    while not long.isdigit() :
        Error("ValueError","invalid value '{long}', type int is expected")
        long = input("longueur du terrain : ")
    long = int(long)

    haut = input("hauteur du terrain : ")
    while not haut.isdigit() :
        Error("ValueError","invalid value '{haut}', type int is expected")
        haut = input("largeur du terrain : ")
    haut = int(haut)


    terrain = [ [0]*long  for _ in range(haut)]
    del long , haut


    # on a une seule liste de toutes les céatures sur le terrain et classée par ordre décroissant d'initiative
    creatures_en_vie_pas_trie = persos + monstres
    creatures_en_vie = []

    while creatures_en_vie_pas_trie != [] :
        maxi = 0

        for j in range(len(creatures_en_vie_pas_trie)) :
            if type(creatures_en_vie_pas_trie[maxi]) == player : stat = { "maxi" : "DEX" , "courant" : None }
            else : stat = { "maxi" : "init" , "courant" : None }

            if type(creatures_en_vie_pas_trie[j]) == player : stat["courant"] = "DEX"
            else : stat["courant"] = "init"

            if creatures_en_vie_pas_trie[j].stats[stat["courant"]] > creatures_en_vie_pas_trie[maxi].stats[stat["maxi"]] :
                maxi = j

        creatures_en_vie.append(creatures_en_vie_pas_trie.pop(maxi))

    del creatures_en_vie_pas_trie


    # correspondance nom : joueur/monstre (pour les monstres, on ajoute un numèro à la fin car ils n'ont pas de 'nom' en tant que tel)
    creatures = { e.Get("nom"):e for e in persos }
    # (pour les monstres, on ajoute un numèro à la fin car ils n'ont pas tous un 'nom' différent)
    temp = monstres.copy()
    monstres = {}
    for i in range(len(temp)) :
        nom = temp[i].Get("nom")
        num = 1
        while f"{nom}_{num}" in monstres :
            num += 1
        nom = f"{nom}_{num}"
        monstres[nom] = temp[i]
        monstres[nom].Modif("nom",nom)
        creatures[nom] = monstres[nom]
    del temp

    # placer les creatures sur le terrain
    print("les creatures (joueurs et monstres) sont placées aléatoirement sur les terrain")
    for e in creatures_en_vie :
        x,y = rnd_randint(0, len(terrain[0])-1) , rnd_randint(0, len(terrain)-1)
        while not isinstance(terrain[y][x], int) :
            x,y = rnd_randint(0, len(terrain[0])) , rnd_randint(0, len(terrain))
        terrain[y][x] = e.nom
        e.coord = (x,y)
    del x , y
    affichage_terrain(terrain, creatures)

    input("presser 'entrer' pour commencer...")

    # =============================================================================
    # boucle principale de combat
    # =============================================================================


    while nb_persos != 0 and nb_monstres != 0 :

        # persos = [ e for e in etat_de_jeu["personnages"] if e.vie[0] > 0 ]
        # nb_persos = len( persos )

        # monstres = [ e for e in monstres if monstres[e].vie[0] > 0 ]

        i = 0
        while i < len(creatures_en_vie) :

            creature = creatures_en_vie[i]
            creature_type = get_simplify_type(creature)

            print("\n---------------------------------")
            cstmprint( f"[bold black on white]{creature.nom}[/bold black on white] joue" )

            if creature_type == monster :
                choix_action_monstre(creatures_en_vie, creatures, creature.nom, terrain)

            elif creature_type == player :
                choix_action_joueur(creatures_en_vie, creatures, creature.nom, terrain)

            else :
                Error("CreatureError","invalid creature type '{creature_type}', type monster or player is excpected")
                return

            L = creatures_en_vie.copy()
            creatures_en_vie.clear()
            firstpop = None
            for j in range(len(L)) :
                if L[j].vie[0] > 0 :
                    creatures_en_vie.append(L[j])
                elif firstpop is None :
                    firstpop = j

            if firstpop is None :
                i += 1
            elif firstpop > i :
                i += 1

            nb_persos = len([e for e in creatures_en_vie if e.get_type()=="player"])
            nb_monstres = len(creatures_en_vie) - nb_persos

            if nb_monstres == 0 or nb_persos == 0 :
                break

            input("presser 'entrer' pour continuer...")


    print("\n\n")
    if nb_monstres == 0 :
        cstmprint("Vous avez [green]GAGNÉ ![/green]")
    else :
        cstmprint("Vous avez [red]PERDU ![/red]")

    print("\nfin ducombat\n--------------------------------------------------")


def affrontement(attaquant, attaquant_arme, attaquant_mod_attaque, creature_attaque, creatures_en_vie) :
    print("test d'attaque ...", end="" )
    test_attaque_attaquant = Roll((1,20)) + attaquant_mod_attaque

    if test_attaque_attaquant >= creature_attaque.DEF :
        cstmprint("[green]REUSSI[/green] [yellow];)[/yellow]")
        print(f"{attaquant.nom} attaque {creature_attaque.nom} avec {attaquant_arme['nom'][0]} ({attaquant_arme['DM']} + {'bonus'})")

        degats = Roll(attaquant_arme["DM"]) + attaquant_arme["bonus"]

        creature_attaque.damage([degats])

        print(f"vie de {creature_attaque.nom} : {creature_attaque.vie[0]} / {creature_attaque.vie[1]}")

        if creature_attaque.vie[0] <= 0 :
            for i in range(len(creatures_en_vie)) :
                if creatures_en_vie[i].nom == creature_attaque.nom :
                    creatures_en_vie.pop(i)
                    break

    else :
        cstmprint("[red]RATÉ[/red] [yellow]|([/yellow]")





def choix_action_monstre_simple(creatures_en_vie, creatures, nom_monstre, terrain) :
    """
    niveau1 de difficulté,
    1 deplacement ou 2 pour être suffsamment près pour attaquer ;
    puis 1 attaque si possible
    ( 1->deplacement ; 2->attaque ; 3->capacite speciale )

    """
    print("choix_action_monstre_simple")
    monstre = creatures[nom_monstre]
    nb_action = 2
    print(f"{nom_monstre} est en {monstre.coord}")
    while nb_action > 0 :
        joueurs_attaquables = creatures_attaquables(terrain, monstre.coord, creatures)
        # print("joueurs_attaquables",joueurs_attaquables)
        if joueurs_attaquables != [] :
            # print("attaque : ")
            cible = creatures[joueurs_attaquables[0]]
            cstmprint(f"{nom_monstre} attaque {cible.nom} : ")
            affrontement(monstre, rnd_choice(monstre.armes), monstre.modificateurs_stats["FOR"], cible, creatures_en_vie)

            nb_action -= 2

        else :
            print("déplacement")
            joueur_cible_coord = get_joueur_proche(terrain , monstre.coord , creatures)
            print("joueur_cible_coord",joueur_cible_coord)
            # target =  get_monstre_target(monstre , joueur_cible_coord) #  deplacement intermédiare ou non
            # print("target 1",target)
            target = joueur_cible_coord
            target = case_libre_proche_obj(terrain,target,monstre.coord)
            print("case_libre_proche_obj",target)

            if est_deplacement_possible(monstre.coord, target, terrain) :
                print("déplacement")
                deplacement(monstre, terrain, monstre.coord, target)
                nb_action -= 1
            else :
                Error("ValueError",f"invalid target '{target}' for '{monstre.nom}', exiting...")
                nb_action = -1


def choix_action_monstre_moyen(creatures_en_vie, creatures, nom_monstre, terrain ) :
    """
    niveau2 de difficulté,
    on se rapproche du joueur le plus faible (pouvant etre tué avec un minimum de coups)
    et le plus proche (ratioo deplacement / nb coups)
    puis on attaque on maintient une distance de securite de 1 dep
    ( 1->deplacement ; 2->attaque ; 3->capacite speciale )

    """
    print("not implemented yet")
    pass

    nb_action = 2
    while nb_action > 0 :
        action = None


    # TODO

def choix_action_monstre_dur(creatures_en_vie, creatures, nom_monstre, terrain) :
    pass
    # TODO

def choix_action_joueur(creatures_en_vie, creatures, nom_joueur, terrain) :

    affichage_terrain(terrain,creatures)

    liste = get_monster_list()

    personnage = creatures[nom_joueur]

    nb_actions = 2
    print("actions disponibles : ")
    print("\t 1) déplacement (1 à 20 m) (d)")
    print("\t 2) attaque (arme simple) (a)")
    print("\t 3) faire une action limitée (not implemented yet) (l)")

    while nb_actions > 0 :
        action = input("votre choix : ")
        while not action in ( "1","2","3","d","a","l" ) :
            Error("ValueError",f"invalid value '{action}' for a player action, please select one one of the element below by entering its number or the letter in parenthesis")

        if action in ("1","d") :
            coord_init = personnage.coord
            print(f"vos coordonnées : {coord_init}")

            objectif = tuple(input("votre objectif (au format x,y /!\\ virgule obligatoire) : ").split(","))
            while not est_deplacement_possible(personnage.coord, objectif, terrain) and not objectif[0].isdigit() and not objectif[1].isdigit() :
                Error("ValueError",f"invalid target '{objectif}'")
                objectif = tuple(input("votre objectif (au format x,y /!\\ virgule obligatoire) : ").split(","))

            objectif = ( int(objectif[0]) , int(objectif[1]) )

            deplacement(personnage, terrain, personnage.coord, objectif)
            cstmprint( f"déplacement {coord_init} -> {objectif} [green]V[/green]" )
            nb_actions -= 1
            print("\n-----")


        elif action in ("2","a") :

            attaquables = creatures_attaquables( terrain , personnage.coord, creatures)

            if attaquables == [] :
                cstmprint("[red]aucun[/red] monstre à attaquer \n")

            else :

                print("creatures attaquables (à 2m ou moins de vous) : ")
                for i , creature in enumerate( attaquables ) :
                    print(f"\t {i}) {creature}")

                inp = ""
                liste = list(creatures.keys())
                while inp != "n" :
                    inp = normalize(input("nom du monstre à détailler (n si aucun) : ") , liste + ["n"] , "nom du monstre à détailler")
                    if inp in creatures :
                        afficher_creature(creatures[inp])
                    elif inp != "n" :
                        Error("NameError",f"unknown creature '{inp}'")

                cible = normalize(input("nom du monstre à attaquer : ") , attaquables , "nom du monstre à attaquer")
                while not cible in attaquables :
                    Error("NameError",f"unknown monster '{cible}'")
                    cible = normalize(input("nom du monstre à attaquer : ") , attaquables , "nom du monstre à attaquer")

                cible = creatures[cible]

                if len(personnage.armes) > 1 :
                    print("armes disponibles : ")
                    for i in range(len(personnage.armes)) :
                        arme = personnage.armes[i]
                        print((f"\t {i}) {arme['nom'][0]}, {arme['DM'][0]}D{arme['DM'][1]} + {arme['bonus']}"))

                    arme_choisie = input("numéro de l'arme choisie : ")
                    while not arme_choisie.isdigit() and int(arme_choisie) >= len(personnage.armes) :
                        Error("ValueError",f"invalid value '{arme_choisie}', it must be one of the numbers below")
                        arme_choisie = input("numéro de l'arme choisie : ")

                    arme_choisie = personnage.armes[int(arme_choisie)]

                else :
                    arme_choisie = personnage.armes[0]
                    print(f"arme utilisée pour votre combat : {arme_choisie} (la seule disponible pour {personnage.nom})")

                mod = input("modificateur d'attaque (FOR, INT, SAG, DEX, ...) : ") .upper()
                while not mod in ("FOR","INT","SAG","DEX","CHA","CON") :
                    Error("ValueError",f"invalid value '{mod}', it must be 'FOR','INT','SAG','DEX','CHA'or'CON'")
                    mod = input("modificateur d'attaque (FOR, INT, SAG, DEX, ...) : ") .upper()

                affrontement(personnage, arme_choisie, personnage.modificateurs_stats[mod], cible, creatures_en_vie)

                nb_actions -= 2
                print("")

        elif action in ("3","l") :
            print("Not Implemented yet, please wait next release")

        else :
            Error("ValueError")

    # TODO


# =============================================================================
# gestion de l'affichage du terrain
# =============================================================================
def print_terrain(terrain,creatures) :
    cstmprint("[underline bold]Terrain :[/underline bold]")
    cstmprint("  \\_[green]V[/green] -> joueur")
    cstmprint("  \\_[red]X[/red] -> monstre")
    # tbl rich

    table = Table(show_header=False, show_lines=True, expand=False, box=None)
    for _ in range(len(terrain[0])+1) :
        table.add_column(justify="center" , style="bold")

    table.add_row(" " , *[f"{i}" for i in range(len(terrain[0]))])

    for i in range(len(terrain)) :
        ligne = []
        for e in terrain[i] :
            if type(e) == str :
                if get_simplify_type(creatures[e]) == player :
                    ligne.append(Text("V" , style="green"))
                elif get_simplify_type(creatures[e]) == monster :
                    ligne.append(Text("X" , style="red"))
                else :
                    ligne.append(Text("°"))
            else :
                ligne.append(Text("°"))

        table.add_row(f"{i}",*ligne)

    cstmprint(table)

# def affichage_terrain(terrain,creatures) :
#     print_terrain(terrain , creatures)
#     print("\ninformations complémentaires sur une case (au format x,y) \n",
#           "/!\\ les coords doivent séparées par des virgules + pour quiter, tapez q :",)
#     inp = ""
#     while inp.lower() != "q" :
#         inp = input("\ncoord de la case : ")
#         if not "," in inp and not inp.split(",")[0].isdigit() and not inp.split(",")[1].isdigit() and inp != "q" :
#             Error("ValueError",f"invalid value'{inp}' for coordinates, 'x,y' format is expected and x and y must be integers")
#         elif inp != "q" :
#             coord = inp.split(",")
#             coord[0] , coord[1] = int(coord[0]) , int(coord[1])
#             if 0 <= coord[0] < len(terrain[0])  and  0 <= coord[1] < len(terrain) :
#                 obj = terrain[coord[1]][coord[0]]
#                 if type(obj) == str :
#                     if get_simplify_type(obj) == player :
#                         afficher_creature(obj)
#                     elif get_simplify_type(obj) == monster :
#                         afficher_creature(obj)
#                     else :
#                         print("case vide")
#                         Error("DevError",f"we musn't have a string in {coord}")

#                     print_terrain(terrain, creatures)

#                 else :
#                     print("case vide")
#             else :
#                 Error("CoordError",f"non-existent box '{coord}'")


#     print("sortie de l'affichage du terrain, bonne suite de combat ;)")

def affichage_terrain(terrain, creatures):
    print_terrain(terrain, creatures)
    print("\nInformations complémentaires sur une case (au format x,y)\n"
        "/!\\ Les coordonnées doivent être séparées par une virgule ; pour quitter, tapez q :")
    while True:
        inp = input("\nCoordonnées de la case : ").strip()
        if inp.lower() == "q":
            break

        if not "," in inp:
            Error("ValueError",f"Invalid value '{inp}' for coordinates. Format attendu : 'x,y' avec x et y entiers.")
            continue

        x_str, y_str = (part.strip() for part in inp.split(",", maxsplit=1))

        try:
            x = int(x_str)
            y = int(y_str)
        except ValueError:
            Error(
                "ValueError",
                f"Invalid value '{inp}' for coordinates. x et y doivent être des entiers."
            )
            continue

        # Contrôle des bornes
        if not (0 <= y < len(terrain)) or not (0 <= x < len(terrain[0])):
            Error("CoordError", f"Non-existent box '{(x, y)}'")
            continue

        obj = terrain[y][x]

        if isinstance(obj, str):
            obj = creatures.get(obj)
            # obj_type = get_simplify_type(obj)
            # if obj_type == "player":
            #     afficher_creature(obj)
            # elif obj_type == "monster":
            #     afficher_creature(obj)
            # else:
            #     print("Case vide")
            #     Error("DevError", f"We shouldn't have a string in {x,y}")
            if obj is None :
                print("Case vide")
                Error("DevError", f"We shouldn't have a string in {x,y}")
            else :
                afficher_creature(obj)

            print_terrain(terrain, creatures)
        else:
            print("Case vide")

    print("Sortie de l'affichage du terrain, bonne suite de combat ;)")


# =============================================================================
# outils de scan du terrain
# =============================================================================
def creatures_attaquables(terrain , coord, creatures) :
    R = []
    creature_type = creatures[terrain[coord[1]][coord[0]]].get_type()
    for i in range(len(terrain)) :
        for j in range(len(terrain[i])) :
            if not isinstance(terrain[i][j], int) and distance((j,i), coord) <= 2 and creature_type != creatures[terrain[i][j]].get_type() :
                if creatures[terrain[i][j]].vie[0] > 0 :
                    R.append(terrain[i][j])
    return R

def est_deplacement_possible(coord : tuple , target : tuple , terrain) :
    return isinstance(coord, tuple) and isinstance(target, tuple) and \
        isinstance(coord[0], int) and isinstance(coord[1], int) and \
        isinstance(target[0], int) and isinstance(target[1], int) and \
        0<=target[0] and target[0]<len(terrain[0]) and 0<=target[1] and target[1]<len(terrain) and \
        distance(coord, target) <= 20  and  isinstance( terrain[target[1]][target[0]] , int )


def deplacement(creature, terrain, coord, target) :
    # coord[0] : abscisse ; coord[1] : ordonne
    terrain[coord[1]][coord[0]] , terrain[target[1]][target[0]] = 0 , creature.nom
    creature.coord = target


def distance(pt1,pt2) :
    return sqrt( (pt2[0] - pt1[0])**2  +  (pt2[1] - pt1[1])**2 )


# =============================================================================
# outils de prise de decision des monstres
# =============================================================================
def get_joueur_proche(terrain , monstre_coord , creatures) :
    # renvoie coord du joueur le plus proche
    L_coord = []
    for i in range(len(terrain)) :#y
        for j in range(len(terrain[i])) :#x
            if ( not isinstance(terrain[i][j], int) ) and creatures[terrain[i][j]].get_type() == "player" :
                if creatures[terrain[i][j]].vie[0] > 0 :
                    L_coord.append((j,i))

    if L_coord == [] :
        return None

    L_distance = [ distance( c , monstre_coord) for c in L_coord]

    i_min_d , mini = 0 , L_distance[0]
    for i in range(len(L_distance)) :
        if L_distance[i] < mini :
            i_min_d , mini = i , L_distance[i]

    return L_coord[i_min_d]


def case_libre_proche_obj(terrain,target,monstre_coord) :
    disque_target = disque(target , 2 , terrain) # zone d'attaque
    disque_monstre = disque(monstre_coord , 20 , terrain)# zone de déplacement
    # print(disque_monstre)

    cases_communes = []

    for i in range(len(disque_target)) :
        for j in range(len(disque_monstre)) :
            if disque_target[i] == disque_monstre[j] :
                cases_communes.append(disque_target[i])

    cases_libres = []
    for e in cases_communes :
        if est_deplacement_possible(monstre_coord, target, terrain) :
            cases_libres.append(e)
    del cases_communes

    # print(cases_libres)

    if len(cases_libres) == 0 :
        # case du cercle du monstre la plus proche de target dans le disque du monstre
        # print("intersection")
        coord = disque_monstre[0]
        if coord == target :
            coord = disque_monstre[1]
        dist = distance(target, coord)
        for e in disque_monstre :
            if e != target and distance(target, e) < dist :
                coord = e
                dist = distance(target, e)
        return coord


    else :
        # case la plus loin du monstre
        coord = cases_libres[0]
        dist = distance(monstre_coord, coord)
        for e in cases_libres :
            if distance(monstre_coord, e) > dist and est_deplacement_possible(monstre_coord, e, terrain) :
                coord = e
                dist = distance(monstre_coord, e)
        return coord



def disque(centre,rayon,terrain,obj=None) :
    # r = rayon
    # coord_lst = []
    # # on construit un disque de centre 0,0
    # for rayon in range(r+1) :
    #     for x in range(0,rayon+1) :
    #         coord_lst.append(( x , int(ceil(sqrt( rayon**2 - x**2 ) )) ))
    #         #coord_lst = [ ( int(ceil(sqrt( rayon**2 - (x-centre[0])**2 ) -centre[1] )) , x ) for x in range(0,rayon+1) ]

    # for coord in coord_lst :
    #     coord_lst.append( ( -coord[0] , coord[1] ) )
    #     coord_lst.append( ( coord[0] , -coord[1] ) )
    #     coord_lst.append( ( -coord[0] , -coord[1] ) )

    # # ???
    # for i in range(len(coord_lst)) :
    #     coord_lst[i] = ( centre[0]+coord_lst[i][0] , centre[1]+coord_lst[i][1] )

    # print(coord_lst)

    # Rep = []
    # for i in range(len(coord_lst)) :
    #     try :
    #         a_aj = True
    #         terrain[coord_lst[i][1]][coord_lst[i][0]]
    #     except Exception :
    #         a_aj = False
    #     finally :
    #         if a_aj :
    #             Rep.append(coord_lst[i])

    # return Rep

    quart_hd = [] # quart en haut à droite
    # on construit un disque de centre 0,0
    for x in range(rayon+1) :
        y_max = int(sqrt( rayon**2 - x**2 ) )
        for y in range(y_max) :
            quart_hd.append(( x , y ))

    coord_lst = []
    xc,yc = centre

    if obj :
        xo,yo = obj
        if xc >= xo :
            for e in quart_hd :
                coord_lst.append(e)
            quart_bd = [ (x,-y) for (x,y) in quart_hd ]
            for e in quart_bd :
                coord_lst.append(e)
        if xc >= xo :
            quart_hg = [ (-x,y) for (x,y) in quart_hd ]
            for e in quart_hg :
                coord_lst.append(e)
            quart_bg = [ (x,-y) for (x,y) in quart_hg ]
            for e in quart_bg :
                coord_lst.append(e)
    else :
        for e in quart_hd :
            coord_lst.append(e)
        quart_bd = [ (x,-y) for (x,y) in quart_hd ]
        for e in quart_bd :
            coord_lst.append(e)
        quart_hg = [ (-x,y) for (x,y) in quart_hd ]
        for e in quart_hg :
            coord_lst.append(e)
        quart_bg = [ (x,-y) for (x,y) in quart_hg ]
        for e in quart_bg :
            coord_lst.append(e)

    # ???
    for i in range(len(coord_lst)) :
        coord_lst[i] = ( xc+coord_lst[i][0] , yc+coord_lst[i][1] )

    Rep = []
    for i in range(len(coord_lst)) :
        y_max = len(terrain)
        x_max = len(terrain[0])
        if coord_lst[i][1] >= 0 and coord_lst[i][1] < y_max and coord_lst[i][0] >= 0 and coord_lst[i][0] < x_max :
            Rep.append(coord_lst[i])

    #print(Rep)

    return Rep

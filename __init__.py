"""
Ce module fournit une aide à la gestion de vos parties et combats de jeu de role
en permettant de stocker des informations sur des joueurs et des monstres

-------------------------------------------------------------------------------
fonctions :
    start -> démarre une partie
    gamemanager -> gérer les parties
    normalize -> petit bonus de normalisation de chaines de caractère, pas vraiment utile pour le jeux
"""

from pyjdr.Check.check_deps import check_PyJDR_deps
check_PyJDR_deps()

import os
from rich import print as cstmprint


from pyjdr.game_set import CreateGameSet
from pyjdr.Messages import Error , PrintMsg
from pyjdr.confrontations import franchissement
from pyjdr.combats_gestion import combat
from pyjdr.affichage_joueur_monstres import afficher_creature
from pyjdr.sauvegarde_et_chargement import save_game , load_game , getpath
from pyjdr.navigation_monstres import naviguer
from pyjdr.str_op import normalize
path = getpath()

__all__ = [ "start" , "gamemanager" , "normalize" ]

#%% Main
def start() :
    """
    this function just launch a game

    Returns
    -------
    None.

    """

    global  nom_partie , etat_de_jeu , to_save
    nom_partie , etat_de_jeu = _init_JDR()
    # print(etat_de_jeu)
    _jouer()
    if to_save :
        save_game(nom_partie, etat_de_jeu)
        PrintMsg(("Votre partie a été [green]enregistrée[/green] avec succès ",1) , f"dans le dossier : '{nom_partie}'")


def _jouer() :
    global  nom_partie , etat_de_jeu , is_night , to_save
    print("Bienvenu dans pyjdr !!\n")
    consignes = """
[underline bold green]consigne de jeu : [/underline bold green]
- vous pouvez y avoir accès à tout moment en entrant "help" dans les inputs généraux
- un dé se représente sous la forme (a,b) où a est le nb de dé lancé et b et le type de dé (d6 ou d20 par ex)
- les regles du jeux de rôle utilisées sont celles de Chroniques Oubliées
- à chaque tour, differentes possibilites s'offrent à vous :
    1 - lancer un combat (c)
    2 - interagir avec les PNJ (i)
    3 - franchir un obstacle (o)
    4 - se soigner (sort ou potions) (s)
    5 - interchanger le jour et la nuit (n ou j en fonction du cas)
    6 - dormir pour récupérer des PV (uniquement de nuit (d)
    7 - quitter et sauvegarder (q)
    8 - quitter sans sauvegarder (e)
    9 - afficher un personnage (a)
    10 - naviguer dans la liste des monstres (m)
    """
    cstmprint(consignes)

    to_save = True
    is_night = False

    inp = ""
    while inp != "q" and inp != "7" and inp != "e" and inp != "8" :
        inp = input("\n menu principal - votre choix : ")

        if inp in ("help" , "h" , "0") :
            cstmprint(consignes)


        elif inp == "c" or inp == "1" :
            combat(etat_de_jeu)


        elif inp in ("i","o") or inp in ("2","3") :
            if inp in ("o","3") :
                objet = "obstacle"
                msg = "franchi"
            else :
                objet = "PNJ"
                msg = "non convaincu"

            stat = input("stat utilisée : ")
            stat = stat.upper()
            mod = eval(input("éventuel modificateur (une liste ou non de dé ou d'entier) : "))
            seuil = int(input("minimum pour la victoire : "))
            perso = input("nom du perso faisant le test : ")
            perso = _vrai_perso(perso)

            if perso == None :
                Error("NameError","unknown character")
            else :
                if franchissement(stat , seuil , perso , mod) :
                    PrintMsg( ( f"{objet} [green]{msg}[/green]" , 1 ) )
                else :
                    PrintMsg( ( "vous avez [red]échoué[/red]" , 1 ) )


        elif inp == "s" or inp == "4" :
            perso = input("nom du perso subissant le soin (sort ou potion) : ")
            perso = _vrai_perso(perso)
            choix = input("potion ? (o/n)").lower() == "o"

            if choix :
                i = 0
                LPersoPot = []
                print("personnages avec une potion : ")
                for e in etat_de_jeu["personnages"] :
                    inv = e.inv
                    for j in range(len(inv)) :
                        if "potion" in inv[j] :
                            print(f"\t{i}) {e.nom} : {inv[j]}")
                            LPersoPot.append({ "perso":e , "i_obj":j })
                            i += 1

                if len(LPersoPot) == 0 :
                    print("AUCUN")

                else :
                    soigneur = input("numéro de perso + potion à faire le soin")
                    while not soigneur.isdigit() or int(soigneur) >= len(LPersoPot) :
                        Error("ValueError",f"invalid index value '{soigneur}'")
                        soigneur = input("numéro de perso + potion à faire le soin")
                    soigneur = LPersoPot[int(soigneur)]
                    pot = soigneur["i_obj"]
                    soigneur = soigneur["perso"]

                    pot = soigneur.inv.pop(pot).split(":")[-1]
                    perso.heal(pot)


            else :
                soin = eval(input("montant du soin (un entier ou un dé) : "))
                perso.heal(soin)


        elif inp in ("n","j") or inp == "5" :
            if inp == "n" and is_night :
                print("impossible il fait déjà nuit")
            elif inp =="n" :
                is_night = True
                print(r"""
    _|_
     |   NUIT   _\_
           _|_   \
            |""")
            elif inp == "j" and is_night :
                is_night = False
                print(r"""
    \___ /
    /   |
    |___/   JOUR
   /    \ """)
            elif inp == "j" :
                print("impossible il fait déjà jour")
            else :
                is_night = not is_night


        elif inp == "d" or inp == "6" :
            if is_night :
                etat_de_jeu["personnages"].heal("D")
                etat_de_jeu["personnages"].resume("vie")
            else :
                print("quand ce n'est pas la nuit, on ne dort pas !!")


        elif inp == "q" or inp == "7" :
            to_save = True


        elif inp == "e" or inp == "8" :
            to_save = False


        elif inp == "a" or inp == "9" :
            print("entrée dans le mode 'affichage perso', tapez q pour quiter")
            print("liste des personnages : ")
            personnages = etat_de_jeu["personnages"].Get("all")
            personnages = [ perso.nom for perso in personnages ]
            for e in personnages :
                print(f"\t - {e}")
            print("")
            perso = ""
            while perso != "q" :
                perso = input("nom du personnage : ")
                if not _vrai_perso(perso) is None :
                    afficher_creature(_vrai_perso(perso))
                else :
                    Error("NameError",f"unknown character {perso}")


        elif inp in ("m","10") :
            naviguer()


        else :
            Error("CommandError" , f"invalid command '{inp}', type 'h' to get help")


def _init_JDR() :
    """
    hargement / création de la partie

    Returns
    -------
    nom_partie : str
        nom de la partie.
    etat_de_jeu : dict
        etat_de_jeu{

            }.

    """
    old = False
    nom_partie = input("nom de votre partie : ")
    partie = path+"/"+"parties/"+nom_partie

    if not os.path.exists(partie):
        os.makedirs(partie)
        etat_de_jeu = CreateGameSet()
    else :
        while os.path.exists(partie) and not old:
            print("cette partie existe déjà, vous voulez la charger ?")
            old = bool(int(input("oui (1) ou non (0) : ")))
            if old :
                etat_de_jeu = load_game(nom_partie)
            else :
                nom_partie = input("nom de votre partie : ")
                partie = path+"/parties/"+nom_partie
        if not old :
            os.makedirs(partie)
            etat_de_jeu = CreateGameSet()
            print(partie, "created")
            print("etat_de_jeu","created")

    save_game(nom_partie, etat_de_jeu)

    print(etat_de_jeu)

    return nom_partie , etat_de_jeu


def _vrai_perso(perso_nom) :
    for i in range(len(etat_de_jeu["noms"])) :
        if etat_de_jeu["noms"][i] == perso_nom :
            return etat_de_jeu["personnages"].Get(i)
    return None


#%% GameManager

def gamemanager() :
    """
    it's an interface to manage all your games (delete, preview or rename)

    Returns
    -------
    None.

    """

    parties = os.listdir(path+"/parties")
    actions = ["supprimer une partie (s)","visualiser une partie (v)","renommer partie+joueurs (r)","quitter (q)"]

    def printgamesandactions(parties,actions) :
        print("liste des parties : ")
        for i,p in enumerate(parties) :
            print(f"\t{i}) {p}")

        print("\nactions disponibles : ")
        for i,a in enumerate(actions) :
            print(f"\t{i}) {a}")

    printgamesandactions(parties,actions)

    inp = input("Gamemanager - votre choix : ")
    while not inp in ("3","q") :

        if inp in ("0","s") :
            _deletegame(parties)
            parties = os.listdir(path+"/parties")
            printgamesandactions(parties,actions)

        elif inp in ("1","v") :
            _seegame(parties)
            printgamesandactions(parties,actions)

        elif inp in ("2","r") :
            _rename(parties)

        else :
            Error("ValueError",f"invalid value '{inp}'")
        inp = input("\nGameManager - votre choix : ")

    print("\n\n----------------\n\nexit")


def _deletegame(parties) :
    print("liste des parties : ")
    for i,p in enumerate(parties) :
        print(f"\t{i}) {p}")

    inp = input("GameManager - DeleteGame - numéro de la partie à supprimer : ")
    while not isvalidgame(parties,inp) :
       inp = input("GameManager - DeleteGame - numéro de la partie à supprimer : ")
    inp = int(inp)

    if input(f"voulez vous supprimer '{parties[inp]}' (o/n) ? ").lower() == "o" :
        os.remove(path+"/parties/"+parties[inp]+'/JdR_game_objects.pkl')
        os.rmdir(path+"/parties/"+parties[inp])
        print("partie SUPPRIMEE")


def _seegame(parties) :
    global etat_de_jeu
    print("liste des parties : ")
    for i,p in enumerate(parties) :
        print(f"\t{i}) {p}")

    inp = input("GameManager - DeleteGame - numéro de la partie à visualiser : ")
    while not isvalidgame(parties,inp) :
       inp = input("GameManager - DeleteGame - numéro de la partie à visualiser : ")
    inp = int(inp)

    print(parties[inp],":")

    etat_de_jeu = load_game(parties[inp])
    print("entrée dans le mode 'affichage perso', tapez q pour quiter")
    print("liste des personnages : ")
    personnages = etat_de_jeu["personnages"].Get("all")
    personnages = [ perso.nom for perso in personnages ]
    for e in personnages :
        print(f"\t - {e}")
    print("")
    perso = ""
    while perso != "q" :
        perso = input("nom du personnage : ")
        if not _vrai_perso(perso) is None :
            afficher_creature(_vrai_perso(perso))
        else :
            Error("NameError",f"unknown character {perso}")


def _rename(parties) :
    inp = input("GameManager - DeleteGame - numéro de la partie à renommer : ")
    while not isvalidgame(parties,inp) :
       inp = input("GameManager - DeleteGame - numéro de la partie à renommer : ")

    etat_de_jeu = load_game(parties[inp])

    if input(f"voulez-vous rennomer la partie '{parties[inp]}' (o/n) ? ").lower() == "o" :
        newgamename = input("nouveau nom : ")
        while input(f"'{parties[inp]}' -> '{newgamename}' ? (o/n) ").lower == "n" :
            newgamename = input("nouveau nom : ")

    persos = etat_de_jeu["personnges"]
    for p in persos :
        if input(f"voulez-vous rennomer '{p.nom}' (o/n) ? ").lower() == "o" :
            newname = input("nouveau nom : ")
            while input(f"'{p.nom}' -> '{newname}' ? (o/n) ").lower == "n" :
                newname = input("nouveau nom : ")
            p.nom = newname

    os.remove(path+"/parties/"+parties[inp]+'/JdR_game_objects.pkl')
    os.rmdir(path+"/parties/"+parties[inp])

    os.makedirs(path+"/parties/"+newgamename)
    save_game(newgamename, etat_de_jeu)




def isvalidgame(parties,inp) :
    if inp.isdigit() :
        if not int(inp) in range(len(parties)) :
            Error("IndexError",f"list index '{int(inp)}' out of range")
            return False
        else :
            return True
    else :
        Error("TypeError",f"list indexes must be integers, not '{inp}'")
        return False

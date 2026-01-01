#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  4 15:13:12 2025

@author: Drayen
"""
from json import load

from pyjdr.game_elements import *
from pyjdr.dice_roller import Roll , Roll_liste
from pyjdr.Messages import Error , PrintMsg
from pyjdr.sauvegarde_et_chargement import getpath
path = getpath()

#%% joueur

class player() :
    def __init__(self,nom,race,metier,information_complementaires = "None") :
        mod_stat = Modificateurs_stats()
        equipements = equipements_departs()

        # pour le combat uniquement :
        self.coord = None # (x,y) en combat

        self.niv = 1

        self.nom , self.race , self.metier = nom , race , metier

        self.stats = {"FOR":0 , "DEX":0 , "CON":0 , "INT":0 , "SAG":0 , "CHA":0}
        for e in self.stats :
            res = Roll_liste((4,6))   # on lance 4D6 et on enlève le moins bon
            res = sum(res) - min(res) # la stat vaut alors la somme des dés plus un modificateur lié à la race du perso
            self.stats[e] = ( res ) + mod_stat[race][e]

        self.modificateurs_stats = { e : 0.5*(self.stats[e]-self.stats[e]%2)-5 if e != 1 else -4 for e in self.stats } # équation du tableau dans la marge du livre des règles du Jdr de chroniques oubliées page 6

        self.armes = equipements[self.metier]["armes"]  # le nom est une liste de mots clés donnant ses caractéristiques, le dernier élément est son véritable nom
        self.arme_utilisee = self.armes[0] # ici on stocke toutes les caractéristiques

        self.armures = equipements[self.metier]["armures"]  # le nom None signifie qu'il n'y a pas d'armure ici
        self.boucliers = equipements[self.metier]["boucliers"]
        self.defences = [ self.boucliers[0]["prot"] , self.armures[0]["prot"] , self.modificateurs_stats["DEX"]] # ici on stocke juste les défences : indice 0 = bouclier ; indice 1 = armure
        self.DEF = sum(self.defences)

    # TODO : armes utilisables en fonction metier
        self.armes_utilisables = {
            "dague" : False ,
            "épée" : True ,
            "1main" : True ,
            "2main" : True ,
            "masse" : True , #type masse : marteau, massue, gourdin, ...
            "arc" : True ,
            "baton" : True ,
            "baton mage" : False ,
            "grimoire" : False ,
            }

        self.Dvie = Des_vie()[metier]
        self.vie = Roll(self.Dvie)
        self.vie = [self.vie] * 2 # on la stocke dans une liste avec indice 0 = pts de vie actuels  et  indice 1 = pts de vie max à ce niv

        #TODO : Capacités
        self.capacites = ["TODO"]*10

        self.argent = 10.0 #en pièce d'or, 1 argent = 1/2 or  et  1 bronze = 1/4 or
        self.inv = ["torche","couverture"] + equipements[self.metier]["autres"]

        self.infos = information_complementaires

        self.tout = {
            "niv" : self.niv ,
            "nom" : self.nom ,
            "race" : self.race ,
            "metier" : self.metier ,
            "stats" : self.stats ,
            "modificateurs_stats" : self.modificateurs_stats ,
            "armes" : self.armes ,
            "arme_utilisee" : self.arme_utilisee ,
            "armes_utilisables" : self.armes_utilisables ,
            "armures" : self.armures ,
            "boucliers" : self.boucliers ,
            "defences" : self.defences ,
            "DEF" : self.DEF ,
            "Dvie" : self.Dvie ,
            "vie" : self.vie ,
            "argent" : self.argent ,
            "inv" : self.inv ,
            "infos" : self.infos ,
            "capacites" : self.capacites
            }

    def __str__(self) :
        return str(self.tout)

    def Get(self,key : str) :
        if key == "all" :
            return self.tout
        elif key in self.tout :
            return self.tout[key]
        Error("ValueError",f"the key '{key}' doesn't exist, you can't get it, please restart")
        return None

    def Modif(self , key:str , newvalue) :
        if key in self.tout and hasattr(self, key) :
            self.tout[key] = newvalue
            setattr(self, key, newvalue)
        else :
            Error("ValueError",f"the key '{key}' doesn't exist, you can't modify it, please restart")

    def modif_vie(self , value : (tuple , list , int , float) , sign:(1,-1)) :
        if value == "D" :
            to_mod = Roll(self.Dvie)
        elif type(value) in (tuple,list) :
            to_mod = Roll(value)
        elif type(value) in (int,float) :
            to_mod = value
        else :
            to_mod = 0
            Error("MethodError",f"unknown value '{value}' for heal")
        self.Modif("vie", [ max( min( self.vie[0] + (to_mod*sign) , self.vie[1] ) , 0 ) , self.vie[1] ] )

    def heal(self , value : (tuple , list , int , float)) :
        self.modif_vie(value,sign=1)

    def damage(self,value:list) :
        if isinstance(value , int) :
            self.modif_vie(value,sign=-1)

        elif isinstance(value, (list,tuple)) :
            for i in range(len(value)) :
                if type(value[i]) in (tuple,list) and len(value[i]) == 2:
                    value[i] = Roll(value[i])
                elif type(value[i]) in (int,float) or value[i] == "D":
                    pass
                else :
                    value[i] = 0
                    Error("ValueError",f"incompatible value '{value[i]}', 0 has been used instead")
        self.modif_vie(sum(value),sign=-1)

    def get_type(self) :
        return "player"

class player_list() :
    def __init__(self) :
        self.list = []

    def __len__(self) :
        return len(self.list)

    def __str__(self) :
        return str(self.list)

    def __iter__(self) :
        return iter(self.list)

    def __next__(self) :
        return next(self.list)

    def append(self,elem) :
        self.list.append(elem)

    def pop(self,index) :
        return self.list.pop(index)

    def Change(self,index,new) :
        self.list[index] = new

    def Get(self,index) :
        if index == "all" :
            return self.list
        return self.list[index]

    def heal(self,method) :
        for e in self.list :
            e.heal(method)

    def resume(self, elem) :
        print(f"{elem} : ")
        for perso in self.list :
            print(f"\t {perso.nom} : ",end="")
            if hasattr(perso, elem) :
                print(getattr(perso,elem))
            else :
                Error(AttributeError,f"'{perso.nom}' doesn't have any attribute named '{elem}'")

#%% monstre
from pyjdr.str_op import normalize

from pickle import load as pkl_load , dump as pkl_dump
from json import load as json_load , dump as json_dump

def get_monster(monster_name) :
    with open (path+"/monstres/monstres_liste.json","r") as file :
        liste = json_load(file)
    if monster_name in liste :
        with open(f"{path}/monstres/{monster_name}.pkl","rb") as file_monster :
            return pkl_load( file_monster )
    else :
        with open(path+"/trad_fr-en/en_to_fr.json","r") as file :
            dic_monsters_en_to_fr = json_load(file)
        monster_name_fr = dic_monsters_en_to_fr.get(monster_name)
        if not monster_name_fr is None :
            with open(f"{path}/monstres/{monster_name_fr}.pkl","rb") as file_monster :
                return pkl_load( file_monster )

    return None


def create_monster(monster_name:str) -> None :
    with open (path+"/monstres/monstres_liste.json","r") as file :
        liste = json_load(file)
    if monster_name in liste :
        Error("NameError",f"monster '{monster_name}' already exists, you can't redefine it")
        return None

    print("\n\n----------------------------------------------------")
    PrintMsg( f"le monstre '{monster_name}' " , ("[red]n'existe pas[/red]",1) , " dans votre base de données, veuillez le" , (" [red]définir[/red]",1) , " en répondant aux questions" )
    print("/!\\ une fois saisie, une information ne peut plus être modifié /!\\")

    elem = [ # le premier parametre reste le nom mais il n'entre pas dans la liste des demandes etant fourni a l'appel de la fonction
        "sa défence",
        "sa vie",
        "son initiative" ,
        "son modificateur de force" ,
        "son modificateur de dextérité" ,
        "son modificateur de constitution" ,
        "son modificateur d'intelligence" ,
        "son modificateur de sagesse" ,
        "son modificateur de charisme" ,
        "le nombre d'armes",
        "le nombre de capacités",
        "informations complémentaires (non obligatoire, None si rien)"
        ]
    param = []
    param.append(monster_name)

    for i in range(len(elem)) :
        if "armes" in elem[i] :
            a_ajouter = []
            inp = input(elem[i]+" : ")
            while not inp.isdigit() :
                Error("ValueError",f"invalid value '{inp}' for input '{elem[i]}'")
                inp = input(elem[i]+" : ")
            inp = int(inp)

            for j in range(inp) :
                nom = input(f"nom de son arme {j+1} : ")

                de = input("dé des dégats (6,10,20,...) : ")
                while not de.isdigit() :
                    Error("ValueError",f"invalid value '{de}' for input 'dé des dégats'")
                    de = input("dé des dégats : ")
                de = int(de)

                nb = input("nb de dés lancés : ")
                while not nb.isdigit() :
                    Error("ValueError",f"invalid value '{nb}' for input 'nb de dés lancés'")
                    nb = input("nb de dés lancés : ")
                nb = int(nb)
                a_ajouter.append( { "nom":[nom] , "DM":(nb,de) } )
            param.append(a_ajouter)


        elif "capacités" in elem[i] :
            a_ajouter = []
            inp = input(elem[i]+" : ")
            while not inp.isdigit() :
                Error("ValueError",f"invalid value '{inp}' for input '{elem[i]}'")
                inp = input(elem[i]+" : ")
            inp = int(inp)
            for j in range(inp) :
                nom = input(f"nom de la capacité {j+1} : ")
                descr = input(f"description de la capacité {j+1} : ")
                a_ajouter.append( { "nom":nom , "description":descr } )
            param.append(a_ajouter)

        elif "info" in elem[i] :
            param.append(input(elem[i] + " : "))

        else :
            # type_target = int
            a_ajouter = input(elem[i]+" : ")
            while not (a_ajouter.lstrip('-').isdigit()) :
                Error("ValueError",f"invalid value '{a_ajouter}' for input '{elem[i]}'")
                a_ajouter = input(elem[i]+" : ")
            param.append(int(a_ajouter))

    monster_object = monster(param)


    liste.append(monster_name)
    with open (path+"/monstres/monstres_liste.json","w") as file :
        json_dump(liste,file)

    with open(f"{path}/monstres/model_monstre_{monster_name}.pkl","wb") as monster_file :
        pkl_dump(monster_object, monster_file)

    print("----------------------------------------------------\n\n")
    return monster_object





class monster():
    def __init__(self,liste_de_param:list) :
        # capacites est juste une liste des cap du monstre, on aura 60 % de chance d'en utiliser une aléatoirement
        # (on ne prend pas en core en compte les cap de type L)
        # TODO
        nom,DEF,PV,Init,ModFor,ModDex,ModCon,ModInt,ModSag,ModCha,armes,capacites,information_complementaires = liste_de_param

        # pour le combat uniquement :
        self.coord = None # (x,y) en combat

        self.nom = normalize(nom)
        self.race = self.nom
        self.DEF = DEF
        self.vie = (PV,PV)
        self.init = Init
        self.stats = {"init":self.init}
        self.modificateurs_stats = { # mod de stat
            "FOR" : ModFor ,
            "DEX" : ModDex ,
            "CON" : ModCon ,
            "INT" : ModInt ,
            "SAG" : ModSag ,
            "CHA" : ModCha ,
            }
        self.armes = armes
        self.capacites = capacites
        self.infos = information_complementaires

        self.tout = {
            "coord":self.coord ,
            "nom" : self.nom ,
            "stats" : self.stats ,
            "modificateurs_stats" : self.modificateurs_stats ,
            "init" : self.init ,
            "armes" : self.armes ,
            "DEF" : self.DEF ,
            "vie" : self.vie ,
            "infos" : self.infos
            }

    def __str__(self) :
        return str(self.tout)

    def Get(self,key : str) :
        if key == "all" :
            return self.tout
        elif key in self.tout :
            return self.tout[key]
        Error("ValueError",f"the key '{key}' doesn't exist, you can't get it, please restart")
        return None

    def Modif(self , key:str , newvalue) :
        if key in self.tout and hasattr(self, key) :
            self.tout[key] = newvalue
            setattr(self, key, newvalue)
        else :
            Error("ValueError",f"the key '{key}' doesn't exist, you can't modify it, please restart")

    def modif_vie(self , value : (tuple , list , int , float) , sign:(1,-1)) :
        if value == "D" :
            to_mod = Roll(self.Dvie)
        elif type(value) in (tuple,list) :
            to_mod = Roll(value)
        elif type(value) in (int,float) :
            to_mod = value
        else :
            Error("MethodError",f"unknown value '{value}' for heal")
            return
        self.Modif("vie", [ max( min( self.vie[0] + (to_mod*sign) , self.vie[1] ) , 0 ) , self.vie[1] ] )

    def heal(self , value : (tuple , list , int , float)) :
        self.modif_vie(value,sign=1)

    def damage(self,value:list) :
        if isinstance(value , int) :
            self.modif_vie(value,sign=-1)

        elif isinstance(value, (list,tuple)) :
            for i in range(len(value)) :
                if type(value[i]) in (tuple,list) and len(value[i]) == 2:
                    value[i] = Roll(value[i])
                elif type(value[i]) in (int,float) or value[i] == "D":
                    pass
                else :
                    value[i] = 0
                    Error("ValueError",f"incompatible value '{value[i]}', 0 has been used instead")
        self.modif_vie(sum(value),sign=-1)

    def get_type(self) :
        return "monster"

def get_monster_list() :
    with open(path+"/monstres/monstres_liste.json" , "r") as file :
        return load(file)

#%% joueur et monstre
def get_simplify_type(creature):
    creature = type(creature)
    if "monster" in str(creature):
        return monster
    elif "player" in str(creature):
        return player
    return creature

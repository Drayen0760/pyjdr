#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 18 17:10:08 2025

@author: Drayen
"""
from rich import print as cstmprint

from pyjdr.game_elements import Races , Metiers
from pyjdr.Messages import Error
from pyjdr.creatures_definition import player , player_list
from pyjdr.Messages import Error

def CreateGameSet() :
    races = Races()
    metiers = Metiers()

    affiche_L(races,head="races disponibles :")
    affiche_L(metiers,head="métiers disponibles :")

    nb_perso = input("nombre de joueurs : ")
    while not nb_perso.isdigit() :
        Error("TypeError","an integer is expected")
        nb_perso = input("nombre de joueurs : ")
    nb_perso = int(nb_perso)
    nom_persos = {}
    races_persos = {}
    métiers_persos = {}
    personnages = player_list()

    for i in range(nb_perso) :
        inp = "defaut"
        nom_persos[i] = inp
        while inp in nom_persos.values() :
            inp = input(f"nom du personnage {i} : ")
            if inp in nom_persos.values() :
                Error("NameError","this name allready exists, please restart")
        nom_persos[i] = inp

        done = False
        while not done :
            try :
                races_persos[i] = races[ int(input(f"race (son numéro) du personnage {i} : ")) - 1 ]
                métiers_persos[i] = metiers[ int(input(f"métier (son numéro) du personnage {i} : ")) - 1 ]
                done = True
            except (IndexError , ValueError) :
                Error("IndexError","the index you entered is incorrect, please restart")
        personnages.append( player(nom_persos[i] , races_persos[i] , métiers_persos[i]) )
        print("\n")
    return { "personnages":personnages , "noms":nom_persos }



def affiche_L(L , head : str = "") :
    cstmprint( "[underline red]" + head + "[/underline red]" )
    a_afficher = ""
    for i in range(len(L)) :
        a_afficher += f"{i+1}- {L[i]} \n"
    cstmprint(a_afficher)

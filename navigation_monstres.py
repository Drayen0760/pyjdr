#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  8 15:08:01 2025

@author: Drayen
"""
from json import load as jsonload

from pyjdr.creatures_definition import get_monster
from pyjdr.str_op import normalize
from pyjdr.affichage_joueur_monstres import afficher_creature
from pyjdr.sauvegarde_et_chargement import getpath
path = getpath()

def naviguer() :
    with open(f"{path}/monstres/monstres_liste.json","r") as file :
        lst_monstres = jsonload(file)

    print("type e, ex, exit, q or quit to quit")
    exit_main_loop = ("e","ex","exit","q","quit")
    inp = ""
    while True :
        inp = input("nom de votre monstre :\n\t")
        if inp in exit_main_loop : return

        inp = normalize(inp,lst_monstres)
        if type(inp) != int :
            inp = get_monster(inp)
            afficher_creature(inp)
        else :
            print("monstre inconnu")

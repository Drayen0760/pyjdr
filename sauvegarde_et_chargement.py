#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 18 20:34:51 2025

@author: Drayen
"""
import pickle
from site import getusersitepackages

path = getusersitepackages() + "/pyjdr"

def getpath() :
    return path

def save_game(nom_partie,etat_jeu) :
    with open(path+"/parties/"+nom_partie+"/"+"JdR_game_objects.pkl" , "wb") as file:
        pickle.dump( etat_jeu , file )
    return "done"


def load_game(nom_partie) :
    with open(path+"/parties/"+nom_partie+"/"+"JdR_game_objects.pkl" , "rb") as file:
        etat_jeu = pickle.load(file)
    return etat_jeu

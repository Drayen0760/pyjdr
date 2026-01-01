#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 23 12:59:38 2025

@author: jasta
"""
from pyjdr.dice_roller import Roll
from pyjdr.creatures_definition import player
from pyjdr.Messages import Error

def franchissement(stat , seuil , perso:player , mod) :
    if stat not in ("FOR","DEX","CON","INT","SAG","CHA") :
        Error("ValueError","invalid stat")
        return False
    elif seuil < 0 or seuil > 20 :
        Error("ValueError","invalid limit")
        return False
    elif type(perso) != player :
        Error("ValueError","invalid character")
        return False

    if type(mod) == list :
        mod = sum( [ Roll(e) if type(e)==tuple and len(e)==2 else e for e in mod ] )
    elif type(mod) == tuple and len(mod) == 2 :
        mod = Roll(mod)
    elif type(mod) in (int,float) :
        pass
    else :
        Error("ValueError","invalid mod")

    mod = perso.Get("modificateurs_stats")[stat] + mod # check
    res = Roll((1,20)) + mod
    return res >= seuil

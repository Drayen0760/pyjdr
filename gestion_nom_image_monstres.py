#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  3 09:12:19 2025

@author: Drayen
"""
from pathlib import Path
from os import renames
from json import load as jsonload

from pyjdr.str_op import normalize


def changement_nom_img(nom : str , dic_trad : dict) -> str :
    nom = nom.split(".")
    ext = "." + nom[-1]
    nom =  dic_trad[ normalize( nom[0].split("-modified")[0] ) ]
    return nom + ext



def main() :
    with open("trad_fr-en/en_to_fr.json","r") as file :
        dic_trad = jsonload(file)

    dossier = Path("monstres/monstres_images")
    dossier_str = "monstres/monstres_images/"
    fichiers = [e.name for e in dossier.iterdir() if e.is_file()]
    fichiers_nouveau_nom = [changement_nom_img(e,dic_trad) for e in fichiers]

    for i in range(len(fichiers)) :
        renames(dossier_str + fichiers[i], dossier_str + fichiers_nouveau_nom[i])

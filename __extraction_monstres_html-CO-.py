#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  1 18:07:59 2025

@author: jasta
"""
from pickle import dump as pkl_dump
import json
from bs4 import BeautifulSoup
from pathlib import Path
import re

from pyjdr.creatures_definition import monster as Monstre
from pyjdr.str_op import normalize
from pyjdr.sauvegarde_et_chargement import getpath
path = getpath()

def normalisation_stat(stat:str) -> int :
    r = ""
    signe = 1
    for e in stat :
        if e.isdigit() :
            r = r + e
        elif e == "-" :
            signe = -1
    if r == "" :
        return 0
    return signe * int(r)

def normalisation_arme(armes : str) -> list:
    # Séparer chaque arme/dégât par les majuscules ou transitions de texte
    segments = re.split(r'(?<=[a-z0-9\)])(?=[A-ZÉ])', armes)

    # Liste finale pour les armes
    armes = []

    for segment in segments:
        # Extraire le nom de l'arme (jusqu'à la première mention de "DM")
        match_nom = re.match(r'([\w\s\(\)éÉà]+)', segment)
        if not match_nom:
            continue
        nom = match_nom.group(1).strip()

        # Extraire les dégâts (format 1dX+Y ou 1dX)
        match_dm = re.findall(r'(\d+)d(\d+)(?:\+(\d+))?', segment)
        if not match_dm:
            continue

        for dm in match_dm:
            nb_de, type_de, bonus = dm
            nb_de = int(nb_de)
            type_de = int(type_de)
            bonus = int(bonus) if bonus else 0

            # Ajouter à la liste des armes avec dégâts
            armes.append({
                "nom": [nom.lower()],  # Normalisation en minuscule
                "DM": (nb_de, type_de),
                "bonus": bonus
            })

    return armes


def extraire_monstre(file_html:str) -> Monstre:

    with open(file_html,"r") as html_content :
        soup = BeautifulSoup(html_content, 'html.parser')

    # Extraction des informations générales
    nom = normalize(soup.find('div', class_='field--name-name').text.strip())
    DEF = normalisation_stat(soup.find('div', class_='field--name-defense').find('div', class_='field__item').text.strip())
    PV = normalisation_stat(soup.find('div', class_='field--name-health-point').find('div', class_='field__item').text.strip())
    Init = normalisation_stat(soup.find('div', class_='field--name-init').find('div', class_='field__item').text.strip())

    # Modificateurs de statistiques
    stats = {}
    stat_rows = soup.select('table tr')
    for row in stat_rows:
        cells = row.find_all('td')
        if len(cells) == 3:
            stats["FOR"] = normalisation_stat(cells[0].text.strip().replace("FOR", "").strip())
            stats["DEX"] = normalisation_stat(cells[1].text.strip().replace("DEX", "").replace("*", "").strip())
            stats["CON"] = normalisation_stat(cells[2].text.strip().replace("CON", "").strip())
        elif len(cells) == 2:
            stats["INT"] = normalisation_stat(cells[0].text.strip().replace("INT", "").strip())
            stats["SAG"] = normalisation_stat(cells[1].text.strip().replace("SAG", "").replace("*", "").strip())
            stats["CHA"] = normalisation_stat(cells[1].text.strip().replace("CHA", "").strip())

    # Armes
    armes = []
    for attaque in soup.select('div.field--name-attacks p'):
        armes.append(attaque.text.strip())
    armes = normalisation_arme(armes[0])

    # Capacités
    capacites = []
    for cap in soup.select('article.capability .accordion-header button'):
        capacites.append(cap.text.strip())

    # Informations complémentaires
    infos = {}
    infos_table = soup.select('table.table-striped tr')
    for row in infos_table:
        th = row.find('th')
        td = row.find('td')
        if th and td:
            infos[th.text.strip()] = td.text.strip()

    # Création d'une instance de la classe Monstre
    liste_de_param = [
        nom,
        DEF,
        PV,
        Init,
        stats.get("FOR", 0),
        stats.get("DEX", 0),
        stats.get("CON", 0),
        stats.get("INT", 0),
        stats.get("SAG", 0),
        stats.get("CHA", 0),
        armes,
        capacites,
        infos,
    ]
    return Monstre(liste_de_param)


def enregistrer_monstres(dic_monstres : dict , print_all : bool = False) -> None :
    for monstre in dic_monstres :
        if print_all : print(f"enristrement du monstre '{monstre}' ",end="")
        with open( f"{path}/monstres/{monstre}.pkl" , "wb" ) as file :
            pkl_dump(dic_monstres[monstre] , file)
        if print_all : print("réalisé avec SUCCÉS")


# Exemple d'utilisation
if __name__ == "__main__":
    print_all = False
    # Chemin du dossier
    dossier = Path("/home/jasta/websites/Jeu_De_Role/JdR_Monstres/www.co-drs.org/fr/bestiaire/creatures")
    dossier_str = "/home/jasta/websites/Jeu_De_Role/JdR_Monstres/www.co-drs.org/fr/bestiaire/creatures/"
    # Liste des fichiers uniquement
    fichiers = [e.name for e in dossier.iterdir() if e.is_file()]

    monstres_liste = [ normalize(nom.split(".")[0]) for nom in fichiers ]
    monstres_liste.append("pyjdr")

    with open(path+"/monstres/monstres_liste.json","w") as file :
        json.dump(monstres_liste,file)

    dic = {}
    print("extractions en cours ...")
    for i in range(len(fichiers)) :
        if print_all : print(f"monstre '{monstres_liste[i]}' ",end="")
        dic[monstres_liste[i]] = extraire_monstre(dossier_str + fichiers[i])
        if print_all : print("extrait avec SUCCÉS")
    print("extractions RÉUSSIES")

    print("\n------\n")

    print("enregistrements en cours ...")
    enregistrer_monstres(dic,print_all)

    monstre_pyjdr = Monstre(["pyjdr",
                             15,
                             100,
                             1000,
                             -100,
                             100,
                             100,
                             100,
                             100,
                             100,
                             [{"nom" : ["épée","dé truqué"] , "DM" : (20,20) , "bonus" : 0}],
                             [None]*10,
                             {'Catégorie de créature': 'Dragon',
                              'Milieu naturel': 'Grotte du Dé',
                              'Archétype': 'Standard',
                              'Taille': 'Géant',
                              "histoire": "Pyjdr est un dragon antique, lové autour d’une relique oubliée depuis des siècles dans les profondeurs de la Grotte du Dé. Son corps scintillant porte les marques d’une magie ancienne. Les rares légendes à son sujet parlent d'une créature aux connaissances infinies. Certains disent qu’il attend… mais personne ne sait quoi "
                                 }
        ])
    with open( f"{path}/monstres/pyjdr.pkl" , "wb" ) as file :
        pkl_dump(monstre_pyjdr , file)
    if print_all : print("pyjdr... done")

    print("enregistrements RÉUSSIS")

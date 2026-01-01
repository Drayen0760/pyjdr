#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 18 17:14:32 2025

@author: Drayen
"""
def Races() :
    return [ "elfe haut" , "elfe sylvain" , "demi-elfe" , "nain" , "demi-orque" , "humain" ]

def Metiers() :
    return [ "magicien" , "prètre" , "voleur" , "guerrier" ]

def Modificateurs_stats() :
    return {
        "elfe haut" : {
            "FOR": -2 ,
            "DEX": 0 ,
            "CON": 0 ,
            "INT": 0 ,
            "SAG": 0 ,
            "CHA": 2
            } ,
        "elfe sylvain" : {
            "FOR": -2 ,
            "DEX": 2 ,
            "CON": 0 ,
            "INT": 0 ,
            "SAG": 0 ,
            "CHA": 0
            } ,
        "demi-elfe" : {
            "FOR": 0 ,
            "DEX": 0 ,
            "CON": -2 ,
            "INT": 0 ,
            "SAG": 2 ,
            "CHA": 0
            } ,
        "nain" : {
            "FOR": 0 ,
            "DEX": -2 ,
            "CON": 2 ,
            "INT": 0 ,
            "SAG": 0 ,
            "CHA": 0
            } ,
        "demi-orque" : {
            "FOR": 2 ,
            "DEX": 0 ,
            "CON": 0 ,
            "INT": -2 ,
            "SAG": 0 ,
            "CHA": -2
            } ,
        "humain" : {
            "FOR": 0 ,
            "DEX": 0 ,
            "CON": 0 ,
            "INT": 0 ,
            "SAG": 0 ,
            "CHA": 0
            } ,
        }

def Modificateurs_attaque() :
    # TODO
    return {
        "magicien": {
            "att" : "FOR" ,
            "dist" : "DEX" ,
            "mag" : "INT"
            } ,
        "prètre" : {
            "att" : "FOR" ,
            "dist" : "DEX" ,
            "mag" : "SAG"
            } ,
        "voleur" : {
            "att" : "FOR" ,
            "dist" : "DEX" ,
            "mag" : "None"
            } ,
        "guerrier" : {
            "att" : "FOR" ,
            "dist" : "None" ,
            "mag" : "None"
            }
        }

def Des_vie() :
    # motif : indice 0 = nb lancé ; indice 1 = nb faces dé
    return {
        "magicien": (1,4) ,
        "prètre" : (1,8) ,
        "voleur" : (1,6) ,
        "guerrier" : (1,10)
        }

def equipements_departs() :
    return {
        "magicien": {
            "armes" : [  {"nom":["baton","1main","2main","baton"] , "DM":(1,6) , "bonus":0 }  ,  {"nom":["dague","1main"] , "DM":(1,4) , "bonus":0 }  ] ,
            "armures" : [ {"nom":"None" , "prot":0} ] ,
            "boucliers" : [ {"nom":"None" , "prot":0} ] ,
            "autres" : ["grimoire","potion de soin:(1,8)"]
            } ,
        "prètre" : {
            "armes" : [  {"nom":["masse","1main","marteau de guerre"] , "DM":(1,6) , "bonus":0}  ] ,
            "armures" : [ {"nom":"chemise de maille" , "prot":4} ] ,
            "boucliers" : [ {"nom":"petit bouclier" , "prot":1} ] ,
            "autres" : []
            } ,
        "voleur" : {
            "armes" : [  {"nom":["épée","1main","rapière"] , "DM":(1,6) , "bonus":0 }  ,  {"nom":["dague","1main"] , "DM":(1,4) , "bonus":0 }  ] ,
            "armures" : [ {"nom":"armure en cuire" , "prot":2} ] ,
            "boucliers" : [ {"nom":"None" , "prot":0} ] ,
            "autres" : ["outils de crochetage"]
            } ,
        "guerrier" : {
            "armes" : [  {"nom":["épée","1main","épée longue"] , "DM":(1,8) , "bonus":0 }  ,  {"nom":["épée","2main"] , "DM":(2,6) , "bonus":0  }  ] ,
            "armures" : [ {"nom":"cotte de maille" , "prot":5} ] ,
            "boucliers" : [ {"nom":"grand bouclier" , "prot":2} ] ,
            "autres" : []
            }
        }

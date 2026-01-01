#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 18 20:34:51 2025

@author: Drayen
"""

from rich import print as cstmprint

def cstminput(*args , sep = "" , end = "") :
    cstmprint(*args , sep = sep , end = " ")
    return input(end)

def Error(error="Error",msg="an error occured") :
    cstmprint(f"[bold red]{error}[/bold red] : ",end="")
    print(msg)

def PrintMsg(*args) :
    for i in range(len(args)-1) :
        if type(args[i]) == tuple or type(args[i]) == list :
            cstm_print = bool(args[i][1])  # l'info à afficher est un tuple / une liste dont l'indice indique si on veut un custom print ou non (1 => oui)
            index = True # indique si l'élément en cours est un tuple ou une liste
        else :
            index = False
            cstm_print = False

        if index :
            if cstm_print :
                cstmprint(args[i][0],end="")
            else :
                print(args[i][0],end="")
        else :
            if cstm_print :
                cstmprint(args[i],end="")
            else :
                print(args[i],end="")

    if type(args[-1]) == tuple or type(args[-1]) == list :
        cstm_print = bool(args[-1][1])
        index = True
    else :
        index = False
        cstm_print = False

    if index :
        if cstm_print :
            cstmprint(args[-1][0])
        else :
            print(args[-1][0])
    else :
        if cstm_print :
            cstmprint(args[-1])
        else :
            print(args[-1])

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 25 18:28:46 2025

@author: Drayen
"""
from pyjdr.Messages import Error

def remplacement_input_pour_faute_frappe(inp,L_ref) :
    print(f"\tvotre réponse '{inp}' n'est pas dans dans la liste de référence, \n"
          "\tvoici des éléments correspondant à ce que vous cherchez :")
    for i in range(len(L_ref)) :
        print(f"\t\t{i}) {L_ref[i]}")

    L_ref.append(inp)

    while True :
        inp = input("\tsélectionnez l'élément que vous cherchez (son numéro), n si aucun ne correspond : ")
        if inp == "n" :
            print("")
            return L_ref[-1]
        if inp.isdigit() and int(inp) < len(L_ref):
            print("")
            return L_ref[int(inp)]
        Error("ValueError",f"unknown index '{inp}'")


def detection_fautes_frappe(string : str , L_ref : list) -> list :
    if L_ref == [] :
        return string
    R = []

    for i in range(len(L_ref)) :
        R.append( ( L_ref[i],  LongestCommonSubsequence(string , L_ref[i]) ) )

    min_ref = 0
    for e in R :
        min_ref += e[1]
    min_ref = max(min_ref / len(R) , 10)

    R.sort(key=lambda x: x[1])
    return [ e[0] for e in R if e[1] >= min_ref ]



def LongestCommonSubsequence(string_1: str, string_2: str) -> float:
    if "" in (string_1,string_2) :
        if string_1 == string_2 :
            return 1.0
        return 0.0

    m, n = len(string_1), len(string_2)
    L_LCS = [[0] * (n + 1) for _ in range(m + 1)]

    # Remplissage de la table de programmation dynamique
    for i in range(1, m + 1):
        for j in range(1, n + 1):

            if string_1[i - 1] == string_2[j - 1]:
                L_LCS[i][j] = L_LCS[i - 1][j - 1] + 1
            else:
                L_LCS[i][j] = max(L_LCS[i - 1][j], L_LCS[i][j - 1])

    # L_LCS[m][n] est la longueur de LCS
    L_LCS = L_LCS[m][n] # L pour len et non plus list, c'est la long de la plus grde LCS
    return ( 2*L_LCS ) / ( len(string_1) + len(string_2) )



def normalize(string : str, L_ref : list = [], inp_name : str = "latest") -> str :
    """


    Parameters
    ----------
    string : str
        just a string
    L_ref : list, optional
        a list with the words you want to compare with string in order to detect mistakes
        The default is [], it does nothing in that case.
    inp_name : str, optional
        DESCRIPTION. The default is "latest".

    Returns
    -------
    str
        A normalized string of characters, in the ASCII table, with spaces replaced by underscores.
        Then, typo detection.

    """

    normalisation = {
    "a": "a", "b": "b", "c": "c", "d": "d", "e": "e", "f": "f", "g": "g",
    "h": "h", "i": "i", "j": "j", "k": "k", "l": "l", "m": "m", "n": "n",
    "o": "o", "p": "p", "q": "q", "r": "r", "s": "s", "t": "t", "u": "u",
    "v": "v", "w": "w", "x": "x", "y": "y", "z": "z",

    "A": "a", "B": "b", "C": "c", "D": "d", "E": "e", "F": "f", "G": "g",
    "H": "h", "I": "i", "J": "j", "K": "k", "L": "l", "M": "m", "N": "n",
    "O": "o", "P": "p", "Q": "q", "R": "r", "S": "s", "T": "t", "U": "u",
    "V": "v", "W": "w", "X": "x", "Y": "y", "Z": "z",

    "é": "e", "è": "e", "ê": "e", "ë": "e",
    "à": "a", "â": "a", "ä": "a",
    "î": "i", "ï": "i",
    "ù": "u", "û": "u", "ü": "u",
    "ô": "o", "ö": "o",
    "ç": "c",

    "É": "e", "È": "e", "Ê": "e", "Ë": "e",
    "À": "a", "Â": "a", "Ä": "a",
    "Î": "i", "Ï": "i",
    "Ù": "u", "Û": "u", "Ü": "u",
    "Ô": "o", "Ö": "o",
    "Ç": "c",

    "0": "0", "1": "1", "2": "2", "3": "3", "4": "4",
    "5": "5", "6": "6", "7": "7", "8": "8", "9": "9",

    " ": "_", "-": "_", "/": "_", "\\": "_","_":"_",

    "!": "", "?": "", ".": "", ",": "", "'": "", "\"": "",
    ":": "", ";": "", "(": "", ")": "", "[": "", "]": "",
    "{": "", "}": "", "@": "", "#": "", "$": "", "%": "",
    "&": "", "*": "", "+": "", "=": "", "<": "", ">": "",
    "|": "", "`": "", "~": "", "^": "", "°": "",

    "€": "", "£": "", "¥": "", "©": "", "®": "", "™": "",
    "§": "", "¤": "", "µ": ""
}
    string = list(string)
    for i in range(len(string)) :
        ch = normalisation.get(string[i])
        if ch :
            string[i] = ch
        else :
            string[i] = ""

    res = ""
    for e in string :
        res = res + e

    if L_ref != [] and not res in L_ref :
        Error("ValueError",f"unknown value '{res}' for input : '{inp_name}', maybe you made a typing mistake")
        L_ref = detection_fautes_frappe(res,L_ref)
        res = remplacement_input_pour_faute_frappe(res, L_ref)


    return res

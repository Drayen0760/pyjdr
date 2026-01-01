#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  4 12:25:38 2025

@author: jasta
"""
import json
from pyjdr.str_op import normalize

with open("tad_fr-en/img_to_html.json","r") as file :
    dic = json.load(file)

en_to_fr = { normalize(en.split("-modified")[0]) : normalize(fr.split(".")[0]) for en,fr in dic.items() }

# inversion du dico

fr_to_en = { fr : en for en,fr in en_to_fr.items() }

with open("tad_fr-en/en_to_fr.json","w") as file :
    json.dump(en_to_fr,file)

with open("tad_fr-en/fr_to_en.json","w") as file :
    json.dump(fr_to_en,file)

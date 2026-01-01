#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 18 21:54:23 2025

@author: Drayen
"""
from random import randint

def Roll(dice) :
    res = 0
    if dice[1] == 10 :
        for i in range(dice[0]) :
            res += randint(0, 9)
    else :
        for i in range(dice[0]) :
            res += randint(1, dice[1])
    return res

def Roll_liste(dice) :
    res = []
    if dice[1] == 10 :
        for i in range(dice[0]) :
            res.append(randint(0, 9))
    else :
        for i in range(dice[0]) :
            res.append(randint(1, dice[1]))
    return res

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 18 20:34:51 2025

@author: Drayen
"""

def check_PyJDR_deps() :
    deps_first = [ "os" , "site" , "random", "math" , "matplotlib.pyplot" , "pickle" , "json" , "rich" , "pygame" ]
    to_install = []
    deps_extract_monster = [ "bs4" , "pathlib" , "re" ]
    deps_PyJDR_file = []
    # TODO
    raise_import_error = False

    for e in deps_first :
        try :
            exec( f"import {e}" )
        except ImportError :
            print(f"cannot import import modul '{e}'")
            to_install.append(e)
            raise_import_error = True

    if "rich" in to_install :
        print("you can install the rich module by downloading the 'rich' folder from their github ( https://github.com/Textualize/rich ) and putting it in your python path")
        inp = input("do you want to install it ? (o/n)").lower()
        if inp == "o" :
            from pyjdr.Check.ModuleInstaller.WithGit import githubinstall
            toprint = input("affichage des détails de l'installation ? (o/n)").lower() == "o"
            print("intallation...",end="")
            githubinstall("https://github.com/Textualize/rich","rich",["rich"],print_installation_details=toprint)
            try :
                import rich
                rich.print("[green]REUSSI !![/green]")
            except (ImportError, ModuleNotFoundError) as e:
                print("RATEE !!")
                raise e

    if raise_import_error :
        print(f"You have to install the module(s) {to_install}")
        inp = input("do you want to install it/them ? (o/n)").lower()
        if inp == "o" :
            from pyjdr.Check.ModuleInstaller.WithPip import pipinstall
            for mod in to_install :
                if mod != "rich" :
                    pipinstall(mod)

    return True

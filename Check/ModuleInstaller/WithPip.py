#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 18 20:34:51 2025

@author: Drayen
"""

import subprocess
from pyjdr.Check.ModuleInstaller.GetOs import get_os


def pipinstall(module , operatingsystem : str = None) :
    if operatingsystem is None :
        operatingsystem = get_os()
    out = None

    try :
        if operatingsystem == "linux" :
            out = subprocess.run(f"pip install --user {module} --break-system-packages" ,
                                 shell=True , text=True ,
                                 stdout=subprocess.PIPE , stderr=subprocess.PIPE )
        else :
            out = subprocess.run( f"pip install --user {module}" ,
                                 shell=True , text=True ,
                                 stdout=subprocess.PIPE , stderr=subprocess.PIPE )

        if out.stderr :
            raise ModulInstallationError(out.stderr)

    except Exception as e:
        print(f"an Error occured when trying to install '{module}' : \n{e} \n")
    print(f"details : \n{out.stdout}")


def install_list(lst : list , operatingsystem : str = None):
    if operatingsystem is None :
        operatingsystem = get_os()

    for mod in lst :
        pipinstall(mod, operatingsystem)

class ModulInstallationError(Exception) :
    def __init__(self, message):
        self.message = message

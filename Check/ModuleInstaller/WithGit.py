#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 18 20:34:51 2025

@author: Drayen
"""
import subprocess
from site import getusersitepackages
from shutil import move

from pyjdr.Check.ModuleInstaller.GetOs import get_os

def githubinstall(url : str ,
                  module_name : str ,
                  files_or_folders_to_load : list = [] ,
                  operatingsystem : str = None ,
                  print_installation_details : bool = False) :
    """


    Parameters
    ----------
    url : str
        the github url.
    module_name : str
        the name of the github main branch and the one of the module in your path.
    files_or_folders_to_load : list, optional
        the files and folders you want to be in your module.
        The default is [], it means that all the github elements will be placed in module.
    operatingsystem : str, optional
        DESCRIPTION. The default is None.

    Returns
    -------
    None.

    """
    if operatingsystem is None :
        operatingsystem = get_os()

    #%% linux
    if operatingsystem in ("linux","macos "):
        if len(files_or_folders_to_load) == 1  or files_or_folders_to_load == [] :
            create_global_dir = False
        else :
            create_global_dir = True

        module_path = getusersitepackages()

        temp_path = "/tmp/"

        if print_installation_details :
            print("OS : ",operatingsystem,"\n"
                "module path : ",module_path,"\n"
                "temp path : ",temp_path,"\n"
                )

        #%%% git clone
        print("chargement depuis github...")

        out_git_clone = subprocess.run( f"cd {temp_path} && git clone {url}" ,
                             shell=True , text=True ,
                             stdout=subprocess.PIPE , stderr=subprocess.PIPE )
        if out_git_clone.stderr and out_git_clone.stderr != f"Clonage dans '{module_name}'...\n" :
            raise GitInstallationError(f"an error occured when downloading the module references from {url}, \ndetails : \n{out_git_clone.stderr}")

        elif out_git_clone.stderr != "Clonage dans 'rich'...\n" :
            out_git_clone = out_git_clone.stdout
        temp_path = temp_path + module_name

        #%%% mkdir
        if create_global_dir :
            print("creation du dossier du module...")
            out_mkdir = subprocess.run( f"mkdir {module_path+module_name+'/'}" ,
                                 shell=True , text=True ,
                                 stdout=subprocess.PIPE , stderr=subprocess.PIPE )
            if out_mkdir.stderr :
                raise GitInstallationError(f"an error occured when creating the module directory : {module_name} at {module_path} \ndetails : \n{out_mkdir.stderr}")
            out_mkdir = out_mkdir.stdout
            module_path = module_path + "/" + module_name
        else :
            out_mkdir = "we don't need to create a new folder"

        #%%% move files and folders
        print("déplacement des éléments du module...")
        try :
            if files_or_folders_to_load == [] :
                move( temp_path , module_path)
            else :
                for element in files_or_folders_to_load :
                    print(temp_path,element)
                    print(module_path)
                    move( temp_path + "/" + element , module_path)

            out_move = f"done in {module_path}"
        except Exception as e :
            out_move = e
            raise GitInstallationError(f"an error occured when moving the elements in the path \ndetails : \n{out_move}")

        #%%% recap
        if print_installation_details :
            print( "out_git_clone" , " : \n\t" , out_git_clone , "\n\n" )
            print( "out_mkdir" , " : \n\t" , out_mkdir , "\n\n" )
            print( "out_move" , " : \n\t" , out_move , "\n\n" )

    #%% TODO : windows
    else :
        # TODO
        print(f"not implemented yet for {operatingsystem}")

#%% GitInstallationError
class GitInstallationError(Exception) :
    def __init__(self,message) :
        self.message = message

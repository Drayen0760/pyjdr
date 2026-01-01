#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 27 16:03:26 2025

@author: jasta
"""
import os
import sys

def get_os () :
    if os.name == "posix": # Linux + MacOs
        if sys.platform == "darwin": # Macos
            return "macos"
        else: #Linux
            return "linux"
    else: # Windows
        return "windows"

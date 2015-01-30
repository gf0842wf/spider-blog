# -*- coding: utf-8 -*-
import os, sys

HOME_DIR = os.path.dirname(os.path.abspath(__file__))
PYPATH = os.path.split(HOME_DIR)[0]

def init_path():
    sys.path.append(PYPATH)
    

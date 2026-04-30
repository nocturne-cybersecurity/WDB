import sys
import time
import pyfiglet
import subprocess
import sqlite3 as sql
from pathlib import Path
from rich.panel import Panel
from colorama import Fore, init
from rich.console import Console
import CRUD

def Banner():
    print(Fore.BLUE + r"""
 ___       __   ________  ________     
|\  \     |\  \|\   ___ \|\   __  \    
\ \  \    \ \  \ \  \_\\ \ \  \|\ /_   
 \ \  \  __\ \  \ \  \_\\ \ \   __  \  
  \ \  \|\__\_\  \ \  \_\\ \ \  \|\  \ 
   \ \____________\ \_______\ \_______\
    \|____________|\|_______|\|_______|                                                                      
        """)

def start():
    Banner()
    CRUD.CRUD()
    
start()

import os
import sqlite3
from core.utilities import tools

def menu_view():
    while True:
        tools.clear_screen()
        tools.conexao_db()
        tools.header('PASSWORDS')

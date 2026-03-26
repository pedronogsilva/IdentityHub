import os
import sqlite3
from core.utilities import tools

def password_view():
    """Display paginated list of websites with navigation options."""
    connection, cursor = tools.conexao_db()
    PAGE_SIZE = 10
    current_page = 0

    while True:
        tools.clear_screen()
        tools.conexao_db()
        tools.header('PASSWORDS')

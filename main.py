import os
import sqlite3
from core.utilities import tools
from core.services import website_service
from core.services import manager_service
from core.services import password_service

while True:
    tools.clear_screen()
    connection, cursor = tools.conexao_db()
    tools.create_table(connection, cursor)
    option = tools.main_menu()

    if option == "1":
        website_service.website_view()
    elif option == "2":
        manager_service.menu_view()
    elif option == "3":
        password_service.menu_view()
    elif option == "4":
        exit()
    else:
        input("    Invalid option. Press ENTER to retry...");
        continue
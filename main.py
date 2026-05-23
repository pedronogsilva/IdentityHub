import os
import sqlite3
from core.utilities import tools
from core.services import website_service
from core.services import manager_service

while True:
    connection, cursor = tools.conexao_db()
    tools.create_table(connection, cursor)
    tools.clear_screen()
    option = tools.main_menu()

    if option == "1":
        website_service.website_view()
    elif option == "2":
        manager_service.manager_view()
    elif option == "3":
        exit()
    else:
        input("    Invalid option. Press ENTER to retry...");
        continue
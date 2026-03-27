import os
import sqlite3
import hashlib
from core.utilities import tools


def manager_view():
    """Display paginated list of websites with navigation options."""
    connection, cursor = tools.conexao_db()
    PAGE_SIZE = 10
    current_page = 0

    while True:
        tools.clear_screen()
        tools.header('MANAGER')

        cursor.execute('''SELECT id, website_id, username, email, password_encrypted, created_at FROM credential ORDER BY website_id ASC''')
        all_manager = cursor.fetchall()
        total_records = len(all_manager)

        # Pagination slicing
        start_index = current_page * PAGE_SIZE
        end_index = start_index + PAGE_SIZE
        page_records = all_manager[start_index:end_index]

        # Show table of database websites
        line_length = 138
        print("─" * line_length)
        print(f"│ {'WEBSITE':<22} │ {'USERNAME':<25} │ {'EMAIL':<30} │ {'PASSWORD':<25} │ {'CREATION DATE':^20} │")
        print("─" * line_length)

        if not all_manager:
            print("│", " " * 41, "No websites found on database..", " " * 60, "│")
            print("─" * line_length)

        #  Print current page records
        for id_, website, username, email, password, created_at in page_records:
            password_decrypted = tools.decrypt_password(password)
            print(f"│ {website:<22} │ {username:<25} │ {email:<30} │ {password_decrypted:<25} │ {created_at:^20} │")
            print("─" * line_length)

        # User options
        print(f"\n   \033[38;5;99mPage {current_page+1} / "
            f"{((total_records-1)//PAGE_SIZE)+1 if total_records else 1}\033[0m"
            "\n\n   \033[38;5;99m1.\033[0m Create a Password"
            "   \033[38;5;99m2.\033[0m Edit Password"
            "   \033[38;5;99m3.\033[0m Previous Page"
            "   \033[38;5;99m4.\033[0m Next Page"
            "   \033[38;5;99m5.\033[0m Main Menu\n")

        # Choice user in menu
        option = input("""   \033[90mSelect option > \033[0m""");

        if option == "1":
            manager_add()
        elif option == "2": 
            input()
        elif option == "3":
            if current_page > 0: 
                current_page -= 1
        elif option == "4":
            if end_index < total_records: 
                current_page += 1
            else: 
                input("    Already at the last page. Press ENTER to retry...")
        elif option == "5":
            # Close database
            connection.close()
            return
        else: 
            input("    Invalid option. Press ENTER to retry...")
            continue


def manager_add():
    """Display paginated and questions add website."""
    connection, cursor = tools.conexao_db()

    # Select website
    selected = select_website_add()
    if not selected:
        print(" " * 41, "No websites found on database..")
        return
    selected_id, selected_website, selected_url = selected
    
    # Collect username and email
    manager_username = input("\n   What´s the username of the website?\n   \033[90mWrite an option > \033[0m ")
    manager_email = input("\n   What´s the email of the website?\n   \033[90mWrite an option > \033[0m ")
    
    if not manager_username and not manager_email:
        input("    You must provide at least user OR email. Press ENTER...")
        connection.close()
        return
    
    manager_password = input("\n   What´s the password of the website?\n   \033[90mWrite an option > \033[0m ")
    if not manager_password:
        input("    Password is required. Press ENTER...")
        return
    
    # Fernet password
    password_encrypted = tools.encrypt_password(manager_password)

    # Insert into database
    try:
        cursor.execute('''INSERT INTO credential (website_id, username, email, password_encrypted) VALUES (?, ?, ?, ?)''', (selected_id, manager_username, manager_email, password_encrypted))
        connection.commit()
    except Exception as e:
        input(f"    Error: {e}")
    finally:
        connection.close()

def select_website_add():
    """Display paginated and questions add website."""
    connection, cursor = tools.conexao_db()
    PAGE_SIZE = 10
    current_page = 0

    while True:
        tools.clear_screen()
        tools.header('MANAGER')

        cursor.execute('''SELECT id, website, url FROM website ORDER BY website ASC''')
        all_manager_add = cursor.fetchall()
        total_records = len(all_manager_add)

        # Pagination slicing
        start_index = current_page * PAGE_SIZE
        end_index = start_index + PAGE_SIZE
        page_records = all_manager_add[start_index:end_index]

        if not all_manager_add:
            print(" " * 41, "No websites found on database..")

        for i, (id_, website, url) in enumerate(page_records, start=1):
            print(f"{i}.: {website}")

        # User options
        print(f"\n   \033[38;5;99mPage {current_page+1} / "
            f"{((total_records-1)//PAGE_SIZE)+1 if total_records else 1}\033[0m"
            "\n\n   \033[38;5;99m11.\033[0m Previous Page"
            "   \033[38;5;99m12.\033[0m Next Page"
            "   \033[38;5;99m13.\033[0m Return Menu\n")

        # Choice user in menu
        option = input("""   \033[90mSelect option > \033[0m""");

        if option == "11":
            if current_page > 0: 
                current_page -= 1
        elif option == "12":
            if end_index < total_records:
                current_page += 1
            else: 
                input("    Already at the last page. Press ENTER to retry...")
        elif option == "13":
            # Close database
            connection.close()
            return None
        # Options of select by user
        elif option.isdigit():
            option = int(option)
            if 1 <= option <= len(page_records):
                id_, website, url = page_records[option - 1]
                connection.close()
                return id_, website, url
        else: 
            input("    Invalid option. Press ENTER to retry...")
            continue
import sqlite3
from core.utilities import tools


def manager_view():
    """Display paginated list of credentials with navigation options."""
    connection, cursor = tools.conexao_db()
    PAGE_SIZE = 10
    current_page = 0

    while True:
        tools.clear_screen()
        tools.header('MANAGER')

        cursor.execute('''
            SELECT c.id, c.website_id, c.username, c.email,
                   c.password_encrypted, c.credential_salt, c.created_at,
                   w.website, w.url, w.created_at
            FROM credential c
            JOIN website w ON c.website_id = w.id
            ORDER BY w.website ASC
        ''')
        all_manager = cursor.fetchall()
        total_records = len(all_manager)

        # Pagination slicing
        start_index = current_page * PAGE_SIZE
        end_index = start_index + PAGE_SIZE
        page_records = all_manager[start_index:end_index]

        # Show table
        line_length = 138
        print("─" * line_length)
        print(f"│ {'#':<4} │ {'WEBSITE':<20} │ {'USERNAME':<22} │ {'EMAIL':<28} │ {'PASSWORD':<25} │ {'CREATION DATE':^20} │")
        print("─" * line_length)

        if not all_manager:
            print("│", " " * 41, "No credentials found on database..", " " * 57, "│")
            print("─" * line_length)

        # Print current page records — desencripta password antes de mostrar
        for row in page_records:
            cred_id, website_id_val, username, email, password_enc, cred_salt, created_at_cred, website_name, website_url, website_created_at = row

            try:
                key = tools.derive_key(website_name, website_url, cred_salt, website_created_at)
                password_show = tools.decrypt_password(password_enc, key)
            except Exception:
                password_show = "[erro ao desencriptar]"

            print(f"│ {cred_id:<4} │ {website_name:<20} │ {username:<22} │ {email:<28} │ {password_show:<25} │ {created_at_cred:^20} │")
            print("─" * line_length)

        # User options
        print(f"\n   \033[38;5;99mPage {current_page+1} / "
            f"{((total_records-1)//PAGE_SIZE)+1 if total_records else 1}\033[0m"
            "\n\n   \033[38;5;99m1.\033[0m Create"
            "   \033[38;5;99m2.\033[0m Edit"
            "   \033[38;5;99m3.\033[0m Delete"
            "   \033[38;5;99m4.\033[0m Previous Page"
            "   \033[38;5;99m5.\033[0m Next Page"
            "   \033[38;5;99m6.\033[0m Main Menu\n")

        option = input("""   \033[90mSelect option > \033[0m""")

        if option == "1":
            manager_add()
        elif option == "2":
            manager_edit(cursor)
        elif option == "3":
            manager_delete()
        elif option == "4":
            if current_page > 0:
                current_page -= 1
        elif option == "5":
            if end_index < total_records:
                current_page += 1
            else:
                input("    Already at the last page. Press ENTER to retry...")
        elif option == "6":
            connection.close()
            return
        else:
            input("    Invalid option. Press ENTER to retry...")
            continue


def manager_add():
    """Collect data and insert a new encrypted credential."""
    connection, cursor = tools.conexao_db()

    # Select website
    selected = select_website_add()
    if not selected:
        return
    selected_id, selected_website, selected_url, selected_created_at = selected

    # Collect username and email
    manager_username = input("\n   What´s the username of the website?\n   \033[90mWrite an option > \033[0m ")
    manager_email    = input("\n   What´s the email of the website?\n   \033[90mWrite an option > \033[0m ")

    if not manager_username and not manager_email:
        input("    You must provide at least user OR email. Press ENTER...")
        connection.close()
        return

    manager_password = input("\n   What´s the password of the website?\n   \033[90mWrite an option > \033[0m ")
    if not manager_password:
        input("    Password is required. Press ENTER...")
        connection.close()
        return

    # Gerar salt único e imutável para esta credencial
    cred_salt = tools.generate_salt()

    # Derivar chave a partir de campos imutáveis e encriptar
    try:
        key = tools.derive_key(selected_website, selected_url, cred_salt, selected_created_at)
        password_encrypted = tools.encrypt_password(manager_password, key)
    except Exception as e:
        input(f"    Error encrypting password: {e}. Press ENTER...")
        connection.close()
        return

    # Insert into database
    try:
        cursor.execute(
            '''INSERT INTO credential (website_id, username, email, password_encrypted, credential_salt)
               VALUES (?, ?, ?, ?, ?)''',
            (selected_id, manager_username, manager_email, password_encrypted, cred_salt)
        )
        connection.commit()
    except Exception as e:
        input(f"    Error: {e}. Press ENTER...")
    finally:
        connection.close()


def manager_edit(cursor_view):
    """Edit username, email or password of an existing credential."""
    connection, cursor = tools.conexao_db()

    cred_id_input = input("\n   Insert the credential # to edit:\n   \033[90mWrite an option > \033[0m ")
    if not cred_id_input.isdigit():
        input("    Invalid option. Press ENTER to retry...")
        connection.close()
        return

    # Buscar credencial completa com dados do website
    cursor.execute('''
        SELECT c.id, c.username, c.email, c.password_encrypted, c.credential_salt,
               w.website, w.url, w.created_at
        FROM credential c
        JOIN website w ON c.website_id = w.id
        WHERE c.id = ?
    ''', (int(cred_id_input),))
    row = cursor.fetchone()

    if not row:
        input("    Credential not found. Press ENTER to retry...")
        connection.close()
        return

    cred_id, old_username, old_email, password_enc, cred_salt, website_name, website_url, website_created_at = row

    while True:
        tools.clear_screen()
        tools.header('MANAGER — EDIT')

        print(f"   Editing credential \033[38;5;99m#{cred_id}\033[0m — {website_name}\n")
        print(f"   \033[38;5;99m1.\033[0m Edit Username   (current: {old_username})")
        print(f"   \033[38;5;99m2.\033[0m Edit Email      (current: {old_email})")
        print(f"   \033[38;5;99m3.\033[0m Edit Password")
        print(f"   \033[38;5;99m4.\033[0m Back\n")

        option = input("   \033[90mSelect option > \033[0m")

        if option == "1":
            new_value = input("\n   New username:\n   \033[90mWrite an option > \033[0m ")
            if not new_value:
                input("    Invalid option. Press ENTER to retry...")
                continue
            try:
                cursor.execute("UPDATE credential SET username = ? WHERE id = ?", (new_value, cred_id))
                connection.commit()
                old_username = new_value
                input("    Username updated. Press ENTER to continue...")
            except Exception as e:
                input(f"    Error: {e}. Press ENTER...")

        elif option == "2":
            new_value = input("\n   New email:\n   \033[90mWrite an option > \033[0m ")
            if not new_value:
                input("    Invalid option. Press ENTER to retry...")
                continue
            try:
                cursor.execute("UPDATE credential SET email = ? WHERE id = ?", (new_value, cred_id))
                connection.commit()
                old_email = new_value
                input("    Email updated. Press ENTER to continue...")
            except Exception as e:
                input(f"    Error: {e}. Press ENTER...")

        elif option == "3":
            new_password = input("\n   New password:\n   \033[90mWrite an option > \033[0m ")
            if not new_password:
                input("    Password is required. Press ENTER to retry...")
                continue
            # A chave é sempre derivada dos campos imutáveis — não precisa re-encriptar com chave antiga
            try:
                key = tools.derive_key(website_name, website_url, cred_salt, website_created_at)
                new_enc = tools.encrypt_password(new_password, key)
                cursor.execute("UPDATE credential SET password_encrypted = ? WHERE id = ?", (new_enc, cred_id))
                connection.commit()
                password_enc = new_enc
                input("    Password updated. Press ENTER to continue...")
            except Exception as e:
                input(f"    Error: {e}. Press ENTER...")

        elif option == "4":
            connection.close()
            return
        else:
            input("    Invalid option. Press ENTER to retry...")


def manager_delete():
    """Delete a credential permanently after confirmation."""
    connection, cursor = tools.conexao_db()

    cred_id_input = input("\n   Insert the credential # to delete:\n   \033[90mWrite an option > \033[0m ")
    if not cred_id_input.isdigit():
        input("    Invalid option. Press ENTER to retry...")
        connection.close()
        return

    # Verificar se existe
    cursor.execute('''
        SELECT c.id, c.username, c.email, w.website
        FROM credential c
        JOIN website w ON c.website_id = w.id
        WHERE c.id = ?
    ''', (int(cred_id_input),))
    row = cursor.fetchone()

    if not row:
        input("    Credential not found. Press ENTER to retry...")
        connection.close()
        return

    cred_id, username, email, website_name = row

    # Confirmação antes de apagar
    print(f"\n   \033[31mAre you sure you want to delete?\033[0m")
    print(f"   Website: {website_name} | Username: {username} | Email: {email}")
    confirm = input("\n   \033[90mType 'yes' to confirm > \033[0m ")

    if confirm.strip().lower() != "yes":
        input("    Deletion cancelled. Press ENTER to continue...")
        connection.close()
        return

    try:
        cursor.execute("DELETE FROM credential WHERE id = ?", (cred_id,))
        connection.commit()
        input("    Credential deleted. Press ENTER to continue...")
    except Exception as e:
        input(f"    Error: {e}. Press ENTER...")
    finally:
        connection.close()


def select_website_add():
    """Display paginated list of websites and return the selected one."""
    connection, cursor = tools.conexao_db()
    PAGE_SIZE = 10
    current_page = 0

    while True:
        tools.clear_screen()
        tools.header('MANAGER — SELECT WEBSITE')

        cursor.execute('''SELECT id, website, url, created_at FROM website ORDER BY website ASC''')
        all_websites = cursor.fetchall()
        total_records = len(all_websites)

        # Pagination slicing
        start_index = current_page * PAGE_SIZE
        end_index = start_index + PAGE_SIZE
        page_records = all_websites[start_index:end_index]

        if not all_websites:
            print(" " * 41, "No websites found on database..")

        for i, (id_, website, url, created_at) in enumerate(page_records, start=1):
            print(f"   {i}.: {website}  \033[90m({url})\033[0m")

        # User options
        print(f"\n   \033[38;5;99mPage {current_page+1} / "
            f"{((total_records-1)//PAGE_SIZE)+1 if total_records else 1}\033[0m"
            "\n\n   \033[38;5;99m11.\033[0m Previous Page"
            "   \033[38;5;99m12.\033[0m Next Page"
            "   \033[38;5;99m13.\033[0m Return Menu\n")

        option = input("""   \033[90mSelect option > \033[0m""")

        if option == "11":
            if current_page > 0:
                current_page -= 1
        elif option == "12":
            if end_index < total_records:
                current_page += 1
            else:
                input("    Already at the last page. Press ENTER to retry...")
        elif option == "13":
            connection.close()
            return None
        elif option.isdigit():
            option = int(option)
            if 1 <= option <= len(page_records):
                id_, website, url, created_at = page_records[option - 1]
                connection.close()
                return id_, website, url, created_at
        else:
            input("    Invalid option. Press ENTER to retry...")
            continue

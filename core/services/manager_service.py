import os
import sqlite3
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
            print(f"│ {website:<22} │ {username:<25} │ {email:<30} │ {password:<25} │ {created_at:^20} │")
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
            input()
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
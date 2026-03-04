import os
import sqlite3
from core.utilities import tools

def website_view():
    """Display paginated list of websites with navigation options."""
    connection, cursor = tools.conexao_db()
    PAGE_SIZE = 10
    current_page = 0

    while True:
        tools.clear_screen()
        tools.header('WEBSITES')

        cursor.execute('''SELECT id, website, url, created_at FROM website ORDER BY website ASC''')
        all_websites = cursor.fetchall()
        total_records = len(all_websites)

        # Pagination slicing
        start_index = current_page * PAGE_SIZE
        end_index = start_index + PAGE_SIZE
        page_records = all_websites[start_index:end_index]

        # Show table of database websites
        line_length = 138
        print("─" * line_length)
        print(f"│ {'WEBSITE':<35} │ {'URL':<73} │ {'CREATION DATE':^20} │")
        print("─" * line_length)

        if not all_websites:
            print("│", " " * 41, "No websites found on database..", " " * 60, "│")
            print("─" * line_length)

        #  Print current page records
        for id_, website, url, created_at in page_records:
            print(f"│ {website:<35} │ {url:<73} │ {created_at:^20} │")
            print("─" * line_length)

        # User options
        print(f"\n   \033[38;5;99mPage {current_page+1} / "
            f"{((total_records-1)//PAGE_SIZE)+1 if total_records else 1}\033[0m"
            "\n\n   \033[38;5;99m1.\033[0m Create a Website"
            "   \033[38;5;99m2.\033[0m Edit Website"
            "   \033[38;5;99m3.\033[0m Previous Page"
            "   \033[38;5;99m4.\033[0m Next Page"
            "   \033[38;5;99m5.\033[0m Main Menu\n")
        
        # Choice user in menu
        option = input("""   \033[90mSelect option > \033[0m""");

        if option == "1":
            website_add()
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


def website_add():
    """Display paginated add website."""
    connection, cursor = tools.conexao_db()

    # Collect site name
    website_name = input("\n   What´s the name of the website?\n   \033[90mWrite an option > \033[0m ").title()
    if not website_name:
        input("    Invalid option. Press ENTER to retry...")
        return

    # Collect url website
    website_url = input("\n   What´s the url of the website?\n   \033[90mWrite an option > \033[0m ")
    if not website_url:
        website_url = "No URL provided."

    # Insert into database
    try:
        cursor.execute("""INSERT INTO website (website, url) VALUES (?, ?)""",(website_name, website_url))
        connection.commit()
    except sqlite3.IntegrityError:
        connection.rollback()
        input(f"\n   \033[31mError:\033[0m The website '{website_name}' already exist. Press ENTER to retry...")

    # Close database
    connection.close()
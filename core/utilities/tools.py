import os
import sqlite3
from datetime import datetime
from pathlib import Path



def clear_screen():
    """Clear console screen."""

    # Check if the system name contains 'nt'; if it does, execute the first command; otherwise, execute the second.
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # macOS / Linux
        os.system('clear')


def conexao_db(db_name="identityhub.db"):
    """Ensure database directory exists and return connection + cursor."""

    # Check if the directory exists; if not, create it, along with the database.
    db_folder = Path("data")

    try:
        db_folder.mkdir(exist_ok=True)
    except PermissionError:
        print(f"Error: No permisson to create the folder '{db_folder}'.")
    except Exception as e:
        print(f"Unexpected error to crete folder '{db_folder}': {e}")

    db_path = db_folder / db_name

    try:
        # Make the connection with database.
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        return connection, cursor
    except sqlite3.OperationalError as e:
        print(f"Errot to connection the database '{db_path}': {e}")
        return None
    except Exception as e:
        print(f"Unexpected error to open the database '{db_path}': {e}")
        return None


def create_table(connection, cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS website (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        website TEXT UNIQUE COLLATE NOCASE NOT NULL,
        url TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS credential (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        website_id INTEGER NOT NULL,
        username TEXT,
        email TEXT,
        password_encrypted TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME,
        FOREIGN KEY (website_id) REFERENCES website(id))''')


def header(title):
    """Dynamic header for multiple tabs {Only need to define the title on call}"""

    # Line of the Header
    line_length = 138
    print("─" * line_length)

    # Line of Date/Time
    dt_line = f"\033[38;5;99mDate/Time:\033[0m {datetime.now().strftime('%d-%m-%y %H:%M')}"
    space_dt = (line_length - len(dt_line)) // 2
    print(" " * space_dt + dt_line)
    
    # Line of Title
    t_line = f"\033[38;5;99m{title}\033[0m"
    space_t = (line_length - len(t_line)) // 2
    print(" " * space_t + t_line)
    print()


def main_menu():
    print("""\033[38;5;51m
  ██╗ ██████╗  ███████╗ ███╗   ██╗ ████████╗ ██╗ ████████╗ ██╗   ██╗
  ██║ ██╔══██╗ ██╔════╝ ████╗  ██║ ╚══██╔══╝ ██║ ╚══██╔══╝ ╚██╗ ██╔╝
  ██║ ██║  ██║ █████╗   ██╔██╗ ██║    ██║    ██║    ██║     ╚████╔╝ 
  ██║ ██║  ██║ ██╔══╝   ██║╚██╗██║    ██║    ██║    ██║      ╚██╔╝  
  ██║ ██████╔╝ ███████╗ ██║ ╚████║    ██║    ██║    ██║       ██║   
  ╚═╝ ╚═════╝  ╚══════╝ ╚═╝  ╚═══╝    ╚═╝    ╚═╝    ╚═╝       ╚═╝   
                   H U B  -  P A S S W O R D\033[0m  

\033[90m─────────────────────────────────────────────────────────────────────\033[0m
\033[38;5;46m    SYSTEM STATUS:\033[0m READY
\033[38;5;244m─────────────────────────────────────────────────────────────────────\033[0m

      \033[38;5;99m[1]\033[0m  🌐  Websites
      \033[38;5;99m[2]\033[0m  🗂  Manager
      \033[38;5;99m[3]\033[0m  🔐  Passwords
      \033[38;5;99m[4]\033[0m  🚪  Exit

\033[38;5;244m─────────────────────────────────────────────────────────────────────\033[0m
""");
    option = input("""   \033[90mSelect option > \033[0m""");
    return option;
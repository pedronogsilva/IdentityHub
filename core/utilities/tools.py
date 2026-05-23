import os
import uuid
import sqlite3
import hashlib
import base64
from datetime import datetime
from pathlib import Path
from cryptography.fernet import Fernet



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
        credential_salt TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (website_id) REFERENCES website(id))''')

    # Migração segura: adiciona credential_salt se a tabela já existia sem ela
    try:
        cursor.execute("ALTER TABLE credential ADD COLUMN credential_salt TEXT NOT NULL DEFAULT ''")
        connection.commit()
    except Exception:
        pass  # Coluna já existe, ignorar


def generate_salt() -> str:
    """Gera um salt único e aleatório para cada credencial (UUID v4)."""
    return str(uuid.uuid4())


def derive_key(website: str, url: str, credential_salt: str, website_created_at: str) -> bytes:
    """Deriva uma chave Fernet deterministicamente a partir de campos imutáveis.

    Campos usados — NENHUM é editável pelo utilizador:
      • website           → nome do site (tabela website, UNIQUE)
      • url               → url do site  (tabela website)
      • credential_salt   → UUID aleatório gerado na criação da credencial (nunca muda)
      • website_created_at→ timestamp de criação do website (gerado automaticamente)

    Lógica matemática:
      • password_material = website | url                          (identidade do site)
      • salt              = SHA-256( credential_salt | website_created_at )  (32 bytes fixos)
      • raw_key           = PBKDF2-HMAC-SHA256( password_material, salt, 200 000 iter, 32 bytes )
      • chave Fernet      = Base64-URL( raw_key )

    username e email são editáveis livremente — não entram no cálculo.
    """
    # Material de "palavra-passe": identidade imutável do site
    password_material = f"{website}|{url}".encode("utf-8")

    # Salt: UUID único da credencial + timestamp do website — nunca guardado separadamente
    salt_raw = f"{credential_salt}|{website_created_at}".encode("utf-8")
    salt = hashlib.sha256(salt_raw).digest()  # 32 bytes fixos

    # PBKDF2-HMAC-SHA256: 200 000 iterações, 32 bytes de saída
    raw_key = hashlib.pbkdf2_hmac(
        "sha256",
        password_material,
        salt,
        iterations=200_000,
        dklen=32,
    )

    # Fernet requer Base64-URL de exatamente 32 bytes
    return base64.urlsafe_b64encode(raw_key)


def encrypt_password(plain: str, key: bytes) -> str:
    """Encripta uma password em texto-limpo com a chave derivada."""
    return Fernet(key).encrypt(plain.encode("utf-8")).decode("utf-8")


def decrypt_password(token: str, key: bytes) -> str:
    """Desencripta um token Fernet com a chave derivada."""
    return Fernet(key).decrypt(token.encode("utf-8")).decode("utf-8")


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
      \033[38;5;99m[3]\033[0m  🚪  Exit

\033[38;5;244m─────────────────────────────────────────────────────────────────────\033[0m
""");
    option = input("""   \033[90mSelect option > \033[0m""");
    return option;

# IdentityHub

IdentityHub is a local password management application built in Python, with a command-line interface (CLI). Its primary purpose is to allow users to store, organize, and manage credentials across multiple websites in a centralized and secure local environment.

The idea behind creating this application came from the need for a **free, personalized solution**, as most existing tools are paid, combined with a personal experience of feeling disorganized and forgetting passwords.

---

## Objective

The main goal of IdentityHub is to provide a **lightweight, local, and secure solution** for credential management. The application allows users to:

- Store usernames, emails, and passwords for multiple websites.
- Navigate through a **modular Main Menu**.
- Encrypt all passwords using **Fernet (cryptography)**, ensuring that only those with the key can decrypt them.
- Safely store the encryption key (`identityhub.key`) and the database (`identityhub.db`) in a dedicated local folder (`data/`) to minimize the risk of loss or unauthorized access.

---

## Current Version

**Version:** 0.5.0 (CLI Foundation, Complete Websites Table, Manager Add with Encryption and Fernet Key Storage)

This version includes:

- **Complete Websites Table** – fully functional navigation, addition, and selection of websites.
- **Manager Add functionality** – allows adding usernames and emails (required or optional), with passwords encrypted.
- **Password encryption** – using Fernet symmetric encryption for local security.
- **Key and database storage** – both `identityhub.db` and `identityhub.key` files are stored in the `data/` folder.

### About `identityhub.db` and `identityhub.key`

1. **identityhub.db** – a local SQLite database storing all website, credential, and creation log information.  
2. **identityhub.key** – the Fernet encryption key required to decrypt stored passwords.

⚠️ **Important Note:** If the user deletes the key (`identityhub.key`) and/or the database (`identityhub.db`), **all stored passwords will become irrecoverable**.  

**To safeguard data during system format or migration:**

1. Backup **both files** (`identityhub.db` and `identityhub.key`) to a secure location.
2. After reinstalling the application, restore the files to the `data/` folder.
3. Ensure the application can access the key before attempting to decrypt any passwords.

---

## Project Structure

IdentityHub/
│
├── core/
│ ├── images/
│ │ └── icon.ico
│ ├── services/
│ │ ├── manager_service.py
│ │ ├── password_service.py
│ │ └── website_service.py
│ └── utilities/
│ └── tools.py
├── data/
│ ├── identityhub.db
│ └── identityhub.key
├── docs/
│ └── architecture.md
├── LICENSE
├── main.py
└── README.md

---

## License

This project is distributed under the terms defined in the [LICENSE](https://github.com/pedronogsilva/IdentityHub/blob/main/LICENSE) file.
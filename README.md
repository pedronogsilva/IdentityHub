# IdentityHub

IdentityHub is a local password management application built in Python. It provides a structured command-line interface (CLI) that allows users to organize and manage credentials across multiple websites in a centralized local environment.

Managing multiple accounts across different platforms can quickly become disorganized. IdentityHub aims to solve this problem by offering a clear navigation system through a modular Main Menu, which serves as the core control layer of the application.

This first version focuses on building the foundation of the system, ensuring clean architecture and scalability for future security and feature expansion.

---

## Current Version

**Version:** 0.1 (CLI Foundation)

This release includes:

- Structured CLI Main Menu  
- Modular project organization  
- Local database integration  
- Base website and credential management system  

---

## Project Structure

```
IdentityHub/
│
├── core/
│   ├── services/
│   │   ├── manager_service.py
│   │   ├── password_service.py
│   │   └── website_service.py
│   └── utilities/
│       └── tools.py
├── data/
│   └── identityhub.db
├── docs/
│   └── architecture.md
├── LICENSE
├── main.py
└── README.md
```

---

## License

This project is distributed under the terms defined in the [LICENSE](https://github.com/pedronogsilva/IdentityHub/blob/main/LICENSE) file.

# Library Management System

A simple, beginner-friendly **Library Management System** written Python using Object-Oriented Programming (OOP) and JSON files.

## How to Run

```bash
python main.py
```

## Login Accounts

| Username | Password | Role | Access |
| :--- | :--- | :--- | :--- |
| `admin` | `admin123` | `manager` | Full Access (Options 1–6: Borrow/Return + Manage Books & Members) |
| `librarian` | `lib123` | `librarian` | Daily Operations (Options 1–4: View, Borrow, Return, History) |

## Project Structure

```text
library_system/
├── main.py                  # Runs the menu loop and prints simple tables
├── data/                    # JSON files for saving data
│   ├── books.json
│   ├── members.json
│   ├── borrows.json
│   └── users.json
├── models/                  # OOP Classes
│   ├── book.py              # Book (id, title, author, category, stock)
│   ├── member.py            # Member (id, name, phone)
│   ├── borrow_record.py     # BorrowRecord (record_id, member, book, dates, status)
│   └── user.py              # User (username, password, role)
├── services/                # Core Logic
│   ├── auth_service.py      # Login and logout
│   └── library_service.py   # Add/delete books & members, borrow & return books
└── utils/                   # Helpers
    ├── exceptions.py        # Custom error classes (Inheritance)
    └── storage.py           # Load and save JSON files
```

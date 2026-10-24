from utils.storage import JSONStorage
from utils.exceptions import LibraryError, InvalidInputError
from services.auth_service import AuthService
from services.library_service import LibraryService


def print_header(title):
    print("\n" + "=" * 65)
    print(f"  {title}")
    print("=" * 65)


def print_books_table(books):
    if not books:
        print("  No books found.")
        return
    print(f"  {'ID':<4} | {'Title':<28} | {'Author':<18} | {'Stock':<5}")
    print("  " + "-" * 61)
    for b in books:
        stock_label = str(b.stock) if b.stock > 0 else "0 (Out)"
        print(f"  {b.id:<4} | {b.title[:28]:<28} | {b.author[:18]:<18} | {stock_label:<5}")


def print_members_table(members):
    if not members:
        print("  No members found.")
        return
    print(f"  {'ID':<4} | {'Name':<25} | {'Phone':<15}")
    print("  " + "-" * 50)
    for m in members:
        print(f"  {m.id:<4} | {m.name[:25]:<25} | {m.phone:<15}")


def print_borrows_table(records):
    if not records:
        print("  No borrow records found.")
        return
    print(f"  {'ID':<5} | {'Member':<16} | {'Book Title':<22} | {'Due Date':<10} | {'Status':<8}")
    print("  " + "-" * 71)
    for r in records:
        print(
            f"  {r.record_id:<5} | {r.member_name[:16]:<16} | "
            f"{r.book_title[:22]:<22} | {r.due_date:<10} | {r.status:<8}"
        )


class LibraryApp:
    def __init__(self):
        self.storage = JSONStorage("data")
        self.auth_service = AuthService(self.storage)
        self.library_service = LibraryService(self.storage)

    def run(self):
        while True:
            if self.auth_service.current_user is None:
                if not self.handle_login():
                    break
            else:
                self.handle_main_menu()

    def handle_login(self):
        print_header("LIBRARY MANAGEMENT SYSTEM - LOGIN")
        print("  (Type 'exit' to quit)\n")

        username = input("  Username: ").strip()
        if username.lower() in ("exit", "quit"):
            print("\n  Goodbye!")
            return False

        password = input("  Password: ").strip()
        try:
            user = self.auth_service.login(username, password)
            print(f"\n  [OK] Welcome, {user.username} ({user.role})!")
        except LibraryError as error:
            print(f"\n  [ERROR] {error}")
        return True

    def handle_main_menu(self):
        user = self.auth_service.current_user
        print_header(f"MAIN MENU ({user.username.upper()} - {user.role.upper()})")
        print("  1. View / Search Books")
        print("  2. Borrow a Book")
        print("  3. Return a Book")
        print("  4. View Borrow History")
        if user.is_manager:
            print("  5. Manage Books (Add / Update Stock / Delete)")
            print("  6. Manage Members (Add / Delete)")
        print("  0. Logout")

        choice = input("\n  Select option: ").strip()

        try:
            if choice == "1":
                self.menu_view_books()
            elif choice == "2":
                self.menu_borrow_book()
            elif choice == "3":
                self.menu_return_book()
            elif choice == "4":
                self.menu_borrow_history()
            elif choice == "5" and user.is_manager:
                self.menu_manage_books()
            elif choice == "6" and user.is_manager:
                self.menu_manage_members()
            elif choice == "0":
                self.auth_service.logout()
                print("\n  Logged out successfully.")
            else:
                print("\n  [ERROR] Invalid menu option.")
        except (LibraryError, ValueError) as error:
            print(f"\n  [ERROR] {error}")

    def menu_view_books(self):
        print_header("BOOKS CATALOG")
        print_books_table(self.library_service.list_books())
        keyword = input("\n  Enter keyword to search (or press Enter to go back): ").strip()
        if keyword:
            results = self.library_service.search_books(keyword)
            print_header(f"SEARCH RESULTS ({len(results)} found)")
            print_books_table(results)
            input("\n  Press Enter to continue...")

    def menu_borrow_book(self):
        print_header("BORROW A BOOK")
        print_books_table(self.library_service.list_books())
        print()
        print_members_table(self.library_service.list_members())

        raw_member = input("\n  Enter Member ID (or press Enter to cancel): ").strip()
        if not raw_member:
            return
        raw_book = input("  Enter Book ID to borrow: ").strip()
        if not raw_member.isdigit() or not raw_book.isdigit():
            raise InvalidInputError("Member ID and Book ID must be numbers.")

        record = self.library_service.borrow_book(int(raw_member), int(raw_book))
        print(
            f"\n  [OK] '{record.book_title}' borrowed by {record.member_name}!"
            f"\n       Record ID: #{record.record_id} | Due Date: {record.due_date}"
        )
        input("\n  Press Enter to continue...")

    def menu_return_book(self):
        print_header("RETURN A BOOK")
        active = [r for r in self.library_service.borrows if r.status == "Borrowed"]
        if not active:
            print("  No active borrowed books right now.")
            input("\n  Press Enter to continue...")
            return

        print_borrows_table(active)
        raw_id = input("\n  Enter Record ID to return (or press Enter to cancel): ").strip()
        if not raw_id:
            return
        if not raw_id.isdigit():
            raise InvalidInputError("Record ID must be a number.")

        record = self.library_service.return_book(int(raw_id))
        print(f"\n  [OK] Returned '{record.book_title}' from {record.member_name}. Stock restored!")
        input("\n  Press Enter to continue...")

    def menu_borrow_history(self):
        print_header("BORROW HISTORY")
        print_borrows_table(self.library_service.borrows)
        input("\n  Press Enter to continue...")

    def menu_manage_books(self):
        print_header("MANAGE BOOKS")
        print_books_table(self.library_service.list_books())
        print("\n  a. Add new book")
        print("  b. Update book stock")
        print("  c. Delete book")
        print("  d. Back")

        sub = input("\n  Select (a-d): ").strip().lower()
        if sub == "a":
            title = input("  Book Title : ").strip()
            author = input("  Author     : ").strip()
            category = input("  Category (default General): ").strip() or "General"
            stock = int(input("  Stock Copies: ").strip())
            book = self.library_service.add_book(title, author, category, stock)
            print(f"\n  [OK] Added Book #{book.id}: '{book.title}'")
        elif sub == "b":
            book_id = int(input("  Enter Book ID: ").strip())
            new_stock = int(input("  Enter New Stock: ").strip())
            book = self.library_service.update_book_stock(book_id, new_stock)
            print(f"\n  [OK] Updated stock for '{book.title}' to {book.stock}.")
        elif sub == "c":
            book_id = int(input("  Enter Book ID to delete: ").strip())
            book = self.library_service.delete_book(book_id)
            print(f"\n  [OK] Deleted '{book.title}'.")

    def menu_manage_members(self):
        print_header("MANAGE MEMBERS")
        print_members_table(self.library_service.list_members())
        print("\n  a. Add new member")
        print("  b. Delete member")
        print("  c. Back")

        sub = input("\n  Select (a-c): ").strip().lower()
        if sub == "a":
            name = input("  Member Name : ").strip()
            phone = input("  Phone Number: ").strip()
            member = self.library_service.add_member(name, phone)
            print(f"\n  [OK] Added Member #{member.id}: {member.name}")
        elif sub == "b":
            member_id = int(input("  Enter Member ID to delete: ").strip())
            member = self.library_service.delete_member(member_id)
            print(f"\n  [OK] Deleted Member: {member.name}")


if __name__ == "__main__":
    app = LibraryApp()
    app.run()

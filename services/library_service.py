from datetime import datetime, timedelta
from models.book import Book
from models.member import Member
from models.borrow_record import BorrowRecord
from utils.exceptions import (
    RecordNotFoundError,
    InsufficientStockError,
    InvalidInputError,
)


class LibraryService:
    def __init__(self, storage):
        self.storage = storage
        self.books_file = "books.json"
        self.members_file = "members.json"
        self.borrows_file = "borrows.json"

        self.books = []
        self.members = []
        self.borrows = []
        self.load_all()


    def load_all(self):
        raw_books = self.storage.load(self.books_file, default_data=[])
        self.books = [
            Book(
                book_id=b.get("id", 1),
                title=b.get("title", ""),
                author=b.get("author", ""),
                category=b.get("category", "General"),
                stock=b.get("stock", 0),
            )
            for b in raw_books
        ]

        raw_members = self.storage.load(self.members_file, default_data=[])
        self.members = [
            Member(
                member_id=m.get("id", 1),
                name=m.get("name", ""),
                phone=m.get("phone", "N/A"),
            )
            for m in raw_members
        ]

        raw_borrows = self.storage.load(self.borrows_file, default_data=[])
        self.borrows = [
            BorrowRecord(
                record_id=r.get("record_id", 1001),
                member_id=r.get("member_id", 1),
                member_name=r.get("member_name", ""),
                book_id=r.get("book_id", 1),
                book_title=r.get("book_title", ""),
                borrow_date=r.get("borrow_date", ""),
                due_date=r.get("due_date", ""),
                status=r.get("status", "Borrowed"),
                return_date=r.get("return_date", None),
            )
            for r in raw_borrows
        ]

    def save_books(self):
        self.storage.save(self.books_file, [b.to_dict() for b in self.books])

    def save_members(self):
        self.storage.save(self.members_file, [m.to_dict() for m in self.members])

    def save_borrows(self):
        self.storage.save(self.borrows_file, [r.to_dict() for r in self.borrows])

    def list_books(self):
        return sorted(self.books, key=lambda b: b.id)

    def get_book_by_id(self, book_id):
        target_id = int(book_id)
        for book in self.books:
            if book.id == target_id:
                return book
        raise RecordNotFoundError(f"Book with ID {book_id} not found.")

    def search_books(self, keyword):
        if str(keyword).strip() == "":
            return self.list_books()
        return [b for b in self.books if b.matches_keyword(keyword)]

    def add_book(self, title, author, category, stock):
        next_id = max([b.id for b in self.books], default=0) + 1
        new_book = Book(next_id, title, author, category, stock)
        self.books.append(new_book)
        self.save_books()
        return new_book

    def update_book_stock(self, book_id, new_stock):
        book = self.get_book_by_id(book_id)
        if int(new_stock) < 0:
            raise InvalidInputError("Stock cannot be negative.")
        book.stock = int(new_stock)
        self.save_books()
        return book

    def delete_book(self, book_id):
        book = self.get_book_by_id(book_id)
        self.books.remove(book)
        self.save_books()
        return book


    def list_members(self):
        return sorted(self.members, key=lambda m: m.id)

    def get_member_by_id(self, member_id):
        target_id = int(member_id)
        for member in self.members:
            if member.id == target_id:
                return member
        raise RecordNotFoundError(f"Member with ID {member_id} not found.")

    def add_member(self, name, phone):
        next_id = max([m.id for m in self.members], default=0) + 1
        new_member = Member(next_id, name, phone)
        self.members.append(new_member)
        self.save_members()
        return new_member

    def delete_member(self, member_id):
        member = self.get_member_by_id(member_id)
        self.members.remove(member)
        self.save_members()
        return member


    def borrow_book(self, member_id, book_id, borrow_days=14):
        """Borrow 1 copy of a book for a member and reduce book stock."""
        member = self.get_member_by_id(member_id)
        book = self.get_book_by_id(book_id)

        if book.stock <= 0:
            raise InsufficientStockError(f"'{book.title}' is currently out of stock.")

        book.stock -= 1
        next_record_id = max([r.record_id for r in self.borrows], default=1000) + 1

        now = datetime.now()
        borrow_date = now.strftime("%Y-%m-%d")
        due_date = (now + timedelta(days=int(borrow_days))).strftime("%Y-%m-%d")

        record = BorrowRecord(
            record_id=next_record_id,
            member_id=member.id,
            member_name=member.name,
            book_id=book.id,
            book_title=book.title,
            borrow_date=borrow_date,
            due_date=due_date,
            status="Borrowed",
        )

        self.borrows.append(record)
        self.save_books()
        self.save_borrows()
        return record

    def return_book(self, record_id):
        """Mark a borrowed record as Returned and add 1 copy back to stock."""
        target_id = int(record_id)
        record = None
        for r in self.borrows:
            if r.record_id == target_id:
                record = r
                break

        if record is None:
            raise RecordNotFoundError(f"Borrow record #{record_id} not found.")
        if record.status == "Returned":
            raise InvalidInputError(f"Record #{record_id} has already been returned.")

        # Restore book stock if book still exists
        try:
            book = self.get_book_by_id(record.book_id)
            book.stock += 1
        except RecordNotFoundError:
            pass

        record.status = "Returned"
        record.return_date = datetime.now().strftime("%Y-%m-%d")

        self.save_books()
        self.save_borrows()
        return record

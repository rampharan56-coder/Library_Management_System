from utils.exceptions import InvalidInputError


class Book:
    def __init__(self, book_id, title, author, category="General", stock=1):
        title = str(title).strip()
        author = str(author).strip()
        category = str(category).strip() or "General"
        stock = int(stock)

        if title == "":
            raise InvalidInputError("Book title cannot be empty.")
        if author == "":
            raise InvalidInputError("Author name cannot be empty.")
        if stock < 0:
            raise InvalidInputError("Stock cannot be negative.")

        self.id = int(book_id)
        self.title = title
        self.author = author
        self.category = category
        self.stock = stock

    def matches_keyword(self, keyword):
        kw = str(keyword).strip().lower()
        return (
            kw in str(self.id)
            or kw in self.title.lower()
            or kw in self.author.lower()
            or kw in self.category.lower()
        )

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "category": self.category,
            "stock": self.stock,
        }

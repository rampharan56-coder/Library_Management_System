class BorrowRecord:
    def __init__(
        self,
        record_id,
        member_id,
        member_name,
        book_id,
        book_title,
        borrow_date,
        due_date,
        status="Borrowed",
        return_date=None,
    ):
        self.record_id = int(record_id)
        self.member_id = int(member_id)
        self.member_name = str(member_name)
        self.book_id = int(book_id)
        self.book_title = str(book_title)
        self.borrow_date = str(borrow_date)
        self.due_date = str(due_date)
        self.status = str(status)
        self.return_date = return_date

    def to_dict(self):
        return {
            "record_id": self.record_id,
            "member_id": self.member_id,
            "member_name": self.member_name,
            "book_id": self.book_id,
            "book_title": self.book_title,
            "borrow_date": self.borrow_date,
            "due_date": self.due_date,
            "status": self.status,
            "return_date": self.return_date,
        }

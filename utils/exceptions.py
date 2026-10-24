
class LibraryError(Exception):
    pass


class AuthenticationError(LibraryError):
    pass


class RecordNotFoundError(LibraryError):
    pass


class InsufficientStockError(LibraryError):
    pass


class InvalidInputError(LibraryError):
    pass

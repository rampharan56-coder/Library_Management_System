from models.user import User
from utils.exceptions import AuthenticationError

DEFAULT_USERS = [
    {"username": "admin", "password": "admin123", "role": "manager"},
    {"username": "librarian", "password": "lib123", "role": "librarian"},
]


class AuthService:
    def __init__(self, storage):
        self.storage = storage
        self.filename = "users.json"
        self.current_user = None
        self.users = []
        self.load_users()

    def load_users(self):
        raw_users = self.storage.load(self.filename, default_data=DEFAULT_USERS)
        self.users = []
        for data in raw_users:
            user = User(
                username=data.get("username", ""),
                password=data.get("password", ""),
                role=data.get("role", "librarian"),
            )
            self.users.append(user)

    def login(self, username, password):
        username_clean = str(username).strip()
        if username_clean == "" or password == "":
            raise AuthenticationError("Username and password are required.")

        for user in self.users:
            if user.username.lower() == username_clean.lower():
                if user.verify_password(password):
                    self.current_user = user
                    return user
                raise AuthenticationError("Incorrect password.")

        raise AuthenticationError(f"User '{username_clean}' not found.")

    def logout(self):
        self.current_user = None

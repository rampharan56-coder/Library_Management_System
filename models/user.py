class User:
    def __init__(self, username, password, role="librarian"):
        self.username = str(username).strip()
        self.password = str(password).strip()
        self.role = str(role).strip().lower()
        self.is_manager = (self.role == "manager")

    def verify_password(self, input_password):
        return self.password == input_password

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "role": self.role,
        }

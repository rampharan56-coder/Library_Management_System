from utils.exceptions import InvalidInputError


class Member:
    def __init__(self, member_id, name, phone=""):
        name = str(name).strip()
        phone = str(phone).strip() or "N/A"

        if name == "":
            raise InvalidInputError("Member name cannot be empty.")

        self.id = int(member_id)
        self.name = name
        self.phone = phone

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
        }

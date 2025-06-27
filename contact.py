class Contact:
    def __init__(self, name, phone, email, address):
        if not name or not isinstance(name, str):
            raise ValueError("Name cannot be empty and must be a string.")
        if not phone.isdigit():
            raise ValueError("Phone number must contain only digits.")
        self._name = name
        self._phone = phone
        self._email = email
        self._address = address

    @property
    def name(self):
        return self._name

    @property
    def phone(self):
        return self._phone

    @property
    def email(self):
        return self._email

    @property
    def address(self):
        return self._address

    def to_dict(self):
        return {
            "Name": self.name,
            "Phone": self.phone,
            "Email": self.email,
            "Address": self.address
        }

    @staticmethod
    def from_dict(data):
        return Contact(data['Name'], data['Phone'], data['Email'], data['Address'])

    def __str__(self):
        return (f"Name: {self.name}\n"
                f"Phone: {self.phone}\n"
                f"Email: {self.email}\n"
                f"Address: {self.address}")

    def __repr__(self):
        return f"Contact(name='{self.name}', phone='{self.phone}', email='{self.email}', address='{self.address}')"

    def __eq__(self, other):
        if not isinstance(other, Contact):
            return NotImplemented
        return self.phone == other.phone

    def __hash__(self):
        return hash(self.phone)
class Person:
    """Base class for people-like objects with simple validation."""
    def __init__(self, name: str, email: str):
        # Store raw values on private attributes; properties enforce rules.
        self._name = name
        self._email = email

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not value.strip():
            raise ValueError("Name cannot be empty.")
        self._name = value

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str):
        # Very small email format check: must include '@' and a dot.
        if "@" not in value or "." not in value:
            raise ValueError("Invalid email format.")
        # If validation passes, update the stored email value.
        self._email = value
        
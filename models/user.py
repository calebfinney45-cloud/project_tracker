from models.person import Person

class User(Person):
    _id_counter = 0

    def __init__(self, name: str, email: str, user_id: int = None):
        super().__init__(name, email)
        if user_id is None:
            User._id_counter += 1
            self.id = User._id_counter
        else:
            self.id = user_id
            if user_id > User._id_counter:
                User._id_counter = user_id    

    def to_dict(self) -> dict:
        return {
            "id": self.id, 
            "name": self.name,
            "email": self.email
            }
    
    def __repr__(self) -> str:
        return f"[User {self.id}: {self.name} \n\n Email: {self.email}]"
    
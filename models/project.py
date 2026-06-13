class Project:
    _id_counter = 0

    def __init__(self, title: str, description: str, due_date: str, user_id: int, project_id: int = None):
        if project_id is None:
            Project._id_counter += 1
            self.id = Project._id_counter
        else:
            self.id = project_id
            if project_id > Project._id_counter:
                Project._id_counter = project_id

        self.title = title
        self.description = description
        # Keep the due date as a simple string (no accidental tuple).
        self.due_date = due_date
        # Store the owner user's ID (acts like a foreign key reference).
        self.user_id = user_id

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title, 
            "description": self.description,
            "due_date": self.due_date,
            "user_id": self.user_id
        }       

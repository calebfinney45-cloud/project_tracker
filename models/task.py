class Task:
    _id_counter = 0

    def __init__(self, title: str, project_id: int, status: str = "Pending", task_id: int = None):
        if task_id is None:
            Task._id_counter += 1
            self.id = Task._id_counter
        else:
            self.id = task_id
            if task_id > Task._id_counter:
                Task._id_counter = task_id

        self.title = title
        self.project_id = project_id  # Foreign key linking back to Project
        self.status = status

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "project_id": self.project_id,
            "status": self.status
        }
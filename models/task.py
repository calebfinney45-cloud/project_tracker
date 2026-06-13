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
        # Keep a simple link back to the project this task belongs to.
        self.project_id = project_id
        # Status is a short string like 'Pending' or 'Completed'.
        self.status = status

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "project_id": self.project_id,
            "status": self.status
        }
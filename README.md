# Project Tracker

A small CLI project tracker to manage users, projects, and tasks.

Features
- Create and list users
- Create and list projects (assigned to users)
- Add tasks to projects and mark them completed
- Data is stored in `data/storage.json` as simple JSON

Requirements
- Python 3.8+
- Pipenv (used for managing the virtual environment)

Quick setup

1. Install dependencies and create the virtualenv:

```bash
pipenv install --dev
```

2. Run commands inside the virtualenv. Examples:

```bash
# Add a user
pipenv run python main.py add-user --name "Alice" --email "alice@domain.com"

# List users
pipenv run python main.py list-users

# Add a project for a user (user id 1)
pipenv run python main.py add-project --title "New App" --desc "Build MVP" --due "2026-12-31" --user-id 1

# Add a task to project (project id 1)
pipenv run python main.py add-task --title "Write tests" --project-id 1

# Mark a task completed (task id 1)
pipenv run python main.py complete-task --task-id 1

# List tasks (optionally for a project)
pipenv run python main.py list-tasks --project-id 1
```

Running tests

```bash
pipenv run pytest -q
```

Project layout

- `main.py` - CLI entrypoint and command handlers
- `utils/data_manager.py` - simple JSON persistence helpers
- `models/` - `person.py`, `user.py`, `project.py`, `task.py`
- `data/storage.json` - data file created at runtime
- `test_tracker.py` - unit tests

Notes
- This project uses a simple JSON file for persistence. It is fine for learning and small demos, but not intended for production use.


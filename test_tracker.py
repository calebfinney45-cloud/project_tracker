import pytest
from unittest.mock import patch, mock_open
import json

from models.person import Person
from models.user import User
from models.project import Project
from models.task import Task
from utils.data_manager import load_data, save_data

# ======================== OOP & VALIDATION TESTS ========================

def test_person_encapsulation():
    """Test that Person properties correctly validate inputs."""
    person = Person("Alice", "alice@example.com")
    assert person.name == "Alice"
    assert person.email == "alice@example.com"

    # Test invalid email setter
    with pytest.raises(ValueError, match="Invalid email format."):
        person.email = "bad_email_no_at"

    # Test empty name setter
    with pytest.raises(ValueError, match="Name cannot be empty."):
        person.name = "   "


def test_user_inheritance_and_counting():
    """Test User inherits from Person and increments the ID class counter."""
    # Reset counter for explicit testing state
    User._id_counter = 0
    
    user1 = User("Bob", "bob@example.com")
    user2 = User("Charlie", "charlie@example.com")
    
    assert isinstance(user1, Person)
    assert user1.id == 1
    assert user2.id == 2
    assert user2.name == "Charlie"


def test_project_and_task_relations():
    """Test relational integrity links (foreign-key style IDs)."""
    Project._id_counter = 0
    Task._id_counter = 0

    # User ID = 5 owns this project
    proj = Project("SkyBound Dashboard", "Flight tracker", "2026-12-31", user_id=5)
    assert proj.user_id == 5
    assert proj.id == 1

    # Task links back to Project ID = 1
    task = Task("Write unit tests", project_id=proj.id)
    assert task.project_id == 1
    assert task.status == "Pending"


# ======================== PERSISTENCE MOCK TESTS ========================

@patch("builtins.open", new_callable=mock_open, read_data='{"users":[],"projects":[],"tasks":[]}')
@patch("os.path.exists", return_value=True)
@patch("os.path.getsize", return_value=100)
def test_load_data_success(mock_exists, mock_size, mock_file):
    """Test loading data structures correctly reads clean JSON payloads."""
    data = load_data()
    assert "users" in data
    assert len(data["users"]) == 0


@patch("builtins.open", new_callable=mock_open)
def test_save_data_success(mock_file):
    """Test saving serialized objects correctly passes to file streams."""
    sample_data = {"users": [{"id": 1, "name": "Alice", "email": "a@b.com"}], "projects": [], "tasks": []}
    save_data(sample_data)
    
    # Verify file opened for writing
    mock_file.assert_called_once_with("data/storage.json", "w")
import pytest
from fastapi.testclient import TestClient
from main import app
from models import Task, UpdateTaskModel, TaskList
from db import db

client = TestClient(app)

def test_create_task():
    task_data = {"id": 1, "title": "Test Task", "description": "This is a test task", "completed": False}
    response = client.post("/tasks/", json=task_data)
    assert response.status_code == 200
    assert response.json() == task_data

def test_get_task():
    task_id = 1
    task_data = {"id": task_id, "title": "Test Task", "description": "This is a test task", "completed": False}
    db.add_task(Task(**task_data))
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json() == task_data

def test_get_task_not_found():
    response = client.get("/tasks/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}

def test_get_tasks():
    db.delete_all_tasks()
    task1 = {"id": 1, "title": "Task 1", "description": "Description 1", "completed": False}
    task2 = {"id": 2, "title": "Task 2", "description": "Description 2", "completed": True}
    db.add_task(Task(**task1))
    db.add_task(Task(**task2))
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert response.json() == {"tasks": [task1, task2]}

def test_update_task():
    task_id = 1
    original_task = {"id": task_id, "title": "Original Task", "description": "Original description", "completed": False}
    db.add_task(Task(**original_task))
    update_data = {"title": "Updated Task", "description": "Updated description", "completed": True}
    response = client.put(f"/tasks/{task_id}", json=update_data)
    assert response.status_code == 200
    assert response.json() == {**original_task, **update_data}

def test_update_task_not_found():
    update_data = {"title": "Updated Task", "description": "Updated description", "completed": True}
    response = client.put("/tasks/999", json=update_data)
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}

def test_delete_all_tasks():
    db.add_task(Task(id=1, title="Task 1", description="Description 1", completed=False))
    db.add_task(Task(id=2, title="Task 2", description="Description 2", completed=True))
    response = client.delete("/tasks/all")
    assert response.status_code == 200
    assert response.json() == {"message": "All tasks deleted successfully"}
    assert len(db.get_tasks()) == 0

def test_delete_task():
    task_id = 1
    db.add_task(Task(id=task_id, title="Task to delete", description="This task will be deleted", completed=False))
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Task deleted successfully"}
    assert db.get_task(task_id) is None

def test_delete_task_not_found():
    response = client.delete("/tasks/999")
    assert response.status_code == 200
    assert response.json() == {"message": "Task deleted successfully"}

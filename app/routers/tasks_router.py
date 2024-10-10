"""
Provides an API router for managing tasks.

The `tasks_router` handles the following endpoints:

- `POST /`: Creates a new task.
- `GET /{task_id}`: Retrieves a task by its ID.
- `GET /`: Retrieves a list of all tasks.
- `PUT /{task_id}`: Updates a task by its ID.
- `DELETE /all`: Deletes all tasks.
- `DELETE /{task_id}`: Deletes a task by its ID.
"""
from fastapi import APIRouter, HTTPException, Path
from models import Task, UpdateTaskModel, TaskList
from db import db

tasks_router = APIRouter()


"""
Creates a new task.

Args:
    task (Task): The task to be created.

Returns:
    Task: The created task.
"""
@tasks_router.post("/", response_model=Task)
async def create_task(task: Task):
    return db.add_task(task)


"""
Retrieves a task by its ID.

Args:
    task_id (int): The ID of the task to retrieve.

Returns:
    Task: The retrieved task.

Raises:
    HTTPException: If the task with the given ID is not found.
"""
@tasks_router.get("/{task_id}", response_model=Task)
async def get_task(task_id: int = Path(..., gt=0)):
    task = db.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


"""
Retrieves a list of all tasks.

Returns:
    TaskList: A list of all tasks.
"""
@tasks_router.get("/", response_model=TaskList)
async def get_tasks():
    tasks = db.get_tasks()
    return TaskList(tasks=tasks)


"""
Updates an existing task.

Args:
    task_id (int): The ID of the task to update.
    task_update (UpdateTaskModel): The updated task data.

Returns:
    Task: The updated task.

Raises:
    HTTPException: If the task with the given ID is not found.
"""
@tasks_router.put("/{task_id}", response_model=Task)
async def update_task(task_update: UpdateTaskModel, task_id: int = Path(..., gt=0)):
    updated_task = db.update_task(task_id, task_update)
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

"""
Deletes all tasks.

Returns:
    dict: A message indicating that all tasks were deleted successfully.
"""
@tasks_router.delete("/all", response_model=dict)
async def delete_all_tasks():
    db.delete_all_tasks()
    return {"message": "All tasks deleted successfully"}

"""
Deletes a task with the given ID.

Args:
    task_id (int): The ID of the task to delete.

Returns:
    dict: A message indicating that the task was deleted successfully.
"""
@tasks_router.delete("/{task_id}")
async def delete_task(task_id: int = Path(..., gt=0)):
    db.delete_task(task_id)
    return {"message": "Task deleted successfully"}
from database.transaction_manager import TransactionManager
from repositories.task_repository import (
    get_all_tasks,
    get_task_by_id,
    create_task as repo_create_task,
    delete_task as repo_delete_task,
    update_task_status as repo_update_task_status
)
from auth.permissions import can_create_task, can_delete_task
from rules.workflow_rules import can_transition


def list_tasks():
    with TransactionManager() as conn:
        tasks = get_all_tasks(conn)
        return [dict(task) for task in tasks]


def create_task(data, user):
    if not can_create_task(user["role"]):
        return {"error": "Access denied"}, 403

    with TransactionManager() as conn:
        task_id = repo_create_task(
    conn,
    data["title"],
    "Backlog",
    data["priority"],
    data.get("assigned_to"),
    data.get("due_date")
)

        return {"message": "Task created", "task_id": task_id}, 201


def delete_task(task_id, user):
    if not can_delete_task(user["role"]):
        return {"error": "Access denied"}, 403

    with TransactionManager() as conn:
        repo_delete_task(conn, task_id)
        return {"message": "Task deleted"}, 200


def update_status(task_id, new_status, user):
    with TransactionManager() as conn:
        task = get_task_by_id(conn, task_id)

        if not task:
            return {"error": "Task not found"}, 404

        current_status = task["status"]

        if not can_transition(user["role"], current_status, new_status):
            return {
                "error": f"Invalid transition from {current_status} to {new_status}"
            }, 403

        repo_update_task_status(conn, task_id, new_status)

        return {"message": "Task status updated"}, 200
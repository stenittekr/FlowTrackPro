from auth.permissions import (
    can_create_task,
    can_delete_task
)

def test_admin_can_create():
    assert can_create_task("Admin") is True

def test_viewer_cannot_create():
    assert can_create_task("Viewer") is False

def test_manager_can_delete():
    assert can_delete_task("Manager") is True

def test_developer_cannot_delete():
    assert can_delete_task("Developer") is False
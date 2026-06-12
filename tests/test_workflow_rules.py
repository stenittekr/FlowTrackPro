from rules.workflow_rules import can_transition

def test_manager_can_approve():
    assert can_transition(
        "Manager",
        "Review",
        "Approved"
    ) is True

def test_developer_cannot_approve():
    assert can_transition(
        "Developer",
        "Review",
        "Approved"
    ) is False

def test_viewer_cannot_move_tasks():
    assert can_transition(
        "Viewer",
        "Backlog",
        "In Progress"
    ) is False
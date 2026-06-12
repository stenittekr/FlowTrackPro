VALID_TRANSITIONS = {
    "Backlog": ["In Progress"],
    "In Progress": ["Review"],
    "Review": ["Approved"],
    "Approved": ["Done"],
    "Done": []
}


def can_transition(role, current_status, new_status):

    if role == "Viewer":
        return False

    if (
        current_status == "Review"
        and new_status == "Approved"
    ):
        return role in ["Admin", "Manager"]

    allowed = VALID_TRANSITIONS.get(
        current_status,
        []
    )

    return new_status in allowed
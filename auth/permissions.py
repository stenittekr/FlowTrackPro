def can_create_task(role):
    return role in ["Admin", "Manager", "Developer"]

def can_delete_task(role):
    return role in ["Admin", "Manager"]

def can_manage_users(role):
    return role == "Admin"
from database.transaction_manager import TransactionManager
from repositories.user_repository import (
    get_all_users,
    update_user_role
)


def list_users():
    with TransactionManager() as conn:
        users = get_all_users(conn)
        return [dict(user) for user in users]


def change_role(user_id, role):
    with TransactionManager() as conn:
        update_user_role(
            conn,
            user_id,
            role
        )

        return {
            "message": "Role updated"
        }
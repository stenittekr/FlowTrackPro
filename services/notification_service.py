from database.transaction_manager import TransactionManager
from repositories.notification_repository import (
    create_notification,
    get_user_notifications,
    mark_as_read
)


def notify_user(user_id, message):
    with TransactionManager() as conn:
        create_notification(conn, user_id, message)

    return {"message": "Notification created"}


def list_notifications(user_id):
    with TransactionManager() as conn:
        notifications = get_user_notifications(conn, user_id)
        return [dict(item) for item in notifications]


def read_notification(notification_id):
    with TransactionManager() as conn:
        mark_as_read(conn, notification_id)

    return {"message": "Notification marked as read"}
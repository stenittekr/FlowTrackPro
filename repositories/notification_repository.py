def create_notification(conn, user_id, message):
    conn.execute(
        """
        INSERT INTO notifications
        (user_id, message)
        VALUES (?, ?)
        """,
        (user_id, message)
    )


def get_user_notifications(conn, user_id):
    return conn.execute(
        """
        SELECT *
        FROM notifications
        WHERE user_id = ?
        ORDER BY id DESC
        """,
        (user_id,)
    ).fetchall()


def mark_as_read(conn, notification_id):
    conn.execute(
        """
        UPDATE notifications
        SET is_read = 1
        WHERE id = ?
        """,
        (notification_id,)
    )
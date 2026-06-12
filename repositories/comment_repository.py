def add_comment(conn, task_id, user_id, comment):

    cursor = conn.execute(
        """
        INSERT INTO task_comments
        (
            task_id,
            user_id,
            comment
        )
        VALUES (?, ?, ?)
        """,
        (
            task_id,
            user_id,
            comment
        )
    )

    return cursor.lastrowid


def get_comments(conn, task_id):

    return conn.execute(
        """
        SELECT *
        FROM task_comments
        WHERE task_id = ?
        ORDER BY created_at DESC
        """,
        (task_id,)
    ).fetchall()
def get_all_tasks(conn):
    return conn.execute(
        "SELECT * FROM tasks ORDER BY id DESC"
    ).fetchall()


def get_task_by_id(conn, task_id):
    return conn.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()
def create_task(
    conn,
    title,
    status,
    priority,
    assigned_to=None,
    due_date=None
):
    cursor = conn.execute(
        """
        INSERT INTO tasks
        (
            title,
            status,
            priority,
            assigned_to,
            due_date
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            title,
            status,
            priority,
            assigned_to,
            due_date
        )
    )

    return cursor.lastrowid
def create_task(
    conn,
    title,
    status,
    priority,
    assigned_to=None,
    due_date=None
):
    cursor = conn.execute(
        """
        INSERT INTO tasks (
            title,
            status,
            priority,
            assigned_to,
            due_date
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            title,
            status,
            priority,
            assigned_to,
            due_date
        )
    )

    return cursor.lastrowid


def delete_task(conn, task_id):
    conn.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )


def update_task_status(conn, task_id, status):
    conn.execute(
        "UPDATE tasks SET status = ? WHERE id = ?",
        (status, task_id)
    )
def create_attachment(
    conn,
    task_id,
    file_name,
    file_path,
    uploaded_by
):
    cursor = conn.execute(
        """
        INSERT INTO attachments
        (
            task_id,
            file_name,
            file_path,
            uploaded_by
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            task_id,
            file_name,
            file_path,
            uploaded_by
        )
    )

    return cursor.lastrowid


def get_attachments(
    conn,
    task_id
):
    return conn.execute(
        """
        SELECT *
        FROM attachments
        WHERE task_id = ?
        ORDER BY uploaded_at DESC
        """,
        (task_id,)
    ).fetchall()
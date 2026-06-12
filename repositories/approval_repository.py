def create_approval_request(
    conn,
    task_id,
    requested_by
):
    cursor = conn.execute(
        """
        INSERT INTO approval_requests
        (
            task_id,
            requested_by,
            status
        )
        VALUES (?, ?, 'Pending')
        """,
        (
            task_id,
            requested_by
        )
    )

    return cursor.lastrowid


def get_pending_requests(conn):
    return conn.execute("""
        SELECT *
        FROM approval_requests
        WHERE status='Pending'
    """).fetchall()


def approve_request(
    conn,
    request_id,
    approved_by
):
    conn.execute(
        """
        UPDATE approval_requests
        SET
            approved_by=?,
            status='Approved'
        WHERE id=?
        """,
        (
            approved_by,
            request_id
        )
    )
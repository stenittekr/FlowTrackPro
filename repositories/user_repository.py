def get_all_users(conn):
    return conn.execute("""
        SELECT
            id,
            username,
            email,
            role
        FROM users
        ORDER BY username
    """).fetchall()


def update_user_role(conn, user_id, role):
    conn.execute("""
        UPDATE users
        SET role = ?
        WHERE id = ?
    """, (role, user_id))
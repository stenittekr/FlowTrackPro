import sqlite3

DB_NAME = "flowtrack.db"

def log_action(user_id, username, action, entity_type, entity_id=None):
    conn = sqlite3.connect(DB_NAME)

    conn.execute(
        """
        INSERT INTO audit_logs
        (user_id, username, action, entity_type, entity_id)
        VALUES (?, ?, ?, ?, ?)
        """,
        (user_id, username, action, entity_type, entity_id)
    )

    conn.commit()
    conn.close()
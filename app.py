from audit.audit_logger import log_action
from flask_mail import Mail
import config
import os
from werkzeug.utils import secure_filename

from services.attachment_service import (
    add_attachment,
    list_attachments
)
from services.comment_service import (
    create_comment,
    list_comments
)

from flask import Flask, render_template, request, jsonify, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from services.user_service import list_users, change_role
import sqlite3
from services.notification_service import (
    list_notifications,
    read_notification
)
from services.user_service import (
    list_users,
    change_role
)
from services.approval_service import (
    submit_for_approval,
    pending_approvals,
    approve
)
from services.task_service import (
    list_tasks,
    create_task as service_create_task,
    delete_task as service_delete_task,
    update_status as service_update_status
)
app = Flask(__name__)
DB_NAME = "flowtrack.db"
sqlite3.connect(DB_NAME)
app.secret_key = "flowtrack_secret_key"

app.config.from_object(config)
mail = Mail(app)

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn
@app.route(
    "/api/tasks/<int:task_id>/submit",
    methods=["POST"]
)
def submit_task(task_id):

    return jsonify(
        submit_for_approval(
            task_id,
            session["user_id"]
        )
    )


@app.route("/api/approvals")
def approvals():

    if session["role"] not in [
        "Admin",
        "Manager"
    ]:
        return jsonify({
            "error": "Access denied"
        }), 403

    return jsonify(
        pending_approvals()
    )


@app.route(
    "/api/approvals/<int:request_id>/approve",
    methods=["POST"]
)
def approve_task(request_id):

    if session["role"] not in [
        "Admin",
        "Manager"
    ]:
        return jsonify({
            "error": "Access denied"
        }), 403

    return jsonify(
        approve(
            request_id,
            session["user_id"]
        )
    )

def init_db():
    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'Developer'
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            status TEXT NOT NULL,
            priority TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

@app.route(
    "/api/tasks/<int:task_id>/comments"
)
def get_comments(task_id):

    return jsonify(
        list_comments(task_id)
    )


@app.route(
    "/api/tasks/<int:task_id>/comments",
    methods=["POST"]
)
def add_comment(task_id):

    data = request.get_json()

    return jsonify(
        create_comment(
            task_id,
            session["user_id"],
            data["comment"]
        )
    )
@app.route("/")
def home():
    if "user_id" not in session:
        return redirect("/login")

    return render_template(
        "index.html",
        username=session.get("username"),
        role=session.get("role")
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]
    role = request.form["role"]

    password_hash = generate_password_hash(password)

    try:
        conn = get_connection()
        conn.execute(
            "INSERT INTO users (username, email, password_hash, role) VALUES (?, ?, ?, ?)",
            (username, email, password_hash, role)
        )
        conn.commit()
        conn.close()

        return redirect("/login")

    except sqlite3.IntegrityError:
        return "Email already exists. Go back and use another email."


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form["email"]
    password = request.form["password"]

    conn = get_connection()
    user = conn.execute(
        "SELECT * FROM users WHERE email = ?",
        (email,)
    ).fetchone()
    conn.close()

    if user and check_password_hash(user["password_hash"], password):
        session["user_id"] = user["id"]
        session["username"] = user["username"]
        session["role"] = user["role"]
        return redirect("/")

    return "Invalid email or password."


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    return jsonify(list_tasks())


@app.route("/api/tasks", methods=["POST"])
def create_task():

    data = request.get_json()

    result, status = service_create_task(
        data,
        {
            "id": session.get("user_id"),
            "role": session.get("role"),
            "username": session.get("username")
        }
    )
   
    return jsonify(result), status
@app.route("/api/users")
def get_users():
    if session.get("role") != "Admin":
        return jsonify({"error": "Access denied"}), 403

    return jsonify(list_users())


@app.route(
    "/api/users/<int:user_id>/role",
    methods=["PUT"]
)
@app.route(
    "/api/users/<int:user_id>/role",
    methods=["PUT"]
)
@app.route("/api/users/<int:user_id>/role", methods=["PUT"])
def update_role(user_id):
    if session.get("role") != "Admin":
        return jsonify({"error": "Access denied"}), 403

    data = request.get_json()

    return jsonify(
        change_role(user_id, data["role"])
    )

@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):

    role = session.get("role")

    if not can_delete_task(role):
        return jsonify({"error": "Access denied"}), 403

    conn = get_connection()

    conn.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )

    conn.commit()
    log_action(
    session.get("user_id"),
    session.get("username"),
    "Deleted task",
    "Task",
    task_id
)
    conn.close()

    return jsonify({"message": "Task deleted"})

from auth.permissions import (
    can_create_task,
    can_delete_task
)
@app.route("/projects")
def projects_page():
    if "user_id" not in session:
        return redirect("/login")

    return render_template(
        "projects.html",
        username=session.get("username"),
        role=session.get("role")
    )


@app.route("/api/projects", methods=["GET"])
def get_projects():
    conn = get_connection()
    projects = conn.execute("SELECT * FROM projects ORDER BY id DESC").fetchall()
    conn.close()

    return jsonify([dict(project) for project in projects])
@app.route("/kanban")
def kanban_page():
    if "user_id" not in session:
        return redirect("/login")

    return render_template(
        "kanban.html",
        username=session.get("username"),
        role=session.get("role")
    )


@app.route("/api/tasks/<int:task_id>/status", methods=["PUT"])
def update_task_status(task_id):
    role = session.get("role")

    if role not in ["Admin", "Manager", "Developer"]:
        return jsonify({"error": "Access denied"}), 403

    data = request.get_json()

    conn = get_connection()
    conn.execute(
        "UPDATE tasks SET status = ? WHERE id = ?",
        (data["status"], task_id)
    )
    conn.commit()
    log_action(
    session.get("user_id"),
    session.get("username"),
    "Updated task status",
    "Task",
    task_id
)
    conn.close()

    return jsonify({"message": "Task status updated"})
@app.route("/kanban")
def kanban():

    if "user_id" not in session:
        return redirect("/login")

    return render_template(
        "kanban.html",
        username=session["username"],
        role=session["role"]
    )
@app.route("/audit-logs")
def audit_logs_page():
    if "user_id" not in session:
        return redirect("/login")

    if session.get("role") != "Admin":
        return "Access denied. Admin only."

    conn = get_connection()
    logs = conn.execute(
        "SELECT * FROM audit_logs ORDER BY id DESC"
    ).fetchall()
    conn.close()

    return render_template(
        "audit_logs.html",
        logs=logs,
        username=session.get("username"),
        role=session.get("role")
    )
@app.route("/api/projects", methods=["POST"])
def create_project():
    role = session.get("role")

    if role not in ["Admin", "Manager"]:
        return jsonify({"error": "Access denied"}), 403

    data = request.get_json()

    conn = get_connection()
    conn.execute(
        "INSERT INTO projects (name, description, status, created_by) VALUES (?, ?, ?, ?)",
        (
            data["name"],
            data["description"],
            "Active",
            session.get("user_id")
        )
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Project created"}), 201
@app.route("/users")
def users_page():

    if "user_id" not in session:
        return redirect("/login")

    if session.get("role") != "Admin":
        return "Access denied"

    return render_template(
        "users.html",
        username=session.get("username"),
        role=session.get("role")
    )
@app.route("/reports")
def reports_page():

    if "user_id" not in session:
        return redirect("/login")

    return render_template(
        "reports.html",
        username=session.get("username"),
        role=session.get("role")
    )
@app.route("/api/reports")
def get_reports():

    conn = get_connection()

    total_tasks = conn.execute(
        "SELECT COUNT(*) AS count FROM tasks"
    ).fetchone()["count"]

    total_projects = conn.execute(
        "SELECT COUNT(*) AS count FROM projects"
    ).fetchone()["count"]

    completed_tasks = conn.execute(
        """
        SELECT COUNT(*) AS count
        FROM tasks
        WHERE status='Done'
        """
    ).fetchone()["count"]

    backlog_tasks = conn.execute(
        """
        SELECT COUNT(*) AS count
        FROM tasks
        WHERE status='Backlog'
        """
    ).fetchone()["count"]

    conn.close()

    return jsonify({
        "total_tasks": total_tasks,
        "total_projects": total_projects,
        "completed_tasks": completed_tasks,
        "backlog_tasks": backlog_tasks
    })
@app.route("/approvals")
def approvals_page():
    if "user_id" not in session:
        return redirect("/login")

    if session.get("role") not in ["Admin", "Manager"]:
        return "Access denied. Manager/Admin only."

    return render_template(
        "approvals.html",
        username=session.get("username"),
        role=session.get("role")
    )
@app.route("/notifications")
def notifications_page():
    if "user_id" not in session:
        return redirect("/login")

    return render_template(
        "notifications.html",
        username=session.get("username"),
        role=session.get("role")
    )


@app.route("/api/notifications")
def get_notifications():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    return jsonify(
        list_notifications(session.get("user_id"))
    )


@app.route("/api/notifications/<int:notification_id>/read", methods=["PUT"])
def mark_notification_read(notification_id):
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    return jsonify(
        read_notification(notification_id)
    )
@app.route("/api/tasks/<int:task_id>/attachments", methods=["GET"])
def get_task_attachments(task_id):
    return jsonify(
        list_attachments(task_id)
    )


@app.route("/api/tasks/<int:task_id>/attachments", methods=["POST"])
def upload_attachment(task_id):
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    filename = secure_filename(file.filename)

    os.makedirs("uploads", exist_ok=True)

    file_path = os.path.join(
        "uploads",
        filename
    )

    file.save(file_path)

    return jsonify(
        add_attachment(
            task_id,
            filename,
            file_path,
            session.get("user_id")
        )
    ), 201
if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)

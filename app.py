# Help Desk Web Application
# This project uses Flask, MariaDB, Flask-Login, and Bootstrap.

# Import Flask tools for routes, forms, redirects, templates, and messages.
from flask import Flask, request, redirect, render_template_string, flash

# Import Flask-Login tools for user login/logout and protected pages.
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

# Import password hashing tools for safer password storage.
from werkzeug.security import generate_password_hash, check_password_hash

# Import PyMySQL to connect Flask with MariaDB.
import pymysql


# Create the Flask app.
app = Flask(__name__)
app.secret_key = "NorwayWorldCup2026!"  # Change this to a random secret key in production.


# Database connection settings.
DB = {
    "host": "localhost",
    "user": "helpdesk_user",
    "password": "StrongPassword123!",
    "database": "helpdesk",
    "cursorclass": pymysql.cursors.DictCursor
}


# Set up login management.
login_manager = LoginManager(app)
login_manager.login_view = "login"


# Connect to the MariaDB database.
def db():
    return pymysql.connect(**DB)


# Create database tables and default data.
def init_db():
    conn = db()
    cur = conn.cursor()

    # Users table stores login accounts.
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        role ENUM('user','admin') DEFAULT 'user'
    )
    """)

    # Departments table stores ticket categories.
    cur.execute("""
    CREATE TABLE IF NOT EXISTS departments (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL
    )
    """)

    # Tickets table stores help desk requests.
    cur.execute("""
    CREATE TABLE IF NOT EXISTS tickets (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        department_id INT,
        subject VARCHAR(255) NOT NULL,
        description TEXT NOT NULL,
        status ENUM('open','in_progress','closed') DEFAULT 'open',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (department_id) REFERENCES departments(id)
    )
    """)

    # Articles table stores knowledge base articles.
    cur.execute("""
    CREATE TABLE IF NOT EXISTS articles (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        content TEXT NOT NULL
    )
    """)

    # Create default admin account if it does not exist.
    cur.execute("SELECT * FROM users WHERE username=%s", ("admin",))
    if not cur.fetchone():
        cur.execute(
            "INSERT INTO users (username, password, role) VALUES (%s,%s,%s)",
            ("admin", generate_password_hash("admin123"), "admin")
        )

    # Add default departments if none exist.
    cur.execute("SELECT COUNT(*) AS total FROM departments")
    if cur.fetchone()["total"] == 0:
        cur.execute("""
        INSERT INTO departments (name)
        VALUES ('IT'), ('Network'), ('Software'), ('Hardware')
        """)

    conn.commit()
    conn.close()


# User class used by Flask-Login.
class User(UserMixin):
    def __init__(self, data):
        self.id = str(data["id"])
        self.username = data["username"]
        self.role = data["role"]


# Reload the logged-in user from the database.
@login_manager.user_loader
def load_user(user_id):
    conn = db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE id=%s", (user_id,))
    user = cur.fetchone()

    conn.close()

    return User(user) if user else None


# Main HTML layout used by every page.
BASE = """
<!doctype html>
<html>
<head>
<title>Help Desk</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>

<body>
<nav class="navbar navbar-dark bg-dark navbar-expand-lg">
<div class="container">
<a class="navbar-brand" href="/">Help Desk</a>

<div>
{% if current_user.is_authenticated %}
<a class="btn btn-sm btn-light" href="/tickets">Tickets</a>
<a class="btn btn-sm btn-light" href="/submit">Submit Ticket</a>
<a class="btn btn-sm btn-light" href="/kb">Knowledge Base</a>

{% if current_user.role == 'admin' %}
<a class="btn btn-sm btn-warning" href="/admin">Admin</a>
{% endif %}

<a class="btn btn-sm btn-danger" href="/logout">Logout</a>

{% else %}
<a class="btn btn-sm btn-light" href="/login">Login</a>
<a class="btn btn-sm btn-success" href="/register">Register</a>
{% endif %}
</div>

</div>
</nav>

<div class="container mt-4">

{% with messages = get_flashed_messages() %}
{% for msg in messages %}
<div class="alert alert-info">{{ msg }}</div>
{% endfor %}
{% endwith %}

{{ content|safe }}

</div>
</body>
</html>
"""


# Helper function to display pages inside the main layout.
def page(content, **kwargs):
    inner_page = render_template_string(content, **kwargs)
    return render_template_string(BASE, content=inner_page)


# Home page.
@app.route("/")
def home():
    return page("""
    <div class="p-5 bg-light rounded">
        <h1>IT Help Desk</h1>
        <p>Submit, track, and manage IT-related support tickets.</p>
    </div>
    """)


# Register page for new users.
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        conn = db()
        cur = conn.cursor()

        try:
            cur.execute(
                "INSERT INTO users (username, password) VALUES (%s,%s)",
                (
                    request.form["username"],
                    generate_password_hash(request.form["password"])
                )
            )

            conn.commit()
            flash("Account created. Please log in.")
            return redirect("/login")

        except pymysql.err.IntegrityError:
            flash("Username already exists.")

        finally:
            conn.close()

    return page("""
    <h2>Register</h2>

    <form method="post">
        <input class="form-control mb-2" name="username" placeholder="Username" required>
        <input class="form-control mb-2" name="password" type="password" placeholder="Password" required>
        <button class="btn btn-success">Register</button>
    </form>
    """)


# Login page for existing users.
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        conn = db()
        cur = conn.cursor()

        cur.execute("SELECT * FROM users WHERE username=%s", (request.form["username"],))
        user = cur.fetchone()

        conn.close()

        # Check if the username exists and the password is correct.
        if user and check_password_hash(user["password"], request.form["password"]):
            login_user(User(user))
            return redirect("/tickets")

        flash("Invalid login.")

    return page("""
    <h2>Login</h2>

    <form method="post">
        <input class="form-control mb-2" name="username" placeholder="Username" required>
        <input class="form-control mb-2" name="password" type="password" placeholder="Password" required>
        <button class="btn btn-primary">Login</button>
    </form>
    """)


# Logout route.
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")


# Page for users to submit a new ticket.
@app.route("/submit", methods=["GET", "POST"])
@login_required
def submit_ticket():
    conn = db()
    cur = conn.cursor()

    # Save the submitted ticket.
    if request.method == "POST":
        cur.execute("""
            INSERT INTO tickets (user_id, department_id, subject, description)
            VALUES (%s,%s,%s,%s)
        """, (
            current_user.id,
            request.form["department_id"],
            request.form["subject"],
            request.form["description"]
        ))

        conn.commit()
        conn.close()

        flash("Ticket submitted.")
        return redirect("/tickets")

    # Load departments for the dropdown menu.
    cur.execute("SELECT * FROM departments")
    departments = cur.fetchall()

    conn.close()

    return page("""
    <h2>Submit Ticket</h2>

    <form method="post">
        <input class="form-control mb-2" name="subject" placeholder="Subject" required>

        <select class="form-control mb-2" name="department_id">
            {% for d in departments %}
            <option value="{{ d.id }}">{{ d.name }}</option>
            {% endfor %}
        </select>

        <textarea class="form-control mb-2" name="description" placeholder="Describe the problem" required></textarea>

        <button class="btn btn-primary">Submit</button>
    </form>
    """, departments=departments)


# Page that displays tickets.
@app.route("/tickets")
@login_required
def tickets():
    conn = db()
    cur = conn.cursor()

    # Admins can see all tickets.
    if current_user.role == "admin":
        cur.execute("""
        SELECT tickets.*, users.username, departments.name AS department
        FROM tickets
        JOIN users ON tickets.user_id = users.id
        LEFT JOIN departments ON tickets.department_id = departments.id
        ORDER BY tickets.created_at DESC
        """)

    # Normal users only see their own tickets.
    else:
        cur.execute("""
        SELECT tickets.*, departments.name AS department
        FROM tickets
        LEFT JOIN departments ON tickets.department_id = departments.id
        WHERE user_id=%s
        ORDER BY created_at DESC
        """, (current_user.id,))

    tickets = cur.fetchall()
    conn.close()

    return page("""
    <h2>Tickets</h2>

    <table class="table table-bordered">
        <tr>
            <th>ID</th>
            <th>Subject</th>
            <th>Department</th>
            <th>Status</th>
            <th>Created</th>
        </tr>

        {% for t in tickets %}
        <tr>
            <td>{{ t.id }}</td>
            <td>{{ t.subject }}</td>
            <td>{{ t.department }}</td>
            <td>{{ t.status }}</td>
            <td>{{ t.created_at }}</td>
        </tr>
        {% endfor %}
    </table>
    """, tickets=tickets)


# Knowledge Base page.
@app.route("/kb")
@login_required
def kb():
    conn = db()
    cur = conn.cursor()

    # Get all knowledge base articles.
    cur.execute("SELECT * FROM articles")
    articles = cur.fetchall()

    conn.close()

    return page("""
    <h2>Knowledge Base</h2>

    {% for a in articles %}
    <div class="card mb-3">
        <div class="card-body">
            <h5>{{ a.title }}</h5>
            <p>{{ a.content }}</p>
        </div>
    </div>

    {% else %}
    <p>No articles yet.</p>
    {% endfor %}
    """, articles=articles)


# Admin dashboard.
@app.route("/admin", methods=["GET", "POST"])
@login_required
def admin():
    # Stop normal users from opening the admin page.
    if current_user.role != "admin":
        return "Access denied", 403

    conn = db()
    cur = conn.cursor()

    # Handle admin form submissions.
    if request.method == "POST":

        # Update ticket status.
        if "ticket_id" in request.form:
            cur.execute(
                "UPDATE tickets SET status=%s WHERE id=%s",
                (request.form["status"], request.form["ticket_id"])
            )

        # Add new knowledge base article.
        elif "title" in request.form:
            cur.execute(
                "INSERT INTO articles (title, content) VALUES (%s,%s)",
                (request.form["title"], request.form["content"])
            )

        conn.commit()

    # Count total tickets.
    cur.execute("SELECT COUNT(*) AS total FROM tickets")
    total = cur.fetchone()["total"]

    # Load all tickets for the admin dashboard.
    cur.execute("SELECT * FROM tickets ORDER BY created_at DESC")
    tickets = cur.fetchall()

    conn.close()

    return page("""
    <h2>Admin Dashboard</h2>

    <p><strong>Total tickets:</strong> {{ total }}</p>

    <h4>Update Ticket Status</h4>

    <form method="post" class="mb-4">
        <input class="form-control mb-2" name="ticket_id" placeholder="Ticket ID" required>

        <select class="form-control mb-2" name="status">
            <option value="open">Open</option>
            <option value="in_progress">In Progress</option>
            <option value="closed">Closed</option>
        </select>

        <button class="btn btn-warning">Update</button>
    </form>

    <h4>Add Knowledge Base Article</h4>

    <form method="post">
        <input class="form-control mb-2" name="title" placeholder="Article title" required>
        <textarea class="form-control mb-2" name="content" placeholder="Article content" required></textarea>
        <button class="btn btn-success">Add Article</button>
    </form>

    <h4 class="mt-4">Recent Tickets</h4>

    <table class="table table-bordered">
        <tr>
            <th>ID</th>
            <th>Subject</th>
            <th>Status</th>
            <th>Created</th>
        </tr>

        {% for t in tickets %}
        <tr>
            <td>{{ t.id }}</td>
            <td>{{ t.subject }}</td>
            <td>{{ t.status }}</td>
            <td>{{ t.created_at }}</td>
        </tr>
        {% endfor %}
    </table>
    """, total=total, tickets=tickets)


# Start the program.
if __name__ == "__main__":
    init_db()
    app.run(debug=True)

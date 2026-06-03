# IT Help Desk Web Application

## Project Description

This project is a simple IT Help Desk web application built with Flask, MariaDB, Flask-Login, PyMySQL, and Bootstrap.

The system allows users to create accounts, log in, submit IT support tickets, track their tickets, view knowledge base articles, and allows administrators to manage tickets and create support articles.

## Main Features

- User registration
- User login and logout
- Password hashing for safer password storage
- Ticket submission
- Ticket tracking
- Knowledge base article display
- Admin dashboard
- Ticket status updates
- Default departments
- Default admin account

## Technologies Used

- Python
- Flask
- Flask-Login
- MariaDB
- PyMySQL
- Werkzeug security
- Bootstrap 5

## Project File

The main application file is:

```text
app.py
```

This file contains the Flask web server, database connection, database table creation, user authentication, ticket pages, knowledge base page, and admin dashboard.

## Database Tables

The application creates the following tables automatically when it starts:

### users

Stores user accounts.

| Field | Description |
|---|---|
| id | Unique user ID |
| username | User login name |
| password | Hashed password |
| role | User role, either user or admin |

### departments

Stores help desk departments.

| Field | Description |
|---|---|
| id | Unique department ID |
| name | Department name |

### tickets

Stores support tickets submitted by users.

| Field | Description |
|---|---|
| id | Unique ticket ID |
| user_id | The user who submitted the ticket |
| department_id | The department assigned to the ticket |
| subject | Ticket subject |
| description | Ticket details |
| status | Ticket status |
| created_at | Date and time the ticket was created |

### articles

Stores knowledge base articles.

| Field | Description |
|---|---|
| id | Unique article ID |
| title | Article title |
| content | Article text |

## Requirements

Before running the project, install:

- Python 3
- MariaDB Server
- pip

Python packages needed:

```bash
pip install flask flask-login pymysql werkzeug
```

## MariaDB Setup

Open MariaDB:

```bash
sudo mariadb
```

Create the database and database user:

```sql
CREATE DATABASE helpdesk;

CREATE USER 'helpdesk_user'@'localhost' IDENTIFIED BY 'StrongPassword123!';

GRANT ALL PRIVILEGES ON helpdesk.* TO 'helpdesk_user'@'localhost';

FLUSH PRIVILEGES;

EXIT;
```

The database name, username, and password must match the settings in `app.py`:

```python
DB = {
    "host": "localhost",
    "user": "helpdesk_user",
    "password": "StrongPassword123!",
    "database": "helpdesk"
}
```

## How to Run the Application

Go to the project folder:

```bash
cd /home/stian/Documents/exam
```

Run the Flask application:

```bash
python app.py
```

Then open this address in a browser:

```text
http://127.0.0.1:5000
```

## Default Admin Login

The application automatically creates a default admin account if it does not already exist.

```text
Username: admin
Password: admin123
```

The admin user can:

- View the admin dashboard
- See total tickets
- Update ticket statuses
- Add knowledge base articles

## User Guide

### Register a New User

1. Open the website.
2. Click **Register**.
3. Enter a username and password.
4. Submit the form.
5. Log in with the new account.

### Submit a Ticket

1. Log in as a normal user.
2. Click **Submit Ticket**.
3. Enter a subject.
4. Choose a department.
5. Describe the problem.
6. Click **Submit**.

### Track Tickets

1. Log in.
2. Click **Tickets**.
3. View submitted tickets and their status.

### Use the Knowledge Base

1. Log in.
2. Click **Knowledge Base**.
3. Read available support articles.

### Use the Admin Dashboard

1. Log in with the admin account.
2. Click **Admin**.
3. Enter a ticket ID and choose a new status.
4. Click **Update**.
5. Add knowledge base articles using the article form.

## Website Routes

| Route | Purpose |
|---|---|
| `/` | Home page |
| `/register` | Create a new user account |
| `/login` | Log in |
| `/logout` | Log out |
| `/submit` | Submit a new ticket |
| `/tickets` | View tickets |
| `/kb` | View knowledge base |
| `/admin` | Admin dashboard |

## Ticket Status Options

Tickets can have one of these statuses:

- open
- in_progress
- closed

## Default Departments

The application automatically creates these departments:

- IT
- Network
- Software
- Hardware

## Troubleshooting

### Problem: ModuleNotFoundError

Install the missing packages:

```bash
pip install flask flask-login pymysql werkzeug
```

### Problem: Cannot connect to MariaDB

Check that MariaDB is running:

```bash
sudo systemctl status mariadb
```

Start MariaDB if needed:

```bash
sudo systemctl start mariadb
```

### Problem: Access denied for database user

Make sure the MariaDB username and password match the `DB` settings in `app.py`.

### Problem: Page does not open

Make sure the Flask app is running and open:

```text
http://127.0.0.1:5000
```

## Security Notes

This project is suitable for a beginner or school project. For production use, the following should be improved:

- Use a stronger secret key
- Store database passwords outside the code
- Add better error handling
- Add input validation
- Add CSRF protection
- Use separate HTML template files
- Disable debug mode before deployment

## Future Improvements

Possible improvements include:

- Separate templates into a `templates` folder
- Add ticket priority levels
- Add ticket comments
- Add file uploads for screenshots
- Add search for tickets
- Add user management for admins
- Add email notifications
- Add better dashboard statistics

## Summary

This Help Desk system provides the basic features needed for an IT support ticket application. Users can register, log in, submit tickets, and track their requests. Administrators can manage ticket statuses and create knowledge base articles.

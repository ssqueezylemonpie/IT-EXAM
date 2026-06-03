# Help Desk System Plan

## Project Goal

Create a web-based IT Help Desk system where users can log in, submit support tickets, track ticket progress, read knowledge base articles, and allow admins to manage tickets.

## Technologies

* Flask web server 
* MariaDB database 
* Bootstrap for design
* Apache for hosting later
* Python backend
* HTML templates

## Main Features

### 1. User Login

Users can register, log in, and log out. Passwords will be stored securely using password hashing.

### 2. Ticket Submission

Logged-in users can submit IT-related problems by entering a title, description, and department.

### 3. Ticket Tracking

Users can view their submitted tickets and check the current status: open, in progress, or closed.

### 4. Knowledge Base

The system will include helpful IT support articles for common problems such as password issues, network problems, and computer troubleshooting.

### 5. Admin Dashboard

Admins can view all submitted tickets, check ticket details, and update ticket statuses.

## Database Tables

### users

Stores user account information.

Fields:

* id
* username
* password
* role

### departments

Stores support department names.

Fields:

* id
* name

### tickets

Stores submitted support tickets.

Fields:

* id
* user_id
* department_id
* title
* description
* status
* created_at

## Development Steps

1. Create the project folder.
2. Install Flask and MariaDB connector.
3. Create the MariaDB database.
4. Create the users, departments, and tickets tables.
5. Build the login and registration system.
6. Build the ticket submission page.
7. Build the ticket tracking page.
8. Add a simple knowledge base page.
9. Build the admin dashboard.
10. Test the full system.
11. Improve the design with Bootstrap.
12. Prepare the project for Apache hosting.

## Expected Outcome

The final system will allow users to report IT problems online and allow admins to manage support requests from one dashboard.

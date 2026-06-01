# IT Help Desk System Project Plan

## Overview
This project is a web-based IT Help Desk System built with:

- Apache Web Server
- PHP
- MariaDB
- Bootstrap

The system allows users to submit and track IT support tickets, while administrators manage tickets and monitor system activity.

---

## Features

### User Login
- User authentication using email and password.
- Session management for logged-in users.

### Ticket Submission
- Users can create support tickets.
- Tickets include subject, department, and description.

### Ticket Tracking
- Users can view the status of their submitted tickets.
- Status options:
  - Open
  - In Progress
  - Closed

### Knowledge Base
- Displays common IT solutions and troubleshooting guides.
- Reduces repetitive support requests.

### Admin Dashboard
- View all tickets.
- Monitor ticket statistics.
- Update ticket status.

---

## Database Design

### users
Stores user information.

Fields:
- id
- name
- email
- password
- role

### departments
Stores support departments.

Fields:
- id
- name

### tickets
Stores support tickets.

Fields:
- id
- user_id
- department_id
- subject
- message
- status
- created_at

---

## System Structure

index.php
- Login page
- Ticket submission
- Ticket tracking
- Knowledge base
- Admin dashboard

MariaDB
- users table
- departments table
- tickets table

Bootstrap
- Responsive user interface

---

## Expected Outcome

Users can:
- Log in
- Submit tickets
- Track ticket status
- Read knowledge base articles

Administrators can:
- View all tickets
- Manage ticket status
- Monitor help desk activity
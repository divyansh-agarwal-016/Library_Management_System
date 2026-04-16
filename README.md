# UniLibrary

UniLibrary is a Flask-based library management system for students and librarians.  
It supports authentication, book browsing, issue requests, request approvals, and catalog management with a clean light/dark UI.

## Features

- Role-based login for students and librarians
- Student dashboard with request tracking
- Book catalog with department filtering
- Request books for a selected duration
- Librarian dashboard with approval/rejection workflow
- Add and delete books from the catalog
- SQLite database by default
- Modern responsive UI with dark mode support
- Persistent theme preference in browser localStorage

## Tech Stack

- Python 3.12+
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Werkzeug
- SQLite
- Jinja2 Templates
- HTML, CSS, Bootstrap 5

## Project Structure

```text
library_management/
├── run.py
├── seed.py
├── reset_db.py
├── requirement.txt
├── instance/
│   └── library.db
└── app/
    ├── __init__.py
    ├── config.py
    ├── extensions.py
    ├── models.py
    ├── static/
    │   └── css/
    │       └── style.css
    ├── auth/
    │   ├── __init__.py
    │   └── routes.py
    ├── student/
    │   ├── __init__.py
    │   └── routes.py
    ├── librarian/
    │   ├── __init__.py
    │   └── routes.py
    └── templates/
        ├── base.html
        ├── auth/
        │   ├── login.html
        │   └── register.html
        ├── student/
        │   ├── dashboard.html
        │   └── books.html
        └── librarian/
            ├── dashboard.html
            └── books.html
```

## Main Components

### run.py
Starts the Flask development server.

### seed.py
Creates tables and inserts default users and a sample book catalog.

### reset_db.py
Deletes the SQLite database and reseeds it from scratch.

### __init__.py
Application factory. Initializes the Flask app, database, login manager, and registers blueprints.

### config.py
Holds app configuration including the secret key and database path.

### extensions.py
Initializes shared Flask extensions like SQLAlchemy and LoginManager.

### models.py
Contains the database models:
- `User`
- `Book`
- `IssueRequest`

### auth
Authentication routes:
- login
- register
- logout

### student
Student features:
- dashboard
- browse books
- request books

### librarian
Librarian features:
- dashboard
- approve/reject requests
- manage catalog
- delete books

## Requirements

Install dependencies from:

```bash
requirement.txt
```

## Setup

### 1. Clone or open the project

```bash
cd /home/divyanshagarwal/Code/library_management
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirement.txt
```

## Database Initialization

The app uses SQLite by default.

Default database path:

```text
instance/library.db
```

To create the database and seed sample data:

```bash
python seed.py
```

This will:
- create all tables
- create the default librarian account
- create the default student account
- insert the sample book catalog

If you want to completely reset the database:

```bash
python reset_db.py
```

## Default Test Accounts

### Librarian

- Username: `Admin`
- Password: `Admin@123`

### Student

- Username: `john_doe`
- Password: `Student123!`

## Running the App

Start the development server:

```bash
python run.py
```

Then open:

```text
http://127.0.0.1:5000
```

## Available Pages

### Authentication
- `/login`
- `/register`
- `/logout`

### Student
- `/student/dashboard`
- `/student/books`
- `/student/request/<book_id>`

### Librarian
- `/librarian/dashboard`
- `/librarian/books`
- `/librarian/request/<req_id>/action`

## Usage Flow

### Student flow
1. Log in as a student.
2. Open the book catalog.
3. Filter books by department.
4. Request a book for 3, 5, or 7 days.
5. Track request status from the dashboard.

### Librarian flow
1. Log in as the librarian.
2. Review pending requests on the dashboard.
3. Approve or reject requests.
4. Manage the catalog by adding or deleting books.

## UI Features

- Responsive modern layout
- Light and dark mode
- Theme preference saved in localStorage
- Clean cards, tables, and catalog layout
- Styled login/register pages with a centered auth shell

## Development Notes

- The app uses the Flask application factory pattern.
- The database is created automatically when seeding or when the app starts with the configured SQLite path.
- If you change templates or CSS, refresh the browser to see updates.
- If login credentials appear outdated, rerun `python seed.py`.

## Troubleshooting

### 1. Import errors
Make sure the virtual environment is activated:

```bash
source .venv/bin/activate
```

### 2. Database file not found
Run:

```bash
mkdir -p instance
python seed.py
```

### 3. Login not working
Recreate the database data:

```bash
python reset_db.py
```

### 4. UI not updating
Hard refresh the browser:

```text
Ctrl + Shift + R
```
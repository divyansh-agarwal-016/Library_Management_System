# 📚 UniLibrary

**UniLibrary** is a robust, Flask-based library management system designed to streamline operations for students and librarians. It features a modern role-based interface, real-time request tracking, and comprehensive catalog management, all backed by a lightweight SQLite database.

---

## ✨ Features

### 🎓 For Students
- **Secure Access**: Dedicated login and registration.
- **Book Discovery**: Browse the full catalog with department filtering.
- **Borrowing System**: Request books for specific durations (3, 5, or 7 days).
- **Dashboard**: Track request statuses and viewing history.

### 🛠️ For Librarians
- **Admin Dashboard**: Overview of pending requests and catalog statistics.
- **Request Management**: Approve or reject student book requests with one click.
- **Catalog Control**: Add new books or delete obsolete entries.
- **User Oversight**: Manage the student user base.

### 🎨 General UI/UX
- **Responsive Design**: Works seamlessly on desktop and mobile devices.
- **Theme Toggle**: Switch between **Light** and **Dark** modes.
- **Persistent Settings**: UI preferences are saved via `localStorage`.
- **Clean Layouts**: Organized cards, data tables, and intuitive navigation.

---

## 🛠️ Tech Stack

| Component       | Technology                                      |
|-----------------|-------------------------------------------------|
| **Language**    | Python 3.12+                                    |
| **Framework**   | Flask 3.x                                       |
| **Database**    | SQLite                                          |
| **ORM**         | Flask-SQLAlchemy                                |
| **Auth**        | Flask-Login                                     |
| **Frontend**    | HTML5, CSS3, Bootstrap 5, Jinja2                |

---

## 📁 Project Structure

```text
library_management/
├── run.py                   # Application entry point (starts dev server)
├── seed.py                  # Database initialization script (creates tables + default data)
├── reset_db.py              # Database reset script (drops tables + reseeds data)
├── requirement.txt          # Python dependencies
├── instance/
│   └── library.db           # SQLite database file (generated automatically)
└── app/
    ├── __init__.py          # Application factory (creates app, registers blueprints)
    ├── config.py            # Configuration variables (secret key, DB URI)
    ├── extensions.py        # Shared extensions (db, login_manager)
    ├── models.py            # Database models (User, Book, IssueRequest)
    ├── auth/                # Authentication Blueprint
    │   ├── __init__.py
    │   └── routes.py        # Login, Register, Logout logic
    ├── student/             # Student Blueprint
    │   ├── __init__.py
    │   └── routes.py        # Dashboard, Books, Request logic
    ├── librarian/           # Librarian Blueprint
    │   ├── __init__.py
    │   └── routes.py        # Dashboard, Manage Books, Approve/Reject logic
    ├── templates/           # Jinja2 HTML templates
    │   ├── base.html        # Base layout with nav and theme logic
    │   ├── auth/            # Login & Register forms
    │   ├── student/         # Student dashboard & book list
    │   └── librarian/       # Librarian dashboard & admin views
    └── static/              # Global CSS and assets
        └── css/
            └── style.css    # Custom styling
```

---

## 🚀 Setup & Installation

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd library_management
```
*If you already have the files locally, simply navigate to the project folder.*

### 2. Create Virtual Environment
**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```
**Windows:**
```cmd
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirement.txt
```

---

## 💾 Database Initialization

The application uses SQLite. The database file (`instance/library.db`) is created automatically upon running the seed script.

### Initialize Database
Create tables and populate default accounts and sample books:
```bash
python seed.py
```

### Reset Database
If the database gets corrupted or you want a fresh start:
```bash
python reset_db.py
```
*This deletes the existing database and runs `seed.py` internally.*

---

## 🔑 Default Credentials

After running `seed.py`, use these accounts to test the system:

| Role      | Username   | Password      |
|-----------|------------|---------------|
| Librarian | `Admin`    | `Admin@123`   |
| Student   | `john_doe` | `Student123!` |

---

## ▶️ Running the Application

Start the Flask development server:
```bash
python run.py
```

Visit the application in your browser:
**[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 🗺️ Route Map

### Authentication
- `GET /login` — Login page
- `POST /login` — Process login
- `GET /register` — Registration page
- `POST /register` — Process registration
- `GET /logout` — End session

### Student Module
- `GET /student/dashboard` — View personal request stats and status
- `GET /student/books` — Browse catalog with filters
- `POST /student/request/<book_id>` — Submit a new book request

### Librarian Module
- `GET /librarian/dashboard` — View all pending and active requests
- `GET /librarian/books` — Manage book inventory (Add/Delete)
- `POST /librarian/request/<req_id>/action` — Approve or Reject a request

---

## 🔄 Usage Workflows

### 1. Student Borrowing Flow
1. **Login**: Access account as a student.
2. **Browse**: Go to the **Books** section and filter by department.
3. **Request**: Click "Request" on a book, select duration (3/5/7 days), and submit.
4. **Track**: Return to **Dashboard** to see if the request is Pending, Approved, or Rejected.

### 2. Librarian Admin Flow
1. **Login**: Access account as a librarian.
2. **Manage Requests**: Check **Dashboard** for pending requests. Click "Approve" or "Reject".
3. **Update Catalog**: Go to **Manage Books** to add new titles or remove old ones.

---

## 💡 Development Tips

- **Hot Reloading**: Flask's debug mode reloads the server on code changes.
- **Theme Persistence**: The dark mode toggle saves to browser `localStorage`.
- **Static Assets**: If CSS updates don't show, hard-refresh your browser (`Ctrl + F5` or `Cmd + Shift + R`).
- **Factory Pattern**: The app uses `create_app()` in `app/__init__.py` for modular setup.

---

## 🛟 Troubleshooting

| Problem                            | Solution                                                                                     |
|------------------------------------|----------------------------------------------------------------------------------------------|
| `ModuleNotFoundError: No module...`| Ensure the virtual environment is activated (`source .venv/bin/activate`).                   |
| Database not found                 | Run `mkdir -p instance` then `python seed.py`.                                               |
| Login failing / Invalid user       | The database users might be missing. Run `python reset_db.py` to recreate defaults.          |
| UI looks broken                    | Clear browser cache or hard refresh (`Ctrl + F5`). Ensure `bootstrap` is loading correctly.  |


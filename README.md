# 📚 JECRC UniLibrary — Library Management System

**UniLibrary** is a robust, Flask-based library management system designed to streamline operations for students and librarians. It features a modern role-based interface, real-time request tracking, QR code–based book management, and comprehensive catalog management — all backed by a lightweight SQLite database.

---

## ✨ Features

### 🎓 For Students
- **Secure Access**: Dedicated login and registration.
- **Book Discovery**: Browse the full catalog with department filtering.
- **Borrowing System**: Request books for specific durations (3, 5, or 7 days).
- **Dashboard**: Track request statuses and viewing history.

### 🛠️ For Librarians
- **Admin Dashboard**: Overview of pending requests, catalog statistics with charts.
- **Request Management**: Approve or reject student book requests with one click.
- **Catalog Control**: Add new books or delete obsolete entries.
- **QR Code Generation**: Auto-generated QR codes for each book.
- **User Oversight**: Manage the student user base.
- **Email Notifications**: SMTP-based email alerts for request approvals/rejections.

### 🎨 General UI/UX
- **Responsive Design**: Works seamlessly on desktop and mobile devices.
- **Theme Toggle**: Switch between **Light** and **Dark** modes.
- **Persistent Settings**: UI preferences are saved via `localStorage`.
- **Clean Layouts**: Organized cards, data tables, and intuitive navigation.

---

## 🛠️ Tech Stack

| Component       | Technology                                      |
|-----------------|-------------------------------------------------|
| **Language**    | Python 3.10+                                    |
| **Framework**   | Flask 3.x                                       |
| **Database**    | SQLite                                          |
| **ORM**         | Flask-SQLAlchemy                                |
| **Auth**        | Flask-Login                                     |
| **QR Codes**    | qrcode + Pillow                                 |
| **Email**       | Flask-Mail                                      |
| **Frontend**    | HTML5, CSS3, Bootstrap 5, Chart.js, Jinja2      |

---

## 📁 Project Structure

```text
Library_Management_System/
├── run.py                   # Application entry point (starts dev server)
├── seed.py                  # Database initialization script (creates tables + default data)
├── reset_db.py              # Database reset script (drops tables + reseeds data)
├── requirement.txt          # Python dependencies
├── .gitignore               # Git ignore rules
├── instance/
│   └── library.db           # SQLite database file (generated automatically)
└── app/
    ├── __init__.py          # Application factory (creates app, registers blueprints)
    ├── config.py            # Configuration variables (secret key, DB URI, mail settings)
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
    └── static/              # Global CSS, images, and assets
        └── css/
            └── style.css    # Custom styling
```

---

## 🚀 Prerequisites

Make sure you have the following installed before proceeding:

| Software   | Minimum Version | Check Command          |
|------------|-----------------|------------------------|
| **Python** | 3.10+           | `python --version`     |
| **pip**    | 21.0+           | `pip --version`        |
| **Git**    | 2.30+           | `git --version`        |

> **Note**: On some systems, use `python3` and `pip3` instead of `python` and `pip`.

---

## 📥 Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/Library_Management_System.git
cd Library_Management_System
```

*If you already have the files locally, simply navigate to the project folder.*

---

### 2. Create a Virtual Environment

<details>
<summary><strong>🪟 Windows (PowerShell)</strong></summary>

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

> **If you get an execution policy error**, run this first:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

</details>

<details>
<summary><strong>🪟 Windows (Command Prompt)</strong></summary>

```cmd
python -m venv venv
venv\Scripts\activate.bat
```

</details>

<details>
<summary><strong>🍎 macOS / 🐧 Linux</strong></summary>

```bash
python3 -m venv venv
source venv/bin/activate
```

</details>

You should see `(venv)` in your terminal prompt once activated.

---

### 3. Install Dependencies

```bash
pip install -r requirement.txt
```

This installs:
- `Flask` — Web framework
- `Flask-SQLAlchemy` — ORM for database management
- `Flask-Login` — User session management
- `Werkzeug` — WSGI toolkit
- `qrcode[pil]` — QR code generation
- `Pillow` — Image processing (for QR codes)
- `Flask-Mail` — Email notification support

---

## 💾 Database Setup

The application uses **SQLite** — no external database server needed. The database file (`instance/library.db`) is created automatically.

### Initialize Database (first time)

Create tables and populate with default accounts and sample books:

```bash
python seed.py
```

### Reset Database

If the database gets corrupted or you want a fresh start:

```bash
python reset_db.py
```

*This deletes the existing database and re-seeds it with fresh data.*

---

## ▶️ Running the Application

Start the Flask development server:

```bash
python run.py
```

You should see output like:

```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

Open your browser and visit: **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 🔑 Default Credentials

After running `seed.py`, use these accounts to test the system:

| Role        | Username   | Password      |
|-------------|------------|---------------|
| Librarian   | `Admin`    | `Admin@123`   |
| Student     | `john_doe` | `Student123!` |

---

## 🗺️ Route Map

### Authentication
| Method | Route         | Description           |
|--------|---------------|-----------------------|
| GET    | `/login`      | Login page            |
| POST   | `/login`      | Process login         |
| GET    | `/register`   | Registration page     |
| POST   | `/register`   | Process registration  |
| GET    | `/logout`     | End session           |

### Student Module
| Method | Route                       | Description                  |
|--------|-----------------------------|------------------------------|
| GET    | `/student/dashboard`        | View request stats & status  |
| GET    | `/student/books`            | Browse catalog with filters  |
| POST   | `/student/request/<book_id>`| Submit a new book request    |

### Librarian Module
| Method | Route                                | Description                  |
|--------|--------------------------------------|------------------------------|
| GET    | `/librarian/dashboard`               | View all requests            |
| GET    | `/librarian/books`                   | Manage book inventory        |
| POST   | `/librarian/request/<req_id>/action` | Approve or reject a request  |

---

## 🔄 Usage Workflows

### 1. Student Borrowing Flow
1. **Login** → Access your student account
2. **Browse** → Go to **Books** section and filter by department
3. **Request** → Click "Request" on a book, select duration (3/5/7 days), and submit
4. **Track** → Return to **Dashboard** to see if your request is Pending, Approved, or Rejected

### 2. Librarian Admin Flow
1. **Login** → Access your librarian account
2. **Manage Requests** → Check **Dashboard** for pending requests. Click "Approve" or "Reject"
3. **Update Catalog** → Go to **Manage Books** to add new titles or remove old ones

---

## 💡 Development Tips

- **Hot Reloading**: Flask's debug mode automatically reloads the server on code changes.
- **Theme Persistence**: The dark mode toggle saves preferences to browser `localStorage`.
- **Static Assets**: If CSS updates don't appear, hard-refresh your browser (`Ctrl + F5` / `Cmd + Shift + R`).
- **Factory Pattern**: The app uses `create_app()` in `app/__init__.py` for modular setup.

---

## 🛟 Troubleshooting

| Problem                                | Solution                                                                              |
|----------------------------------------|---------------------------------------------------------------------------------------|
| `ModuleNotFoundError: No module...`    | Ensure the virtual environment is activated. Look for `(venv)` in your terminal.      |
| Database not found                     | Run `python seed.py` to create and populate the database.                             |
| Login failing / Invalid user           | Run `python reset_db.py` to recreate default accounts.                                |
| UI looks broken                        | Clear browser cache or hard refresh (`Ctrl + F5`).                                    |
| PowerShell can't activate venv         | Run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` first.     |
| `venv\Scripts\activate` not recognized | Use `.\venv\Scripts\Activate.ps1` (PowerShell) or `venv\Scripts\activate.bat` (CMD).  |

---

## 📄 License

This project is open-source and available for educational purposes.

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

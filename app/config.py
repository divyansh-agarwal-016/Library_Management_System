import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
DEFAULT_DB_PATH = os.path.join(INSTANCE_DIR, "library.db")

# JECRC University departments
JECRC_DEPARTMENTS = [
    "Computer Science & Engineering",
    "Information Technology",
    "Artificial Intelligence & Machine Learning",
    "Data Science",
    "Cyber Security",
    "Electronics & Communication Engineering",
    "Electrical Engineering",
    "Mechanical Engineering",
    "Civil Engineering",
    "Computer Applications (BCA/MCA)",
    "Management Studies (BBA/MBA)",
    "Law",
    "Science (Physics)",
    "Science (Chemistry)",
    "Science (Mathematics)",
    "Biotechnology",
    "Microbiology",
    "Forensic Science",
    "Fashion Design",
    "Interior Design",
    "Journalism & Mass Communication",
    "Hospitality Management",
    "Physiotherapy",
    "Agriculture",
    "Commerce",
    "Arts & Humanities",
]


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "jecrc-library-secret-key-change-in-production")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", f"sqlite:///{DEFAULT_DB_PATH}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UNIVERSITY_NAME = "JECRC University"
    UNIVERSITY_SHORT = "JECRC"
    UNIVERSITY_TAGLINE = "Build Your World"
    LIBRARY_NAME = "JECRC University Library"
    FINE_PER_DAY = 5.0  # ₹5 per day

    # ── Email / SMTP Configuration ──────────────────────────────────
    # Set these environment variables before running the app.
    # Example (Gmail):
    #   set MAIL_SERVER=smtp.gmail.com
    #   set MAIL_PORT=587
    #   set MAIL_USERNAME=your-email@gmail.com
    #   set MAIL_PASSWORD=your-app-password
    #
    # Example (Outlook/Office365):
    #   set MAIL_SERVER=smtp.office365.com
    #   set MAIL_PORT=587
    #   set MAIL_USERNAME=your-email@outlook.com
    #   set MAIL_PASSWORD=your-password
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "true").lower() == "true"
    MAIL_USE_SSL = os.environ.get("MAIL_USE_SSL", "false").lower() == "true"
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER", "JECRC Library <library@jecrc.ac.in>")
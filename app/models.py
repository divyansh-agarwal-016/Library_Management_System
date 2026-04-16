from datetime import datetime, timedelta
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .extensions import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'student' or 'librarian'

    requests = db.relationship("IssueRequest", backref="student", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method="pbkdf2:sha256")

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(50), nullable=False)
    download_url = db.Column(db.String(300), nullable=True)
    is_available = db.Column(db.Boolean, default=True)

    requests = db.relationship("IssueRequest", backref="book", lazy=True)

class IssueRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)
    duration_days = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default="pending")  # pending, approved, rejected, returned
    requested_at = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=True)

    @property
    def is_overdue(self):
        if self.status != "approved" or not self.due_date:
            return False
        return datetime.utcnow() > self.due_date
from datetime import datetime, timedelta
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .extensions import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    registration_no = db.Column(db.String(30), unique=True, nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    department = db.Column(db.String(80), nullable=True)
    phone = db.Column(db.String(15), nullable=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'student', 'teacher', or 'librarian'

    requests = db.relationship("IssueRequest", backref="user", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method="pbkdf2:sha256")

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def max_books(self):
        """Maximum number of books a user can borrow simultaneously."""
        if self.role == "teacher":
            return 5
        return 3  # student

    @property
    def active_borrows(self):
        """Count of currently approved (active) borrows."""
        return IssueRequest.query.filter_by(user_id=self.id, status="approved").count()

    @property
    def can_borrow(self):
        return self.active_borrows < self.max_books


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(80), nullable=False)
    isbn = db.Column(db.String(20), nullable=True)
    publisher = db.Column(db.String(120), nullable=True)
    edition = db.Column(db.String(30), nullable=True)
    year = db.Column(db.Integer, nullable=True)
    total_copies = db.Column(db.Integer, default=1, nullable=False)
    download_url = db.Column(db.String(300), nullable=True)

    requests = db.relationship("IssueRequest", backref="book", lazy=True)

    @property
    def issued_copies(self):
        return IssueRequest.query.filter_by(book_id=self.id, status="approved").count()

    @property
    def available_copies(self):
        return max(0, self.total_copies - self.issued_copies)

    @property
    def is_available(self):
        return self.available_copies > 0


class IssueRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)
    duration_days = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default="pending")  # pending, approved, rejected, returned
    requested_at = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=True)
    returned_at = db.Column(db.DateTime, nullable=True)
    renewed = db.Column(db.Boolean, default=False)
    fine_amount = db.Column(db.Float, default=0.0)

    FINE_PER_DAY = 5.0  # ₹5 per day

    @property
    def is_overdue(self):
        if self.status != "approved" or not self.due_date:
            return False
        return datetime.utcnow() > self.due_date

    @property
    def overdue_days(self):
        if not self.is_overdue:
            return 0
        delta = datetime.utcnow() - self.due_date
        return max(0, delta.days)

    @property
    def calculated_fine(self):
        return round(self.overdue_days * self.FINE_PER_DAY, 2)

    @property
    def can_renew(self):
        """Can renew only once, and only if not yet overdue."""
        return self.status == "approved" and not self.renewed and not self.is_overdue


class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    author = db.relationship("User", backref="announcements")


class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)
    reserved_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default="waiting")  # waiting, notified, expired

    user = db.relationship("User", backref="reservations")
    book = db.relationship("Book", backref="reservations")
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from ..auth.routes import role_required
from ..models import Book, IssueRequest
from ..extensions import db

student_bp = Blueprint("student", __name__)

@student_bp.route("/dashboard")
@login_required
@role_required(["student"])
def dashboard():
    my_requests = IssueRequest.query.filter_by(student_id=current_user.id)\
                                    .order_by(IssueRequest.requested_at.desc()).all()
    stats = {
        "total": len(my_requests),
        "pending": sum(1 for req in my_requests if req.status == "pending"),
        "approved": sum(1 for req in my_requests if req.status == "approved"),
        "overdue": sum(1 for req in my_requests if req.is_overdue),
    }
    return render_template("student/dashboard.html", requests=my_requests, stats=stats)

@student_bp.route("/books")
@login_required
@role_required(["student"])
def books():
    dept = request.args.get("department", "All")
    available_departments = [
        row[0] for row in Book.query.with_entities(Book.department).distinct().order_by(Book.department).all()
    ]
    departments = ["All"] + available_departments

    if dept not in departments:
        dept = "All"

    query = Book.query
    if dept != "All":
        query = query.filter_by(department=dept)
    books = query.all()
    return render_template("student/books.html", books=books, departments=departments)

@student_bp.route("/request/<int:book_id>", methods=["POST"])
@login_required
@role_required(["student"])
def request_book(book_id):
    book = Book.query.get_or_404(book_id)
    duration = int(request.form.get("duration_days", 3))
    
    if not book.is_available:
        flash("This book is currently issued and unavailable.", "danger")
        return redirect(url_for("student.books"))
    
    existing = IssueRequest.query.filter_by(student_id=current_user.id, book_id=book_id, status="pending").first()
    if existing:
        flash("You already have a pending request for this book.", "warning")
        return redirect(url_for("student.books"))

    new_req = IssueRequest(student_id=current_user.id, book_id=book.id, duration_days=duration, status="pending")
    db.session.add(new_req)
    db.session.commit()
    flash(f"Request submitted for {book.title}. Awaiting librarian approval.", "success")
    return redirect(url_for("student.dashboard"))
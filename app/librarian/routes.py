from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from ..auth.routes import role_required
from ..models import Book, IssueRequest
from ..extensions import db
from datetime import datetime, timedelta

librarian_bp = Blueprint("librarian", __name__)

DEFAULT_DEPARTMENTS = [
    "Computer Science",
    "Electrical Engineering",
    "Chemical Engineering",
    "Psychology",
    "Mechanical Engineering",
    "Civil Engineering",
    "Business Administration",
    "Biology",
    "Mathematics",
    "Physics",
]

@librarian_bp.route("/dashboard")
@login_required
@role_required(["librarian"])
def dashboard():
    total_books = Book.query.count()
    issued = IssueRequest.query.filter_by(status="approved").count()
    pending = IssueRequest.query.filter_by(status="pending").count()
    overdue = IssueRequest.query.filter(IssueRequest.status == "approved", 
                                        IssueRequest.due_date < datetime.utcnow()).count()
    
    pending_requests = IssueRequest.query.filter_by(status="pending").all()
    return render_template("librarian/dashboard.html", 
                           stats={"total": total_books, "issued": issued, "pending": pending, "overdue": overdue},
                           pending_requests=pending_requests)

@librarian_bp.route("/books", methods=["GET", "POST"])
@login_required
@role_required(["librarian"])
def manage_books():
    existing_departments = {
        row[0] for row in Book.query.with_entities(Book.department).distinct().all()
    }
    departments = sorted(existing_departments.union(DEFAULT_DEPARTMENTS))

    if request.method == "POST":
        title = request.form.get("title")
        author = request.form.get("author")
        dept = request.form.get("department")
        url = request.form.get("download_url").strip() if request.form.get("download_url") else None
        
        new_book = Book(title=title, author=author, department=dept, download_url=url)
        db.session.add(new_book)
        db.session.commit()
        flash("Book added successfully.", "success")
        return redirect(url_for("librarian.manage_books"))
    
    books = Book.query.all()
    return render_template("librarian/books.html", books=books, departments=departments)

@librarian_bp.route("/request/<int:req_id>/action", methods=["POST"])
@login_required
@role_required(["librarian"])
def handle_request(req_id):
    req = IssueRequest.query.get_or_404(req_id)
    action = request.form.get("action")
    
    if action == "approve":
        if not req.book.is_available:
            flash("Book is no longer available.", "danger")
        else:
            req.status = "approved"
            req.due_date = datetime.utcnow() + timedelta(days=req.duration_days)
            req.book.is_available = False
            flash(f"Approved. Due date: {req.due_date.strftime('%Y-%m-%d')}", "success")
    elif action == "reject":
        req.status = "rejected"
        flash("Request rejected.", "info")
        
    db.session.commit()
    return redirect(url_for("librarian.dashboard"))

@librarian_bp.route("/books/<int:book_id>/delete", methods=["POST"])
@login_required
@role_required(["librarian"])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    if not book.is_available:
        flash("Cannot delete an issued book.", "warning")
    else:
        db.session.delete(book)
        db.session.commit()
        flash("Book removed from catalog.", "success")
    return redirect(url_for("librarian.manage_books"))
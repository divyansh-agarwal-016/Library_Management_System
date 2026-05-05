from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from ..auth.routes import role_required
from ..models import Book, IssueRequest, Announcement, Reservation
from ..extensions import db
from datetime import datetime, timedelta

teacher_bp = Blueprint("teacher", __name__)


@teacher_bp.route("/dashboard")
@login_required
@role_required(["teacher"])
def dashboard():
    my_requests = IssueRequest.query.filter_by(user_id=current_user.id)\
                                    .order_by(IssueRequest.requested_at.desc()).all()
    stats = {
        "total": len(my_requests),
        "pending": sum(1 for req in my_requests if req.status == "pending"),
        "approved": sum(1 for req in my_requests if req.status == "approved"),
        "overdue": sum(1 for req in my_requests if req.is_overdue),
        "total_fines": sum(req.calculated_fine for req in my_requests if req.is_overdue),
    }
    announcements = Announcement.query.filter_by(is_active=True)\
                                      .order_by(Announcement.created_at.desc()).limit(5).all()
    return render_template("teacher/dashboard.html",
                           requests=my_requests, stats=stats, announcements=announcements)


@teacher_bp.route("/books")
@login_required
@role_required(["teacher"])
def books():
    dept = request.args.get("department", "All")
    search_query = request.args.get("q", "").strip()

    available_departments = [
        row[0] for row in Book.query.with_entities(Book.department).distinct().order_by(Book.department).all()
    ]
    departments = ["All"] + available_departments

    if dept not in departments:
        dept = "All"

    query = Book.query
    if dept != "All":
        query = query.filter_by(department=dept)
    if search_query:
        search_term = f"%{search_query}%"
        query = query.filter(
            db.or_(
                Book.title.ilike(search_term),
                Book.author.ilike(search_term),
                Book.isbn.ilike(search_term),
            )
        )
    books = query.order_by(Book.title).all()
    return render_template("teacher/books.html", books=books, departments=departments,
                           search_query=search_query)


@teacher_bp.route("/request/<int:book_id>", methods=["POST"])
@login_required
@role_required(["teacher"])
def request_book(book_id):
    book = Book.query.get_or_404(book_id)
    duration = int(request.form.get("duration_days", 7))

    if duration not in (7, 14, 30):
        flash("Invalid duration selected.", "danger")
        return redirect(url_for("teacher.books"))

    if not book.is_available:
        flash("This book is currently unavailable. You can join the waitlist.", "danger")
        return redirect(url_for("teacher.books"))

    if not current_user.can_borrow:
        flash(f"You have reached the maximum borrow limit ({current_user.max_books} books).", "warning")
        return redirect(url_for("teacher.books"))

    existing = IssueRequest.query.filter_by(user_id=current_user.id, book_id=book_id, status="pending").first()
    if existing:
        flash("You already have a pending request for this book.", "warning")
        return redirect(url_for("teacher.books"))

    new_req = IssueRequest(user_id=current_user.id, book_id=book.id,
                           duration_days=duration, status="pending")
    db.session.add(new_req)
    db.session.commit()
    flash(f"Request submitted for \"{book.title}\". Awaiting librarian approval.", "success")
    return redirect(url_for("teacher.dashboard"))


@teacher_bp.route("/renew/<int:req_id>", methods=["POST"])
@login_required
@role_required(["teacher"])
def renew_book(req_id):
    req = IssueRequest.query.get_or_404(req_id)
    if req.user_id != current_user.id:
        flash("Unauthorized.", "danger")
        return redirect(url_for("teacher.dashboard"))
    if not req.can_renew:
        flash("This book cannot be renewed.", "warning")
        return redirect(url_for("teacher.dashboard"))

    req.due_date = req.due_date + timedelta(days=req.duration_days)
    req.renewed = True
    db.session.commit()
    flash(f"Book renewed. New due date: {req.due_date.strftime('%Y-%m-%d')}", "success")
    return redirect(url_for("teacher.dashboard"))


@teacher_bp.route("/reserve/<int:book_id>", methods=["POST"])
@login_required
@role_required(["teacher"])
def reserve_book(book_id):
    book = Book.query.get_or_404(book_id)
    if book.is_available:
        flash("This book is available — request it directly instead.", "info")
        return redirect(url_for("teacher.books"))

    existing = Reservation.query.filter_by(user_id=current_user.id, book_id=book_id, status="waiting").first()
    if existing:
        flash("You are already on the waitlist for this book.", "warning")
        return redirect(url_for("teacher.books"))

    reservation = Reservation(user_id=current_user.id, book_id=book_id)
    db.session.add(reservation)
    db.session.commit()
    flash(f"You have been added to the waitlist for \"{book.title}\".", "success")
    return redirect(url_for("teacher.books"))


@teacher_bp.route("/history")
@login_required
@role_required(["teacher"])
def history():
    all_requests = IssueRequest.query.filter_by(user_id=current_user.id)\
                                     .order_by(IssueRequest.requested_at.desc()).all()
    return render_template("teacher/history.html", requests=all_requests)


@teacher_bp.route("/profile", methods=["GET", "POST"])
@login_required
@role_required(["teacher"])
def profile():
    if request.method == "POST":
        phone = request.form.get("phone", "").strip() or None
        current_user.phone = phone
        db.session.commit()
        flash("Profile updated.", "success")
        return redirect(url_for("teacher.profile"))
    return render_template("teacher/profile.html")

from flask import Blueprint, render_template, request, flash, redirect, url_for, make_response, send_file
from flask_login import login_required, current_user
from ..auth.routes import role_required
from ..models import Book, IssueRequest, User, Announcement, Reservation
from ..extensions import db, mail
from ..config import JECRC_DEPARTMENTS
from datetime import datetime, timedelta
import csv
import io
import qrcode
from flask_mail import Message

librarian_bp = Blueprint("librarian", __name__)


@librarian_bp.route("/dashboard")
@login_required
@role_required(["librarian"])
def dashboard():
    total_books = Book.query.count()
    total_copies = db.session.query(db.func.sum(Book.total_copies)).scalar() or 0
    issued = IssueRequest.query.filter_by(status="approved").count()
    pending = IssueRequest.query.filter_by(status="pending").count()
    overdue = IssueRequest.query.filter(
        IssueRequest.status == "approved",
        IssueRequest.due_date < datetime.utcnow()
    ).count()
    total_users = User.query.filter(User.role != "librarian").count()

    pending_requests = IssueRequest.query.filter_by(status="pending")\
                                         .order_by(IssueRequest.requested_at.desc()).all()
    issued_books = IssueRequest.query.filter_by(status="approved")\
                                     .order_by(IssueRequest.due_date.asc()).all()

    # Stats for charts
    dept_stats = db.session.query(Book.department, db.func.count(Book.id))\
                           .group_by(Book.department).all()
    status_stats = db.session.query(IssueRequest.status, db.func.count(IssueRequest.id))\
                             .group_by(IssueRequest.status).all()

    return render_template("librarian/dashboard.html",
                           stats={"total": total_books, "total_copies": total_copies,
                                  "issued": issued, "pending": pending,
                                  "overdue": overdue, "users": total_users},
                           pending_requests=pending_requests,
                           issued_books=issued_books,
                           dept_stats=dept_stats,
                           status_stats=status_stats)


@librarian_bp.route("/books", methods=["GET", "POST"])
@login_required
@role_required(["librarian"])
def manage_books():
    existing_departments = {
        row[0] for row in Book.query.with_entities(Book.department).distinct().all()
    }
    departments = sorted(existing_departments.union(JECRC_DEPARTMENTS))

    search_query = request.args.get("q", "").strip()

    if request.method == "POST":
        title = request.form.get("title")
        author = request.form.get("author")
        dept = request.form.get("department")
        isbn = request.form.get("isbn", "").strip() or None
        publisher = request.form.get("publisher", "").strip() or None
        edition = request.form.get("edition", "").strip() or None
        year = request.form.get("year", "").strip()
        year = int(year) if year else None
        total_copies = int(request.form.get("total_copies", 1))
        url = request.form.get("download_url", "").strip() or None

        new_book = Book(title=title, author=author, department=dept, isbn=isbn,
                        publisher=publisher, edition=edition, year=year,
                        total_copies=total_copies, download_url=url)
        db.session.add(new_book)
        db.session.commit()
        flash("Book added successfully.", "success")
        return redirect(url_for("librarian.manage_books"))

    query = Book.query
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
    return render_template("librarian/books.html", books=books, departments=departments,
                           search_query=search_query)


@librarian_bp.route("/request/<int:req_id>/action", methods=["POST"])
@login_required
@role_required(["librarian"])
def handle_request(req_id):
    req = IssueRequest.query.get_or_404(req_id)
    action = request.form.get("action")

    if action == "approve":
        if not req.book.is_available:
            flash("No copies of this book are available.", "danger")
        else:
            req.status = "approved"
            req.due_date = datetime.utcnow() + timedelta(days=req.duration_days)
            flash(f"Approved. Due date: {req.due_date.strftime('%Y-%m-%d')}", "success")
            send_email_notification(
                subject=f"Book Approved: {req.book.title}",
                recipient_email=req.user.email,
                body=f"Dear {req.user.full_name},\n\nYour request for \"{req.book.title}\" has been approved.\nDue date: {req.due_date.strftime('%Y-%m-%d')}\n\n— JECRC University Library"
            )
    elif action == "reject":
        req.status = "rejected"
        flash("Request rejected.", "info")
        send_email_notification(
            subject=f"Book Request Rejected: {req.book.title}",
            recipient_email=req.user.email,
            body=f"Dear {req.user.full_name},\n\nYour request for \"{req.book.title}\" has been rejected.\nPlease contact the library for more details.\n\n— JECRC University Library"
        )

    db.session.commit()
    return redirect(url_for("librarian.dashboard"))


@librarian_bp.route("/request/<int:req_id>/return", methods=["POST"])
@login_required
@role_required(["librarian"])
def return_book(req_id):
    req = IssueRequest.query.get_or_404(req_id)
    if req.status != "approved":
        flash("Only approved (issued) books can be returned.", "warning")
        return redirect(url_for("librarian.dashboard"))

    req.status = "returned"
    req.returned_at = datetime.utcnow()

    # Calculate fine
    if req.is_overdue:
        req.fine_amount = req.calculated_fine
        flash(f"Book returned. Fine: ₹{req.fine_amount:.2f}", "warning")
    else:
        req.fine_amount = 0.0
        flash("Book returned successfully. No fine.", "success")

    # Check waitlist and notify
    waitlisted = Reservation.query.filter_by(book_id=req.book_id, status="waiting")\
                                  .order_by(Reservation.reserved_at.asc()).first()
    if waitlisted:
        waitlisted.status = "notified"
        db.session.commit()
        flash(f"Waitlisted user ({waitlisted.user.full_name}) has been notified.", "info")

    db.session.commit()
    return redirect(url_for("librarian.dashboard"))


@librarian_bp.route("/books/<int:book_id>/delete", methods=["POST"])
@login_required
@role_required(["librarian"])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    if book.issued_copies > 0:
        flash("Cannot delete a book that has issued copies.", "warning")
    else:
        db.session.delete(book)
        db.session.commit()
        flash("Book removed from catalog.", "success")
    return redirect(url_for("librarian.manage_books"))


@librarian_bp.route("/users")
@login_required
@role_required(["librarian"])
def manage_users():
    users = User.query.filter(User.role != "librarian").order_by(User.full_name).all()
    return render_template("librarian/users.html", users=users)


@librarian_bp.route("/announcements", methods=["GET", "POST"])
@login_required
@role_required(["librarian"])
def announcements():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        if title and content:
            ann = Announcement(title=title, content=content, author_id=current_user.id)
            db.session.add(ann)
            db.session.commit()
            flash("Announcement posted.", "success")
        else:
            flash("Title and content are required.", "warning")
        return redirect(url_for("librarian.announcements"))

    all_announcements = Announcement.query.order_by(Announcement.created_at.desc()).all()
    return render_template("librarian/announcements.html", announcements=all_announcements)


@librarian_bp.route("/announcements/<int:ann_id>/toggle", methods=["POST"])
@login_required
@role_required(["librarian"])
def toggle_announcement(ann_id):
    ann = Announcement.query.get_or_404(ann_id)
    ann.is_active = not ann.is_active
    db.session.commit()
    flash(f"Announcement {'activated' if ann.is_active else 'deactivated'}.", "info")
    return redirect(url_for("librarian.announcements"))


@librarian_bp.route("/announcements/<int:ann_id>/delete", methods=["POST"])
@login_required
@role_required(["librarian"])
def delete_announcement(ann_id):
    ann = Announcement.query.get_or_404(ann_id)
    db.session.delete(ann)
    db.session.commit()
    flash("Announcement deleted.", "success")
    return redirect(url_for("librarian.announcements"))


@librarian_bp.route("/export/books")
@login_required
@role_required(["librarian"])
def export_books_csv():
    books = Book.query.order_by(Book.title).all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Title", "Author", "Department", "ISBN", "Publisher",
                     "Edition", "Year", "Total Copies", "Available Copies"])
    for b in books:
        writer.writerow([b.id, b.title, b.author, b.department, b.isbn or "",
                         b.publisher or "", b.edition or "", b.year or "",
                         b.total_copies, b.available_copies])
    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=jecrc_library_books.csv"
    response.headers["Content-Type"] = "text/csv"
    return response


@librarian_bp.route("/export/history")
@login_required
@role_required(["librarian"])
def export_history_csv():
    all_requests = IssueRequest.query.order_by(IssueRequest.requested_at.desc()).all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "User Reg No", "User Name", "Role", "Book Title", "Duration (days)",
                     "Status", "Requested At", "Due Date", "Returned At", "Fine (₹)"])
    for r in all_requests:
        writer.writerow([r.id, r.user.registration_no, r.user.full_name, r.user.role,
                         r.book.title, r.duration_days, r.status,
                         r.requested_at.strftime("%Y-%m-%d %H:%M"),
                         r.due_date.strftime("%Y-%m-%d") if r.due_date else "",
                         r.returned_at.strftime("%Y-%m-%d %H:%M") if r.returned_at else "",
                         r.fine_amount])
    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=jecrc_library_history.csv"
    response.headers["Content-Type"] = "text/csv"
    return response


@librarian_bp.route("/reservations")
@login_required
@role_required(["librarian"])
def reservations():
    all_reservations = Reservation.query.order_by(Reservation.reserved_at.desc()).all()
    return render_template("librarian/reservations.html", reservations=all_reservations)


@librarian_bp.route("/books/<int:book_id>/qrcode")
@login_required
@role_required(["librarian"])
def book_qrcode(book_id):
    """Generate a QR code image for a book (encodes the book's catalog URL)."""
    book = Book.query.get_or_404(book_id)
    book_url = url_for("librarian.manage_books", _external=True) + f"#book-{book.id}"
    qr_data = f"JECRC Library | {book.title} by {book.author} | ISBN: {book.isbn or 'N/A'} | {book_url}"

    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=8, border=3)
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#c0392b", back_color="white")

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return send_file(buf, mimetype="image/png", download_name=f"qr_book_{book.id}.png")


def send_email_notification(subject, recipient_email, body):
    """Send an email notification. Silently fails if SMTP is not configured."""
    try:
        from flask import current_app
        if not current_app.config.get("MAIL_USERNAME"):
            return  # SMTP not configured, skip silently
        msg = Message(subject=subject, recipients=[recipient_email])
        msg.body = body
        mail.send(msg)
    except Exception:
        pass  # Don't crash the app if email fails
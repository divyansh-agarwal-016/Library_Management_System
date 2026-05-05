from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
from functools import wraps
from ..models import User
from ..extensions import db, login_manager
from ..config import JECRC_DEPARTMENTS

auth_bp = Blueprint("auth", __name__)


def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.role not in allowed_roles:
                flash("Unauthorized access.", "danger")
                return redirect(url_for("auth.login"))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        if current_user.role == "librarian":
            return redirect(url_for("librarian.dashboard"))
        elif current_user.role == "teacher":
            return redirect(url_for("teacher.dashboard"))
        else:
            return redirect(url_for("student.dashboard"))

    if request.method == "POST":
        registration_no = request.form.get("registration_no", "").strip().lower()
        password = request.form.get("password", "")
        user = User.query.filter_by(registration_no=registration_no).first()

        if user and user.check_password(password):
            login_user(user)
            if user.role == "librarian":
                return redirect(url_for("librarian.dashboard"))
            elif user.role == "teacher":
                return redirect(url_for("teacher.dashboard"))
            else:
                return redirect(url_for("student.dashboard"))
        flash("Invalid registration number or password.", "danger")
    return render_template("auth/login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        registration_no = request.form.get("registration_no", "").strip().lower()
        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        department = request.form.get("department", "").strip()
        phone = request.form.get("phone", "").strip() or None
        role = request.form.get("role", "student")
        password = request.form.get("password", "")

        # Validation
        errors = []
        if not registration_no:
            errors.append("Registration number is required.")
        if not full_name:
            errors.append("Full name is required.")
        if not email:
            errors.append("Email is required.")
        if not department:
            errors.append("Department is required.")
        if len(password) < 6:
            errors.append("Password must be at least 6 characters.")
        if role not in ("student", "teacher"):
            errors.append("Invalid role selected.")

        # ── Student-specific validation ─────────────────────────────
        # Reg no format: YYbranchROLL  e.g. 24bcon2125
        #   YY     = 2-digit admission year
        #   branch = 2-6 lowercase letters (branch code)
        #   ROLL   = 1-5 digit roll number
        # Email format: firstname.regNo@jecrcu.edu.in
        import re
        STUDENT_REG_PATTERN = re.compile(r"^\d{2}[a-z]{2,6}\d{1,5}$")
        STUDENT_EMAIL_PATTERN = re.compile(r"^[a-z]+\.\d{2}[a-z]{2,6}\d{1,5}@jecrcu\.edu\.in$")

        if role == "student":
            if registration_no and not STUDENT_REG_PATTERN.match(registration_no):
                errors.append(
                    "Invalid student registration number. "
                    "Format: YYbranchROLL (e.g. 24bcon2125)."
                )
            if email and not STUDENT_EMAIL_PATTERN.match(email):
                errors.append(
                    "Invalid student email. "
                    "Format: firstname.regNo@jecrcu.edu.in (e.g. utkarsh.24bcon2125@jecrcu.edu.in)."
                )
            # Cross-check: email must contain the registration number
            if registration_no and email and registration_no not in email:
                errors.append(
                    "Your email must contain your registration number "
                    f"({registration_no})."
                )

        # ── Teacher / Librarian: flexible for now ───────────────────
        # (formats will be added once confirmed from college)
        if role == "teacher":
            if email and not email.endswith("@jecrcu.edu.in"):
                errors.append("Teacher email must end with @jecrcu.edu.in.")

        if User.query.filter_by(registration_no=registration_no).first():
            errors.append("This registration number is already registered.")
        if User.query.filter_by(email=email).first():
            errors.append("This email is already registered.")

        if errors:
            for err in errors:
                flash(err, "warning")
        else:
            new_user = User(
                registration_no=registration_no,
                full_name=full_name,
                email=email,
                department=department,
                phone=phone,
                role=role,
            )
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for("auth.login"))
    return render_template("auth/register.html", departments=JECRC_DEPARTMENTS)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))
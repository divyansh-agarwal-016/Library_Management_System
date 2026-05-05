from app import create_app
from app.extensions import db
from app.models import User, Book

app = create_app()

ADMIN_REG = "jecrc-lib-001"
ADMIN_NAME = "Library Admin"
ADMIN_EMAIL = "library@jecrcu.edu.in"
ADMIN_PASSWORD = "Admin@123"

TEACHER_REG = "jecrc-t-0012"
TEACHER_NAME = "Dr. Rajesh Sharma"
TEACHER_EMAIL = "rajesh.sharma@jecrcu.edu.in"
TEACHER_PASSWORD = "Teacher@123"

STUDENT_REG = "24bcon2125"
STUDENT_NAME = "Utkarsh Goyal"
STUDENT_EMAIL = "utkarsh.24bcon2125@jecrcu.edu.in"
STUDENT_PASSWORD = "Student@123"

BOOKS_DATA = [
    {"title": "Introduction to Algorithms", "author": "Thomas H. Cormen", "department": "Computer Science & Engineering", "isbn": "978-0262033848", "publisher": "MIT Press", "total_copies": 3},
    {"title": "Clean Code", "author": "Robert C. Martin", "department": "Computer Science & Engineering", "isbn": "978-0132350884", "publisher": "Pearson", "total_copies": 2},
    {"title": "Design Patterns", "author": "Erich Gamma", "department": "Computer Science & Engineering", "isbn": "978-0201633610", "total_copies": 2},
    {"title": "The Pragmatic Programmer", "author": "Andrew Hunt", "department": "Computer Science & Engineering", "isbn": "978-0135957059", "total_copies": 2},
    {"title": "Artificial Intelligence: A Modern Approach", "author": "Stuart Russell", "department": "Artificial Intelligence & Machine Learning", "isbn": "978-0134610993", "publisher": "Pearson", "total_copies": 3},
    {"title": "Deep Learning", "author": "Ian Goodfellow", "department": "Artificial Intelligence & Machine Learning", "isbn": "978-0262035613", "publisher": "MIT Press", "total_copies": 2},
    {"title": "Pattern Recognition and Machine Learning", "author": "Christopher Bishop", "department": "Data Science", "isbn": "978-0387310732", "total_copies": 2},
    {"title": "Database System Concepts", "author": "Abraham Silberschatz", "department": "Information Technology", "isbn": "978-0078022159", "total_copies": 3},
    {"title": "Computer Networks", "author": "Andrew S. Tanenbaum", "department": "Information Technology", "isbn": "978-0132126953", "total_copies": 2},
    {"title": "Operating System Concepts", "author": "Abraham Silberschatz", "department": "Computer Science & Engineering", "isbn": "978-1119800361", "total_copies": 2},
    {"title": "Digital Logic Design", "author": "M. Morris Mano", "department": "Electronics & Communication Engineering", "total_copies": 2},
    {"title": "Microelectronic Circuits", "author": "Adel S. Sedra", "department": "Electronics & Communication Engineering", "isbn": "978-0199339136", "total_copies": 2},
    {"title": "Signals and Systems", "author": "Alan V. Oppenheim", "department": "Electronics & Communication Engineering", "total_copies": 2},
    {"title": "Power System Analysis", "author": "John J. Grainger", "department": "Electrical Engineering", "total_copies": 2},
    {"title": "Control Systems Engineering", "author": "Norman S. Nise", "department": "Electrical Engineering", "total_copies": 2},
    {"title": "Electric Machinery Fundamentals", "author": "Stephen J. Chapman", "department": "Electrical Engineering", "total_copies": 2},
    {"title": "Thermodynamics: An Engineering Approach", "author": "Yunus A. Cengel", "department": "Mechanical Engineering", "isbn": "978-0073398174", "total_copies": 3},
    {"title": "Fluid Mechanics", "author": "Frank M. White", "department": "Mechanical Engineering", "total_copies": 2},
    {"title": "Shigley's Mechanical Engineering Design", "author": "Richard G. Budynas", "department": "Mechanical Engineering", "total_copies": 2},
    {"title": "Structural Analysis", "author": "R.C. Hibbeler", "department": "Civil Engineering", "total_copies": 2},
    {"title": "Fundamentals of Geotechnical Engineering", "author": "Braja M. Das", "department": "Civil Engineering", "total_copies": 2},
    {"title": "Water Resources Engineering", "author": "Larry W. Mays", "department": "Civil Engineering", "total_copies": 2},
    {"title": "Principles of Marketing", "author": "Philip Kotler", "department": "Management Studies (BBA/MBA)", "isbn": "978-0134492513", "publisher": "Pearson", "total_copies": 3},
    {"title": "Financial Management", "author": "Eugene F. Brigham", "department": "Management Studies (BBA/MBA)", "total_copies": 2},
    {"title": "Organizational Behavior", "author": "Stephen P. Robbins", "department": "Management Studies (BBA/MBA)", "total_copies": 2},
    {"title": "The Indian Penal Code", "author": "Ratanlal & Dhirajlal", "department": "Law", "total_copies": 3},
    {"title": "Constitutional Law of India", "author": "J.N. Pandey", "department": "Law", "total_copies": 2},
    {"title": "Law of Contracts", "author": "Avtar Singh", "department": "Law", "total_copies": 2},
    {"title": "Campbell Biology", "author": "Lisa A. Urry", "department": "Biotechnology", "isbn": "978-0134093413", "total_copies": 2},
    {"title": "Molecular Biology of the Cell", "author": "Bruce Alberts", "department": "Biotechnology", "total_copies": 2},
    {"title": "Prescott's Microbiology", "author": "Joanne Willey", "department": "Microbiology", "total_copies": 2},
    {"title": "Calculus", "author": "James Stewart", "department": "Science (Mathematics)", "isbn": "978-1285740621", "total_copies": 3},
    {"title": "Linear Algebra", "author": "Gilbert Strang", "department": "Science (Mathematics)", "total_copies": 2},
    {"title": "Fundamentals of Physics", "author": "David Halliday", "department": "Science (Physics)", "isbn": "978-1118230718", "total_copies": 3},
    {"title": "Quantum Mechanics", "author": "David J. Griffiths", "department": "Science (Physics)", "total_copies": 2},
    {"title": "Organic Chemistry", "author": "Morrison & Boyd", "department": "Science (Chemistry)", "total_copies": 2},
    {"title": "Physical Chemistry", "author": "Peter Atkins", "department": "Science (Chemistry)", "total_copies": 2},
    {"title": "Forensic Science", "author": "Andrew R.W. Jackson", "department": "Forensic Science", "total_copies": 2},
    {"title": "Elements of Fashion and Apparel Design", "author": "Sumathi & Porkodi", "department": "Fashion Design", "total_copies": 2},
    {"title": "Interior Design Illustrated", "author": "Francis D.K. Ching", "department": "Interior Design", "total_copies": 2},
    {"title": "Mass Communication in India", "author": "Keval J. Kumar", "department": "Journalism & Mass Communication", "total_copies": 2},
    {"title": "Introduction to Hospitality", "author": "John R. Walker", "department": "Hospitality Management", "total_copies": 2},
    {"title": "Cyber Security Essentials", "author": "James Graham", "department": "Cyber Security", "total_copies": 2},
    {"title": "Data Science from Scratch", "author": "Joel Grus", "department": "Data Science", "isbn": "978-1492041139", "publisher": "O'Reilly", "total_copies": 2},
    {"title": "Let Us C", "author": "Yashavant Kanetkar", "department": "Computer Applications (BCA/MCA)", "total_copies": 3},
    {"title": "Python Programming", "author": "John Zelle", "department": "Computer Applications (BCA/MCA)", "total_copies": 2},
]


def seed():
    with app.app_context():
        db.create_all()
        added_users = 0

        # Admin / Librarian
        admin = User.query.filter_by(registration_no=ADMIN_REG).first()
        if not admin:
            admin = User(registration_no=ADMIN_REG, full_name=ADMIN_NAME,
                         email=ADMIN_EMAIL, role="librarian", department="Library")
            admin.set_password(ADMIN_PASSWORD)
            db.session.add(admin)
            added_users += 1
        else:
            admin.full_name = ADMIN_NAME
            admin.email = ADMIN_EMAIL
            admin.set_password(ADMIN_PASSWORD)

        # Teacher
        teacher = User.query.filter_by(registration_no=TEACHER_REG).first()
        if not teacher:
            teacher = User(registration_no=TEACHER_REG, full_name=TEACHER_NAME,
                           email=TEACHER_EMAIL, role="teacher",
                           department="Computer Science & Engineering")
            teacher.set_password(TEACHER_PASSWORD)
            db.session.add(teacher)
            added_users += 1

        # Student
        student = User.query.filter_by(registration_no=STUDENT_REG).first()
        if not student:
            student = User(registration_no=STUDENT_REG, full_name=STUDENT_NAME,
                           email=STUDENT_EMAIL, role="student",
                           department="Computer Science & Engineering")
            student.set_password(STUDENT_PASSWORD)
            db.session.add(student)
            added_users += 1

        # Books
        existing_books = {(b.title, b.author) for b in Book.query.all()}
        books_to_add = []
        for bdata in BOOKS_DATA:
            key = (bdata["title"], bdata["author"])
            if key not in existing_books:
                books_to_add.append(Book(**bdata))
                existing_books.add(key)

        if books_to_add:
            db.session.add_all(books_to_add)

        db.session.commit()
        print(f"Seed complete. Added {added_users} users, {len(books_to_add)} books.")


if __name__ == "__main__":
    seed()
from app import create_app
from app.extensions import db
from app.models import User, Book

app = create_app()

ADMIN_USERNAME = "Admin"
ADMIN_PASSWORD = "Admin@123"
ADMIN_EMAIL = "admin@university.edu"

BOOKS_DATA = [
    {"title": "Introduction to Algorithms", "author": "Thomas H. Cormen", "department": "Computer Science", "download_url": "https://mitpress.mit.edu/sites/default/files/sicp/full-text/book/book.html"},
    {"title": "Clean Code", "author": "Robert C. Martin", "department": "Computer Science", "download_url": None},
    {"title": "Design Patterns: Elements of Reusable Object-Oriented Software", "author": "Erich Gamma", "department": "Computer Science", "download_url": None},
    {"title": "The Pragmatic Programmer", "author": "Andrew Hunt", "department": "Computer Science", "download_url": "https://example.com/pragmatic.pdf"},
    {"title": "Structure and Interpretation of Computer Programs", "author": "Harold Abelson", "department": "Computer Science", "download_url": "https://mitpress.mit.edu/sites/default/files/sicp/full-text/book/book.html"},
    {"title": "Artificial Intelligence: A Modern Approach", "author": "Stuart Russell", "department": "Computer Science", "download_url": None},
    {"title": "Digital Logic Design", "author": "M. Morris Mano", "department": "Electrical Engineering", "download_url": None},
    {"title": "Microelectronic Circuits", "author": "Adel S. Sedra", "department": "Electrical Engineering", "download_url": None},
    {"title": "Power System Analysis", "author": "John J. Grainger", "department": "Electrical Engineering", "download_url": None},
    {"title": "Control Systems Engineering", "author": "Norman S. Nise", "department": "Electrical Engineering", "download_url": None},
    {"title": "The Art of Electronics", "author": "Paul Horowitz", "department": "Electrical Engineering", "download_url": "https://example.com/art_of_electronics.pdf"},
    {"title": "Organic Chemistry", "author": "Paula Yurkanis Bruice", "department": "Chemical Engineering", "download_url": None},
    {"title": "Chemical Engineering Thermodynamics", "author": "Y.V.C. Rao", "department": "Chemical Engineering", "download_url": None},
    {"title": "Process Dynamics and Control", "author": "Dale E. Seborg", "department": "Chemical Engineering", "download_url": None},
    {"title": "Transport Phenomena", "author": "R. Byron Bird", "department": "Chemical Engineering", "download_url": None},
    {"title": "Elementary Principles of Chemical Processes", "author": "Richard M. Felder", "department": "Chemical Engineering", "download_url": "https://example.com/chem_processes.pdf"},
    {"title": "Thinking, Fast and Slow", "author": "Daniel Kahneman", "department": "Psychology", "download_url": None},
    {"title": "Introduction to Psychology", "author": "James W. Kalat", "department": "Psychology", "download_url": None},
    {"title": "Social Psychology", "author": "David G. Myers", "department": "Psychology", "download_url": None},
    {"title": "Cognitive Psychology", "author": "Robert L. Solso", "department": "Psychology", "download_url": "https://example.com/cognitive.pdf"},
    {"title": "Database System Concepts", "author": "Abraham Silberschatz", "department": "Computer Science", "download_url": None},
    {"title": "Computer Networks", "author": "Andrew S. Tanenbaum", "department": "Computer Science", "download_url": "https://example.com/networks.pdf"},
    {"title": "Operating System Concepts", "author": "Abraham Silberschatz", "department": "Computer Science", "download_url": None},
    {"title": "Signals and Systems", "author": "Alan V. Oppenheim", "department": "Electrical Engineering", "download_url": None},
    {"title": "Electric Machinery Fundamentals", "author": "Stephen J. Chapman", "department": "Electrical Engineering", "download_url": "https://example.com/machinery.pdf"},
    {"title": "Thermodynamics: An Engineering Approach", "author": "Yunus A. Cengel", "department": "Mechanical Engineering", "download_url": None},
    {"title": "Fluid Mechanics", "author": "Frank M. White", "department": "Mechanical Engineering", "download_url": "https://example.com/fluid.pdf"},
    {"title": "Shigley's Mechanical Engineering Design", "author": "Richard G. Budynas", "department": "Mechanical Engineering", "download_url": None},
    {"title": "Manufacturing Engineering and Technology", "author": "Serope Kalpakjian", "department": "Mechanical Engineering", "download_url": None},
    {"title": "Structural Analysis", "author": "R.C. Hibbeler", "department": "Civil Engineering", "download_url": None},
    {"title": "Fundamentals of Geotechnical Engineering", "author": "Braja M. Das", "department": "Civil Engineering", "download_url": "https://example.com/geotech.pdf"},
    {"title": "Traffic and Highway Engineering", "author": "Nicholas J. Garber", "department": "Civil Engineering", "download_url": None},
    {"title": "Water Resources Engineering", "author": "Larry W. Mays", "department": "Civil Engineering", "download_url": None},
    {"title": "Principles of Marketing", "author": "Philip Kotler", "department": "Business Administration", "download_url": None},
    {"title": "Financial Management: Theory & Practice", "author": "Eugene F. Brigham", "department": "Business Administration", "download_url": "https://example.com/finance.pdf"},
    {"title": "Operations Management", "author": "Jay Heizer", "department": "Business Administration", "download_url": None},
    {"title": "Organizational Behavior", "author": "Stephen P. Robbins", "department": "Business Administration", "download_url": None},
    {"title": "Molecular Biology of the Cell", "author": "Bruce Alberts", "department": "Biology", "download_url": "https://www.ncbi.nlm.nih.gov/books/NBK21054/"},
    {"title": "Campbell Biology", "author": "Lisa A. Urry", "department": "Biology", "download_url": None},
    {"title": "Genetics: Analysis and Principles", "author": "Robert J. Brooker", "department": "Biology", "download_url": None},
    {"title": "Ecology: Concepts and Applications", "author": "Manuel C. Molles", "department": "Biology", "download_url": None},
    {"title": "Calculus", "author": "James Stewart", "department": "Mathematics", "download_url": None},
    {"title": "Linear Algebra and Its Applications", "author": "Gilbert Strang", "department": "Mathematics", "download_url": "https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/"},
    {"title": "Introduction to Probability", "author": "Dimitri P. Bertsekas", "department": "Mathematics", "download_url": None},
    {"title": "Discrete Mathematics and Its Applications", "author": "Kenneth H. Rosen", "department": "Mathematics", "download_url": None},
    {"title": "Fundamentals of Physics", "author": "David Halliday", "department": "Physics", "download_url": None},
    {"title": "Introduction to Quantum Mechanics", "author": "David J. Griffiths", "department": "Physics", "download_url": "https://example.com/quantum.pdf"},
    {"title": "Classical Mechanics", "author": "John R. Taylor", "department": "Physics", "download_url": None},
    {"title": "University Physics", "author": "Hugh D. Young", "department": "Physics", "download_url": None},
]

def seed():
    with app.app_context():
        db.create_all()
        added_users = 0
        admin = User.query.filter_by(username=ADMIN_USERNAME).first()
        if not admin:
            legacy_admin = User.query.filter_by(username="admin_lib").first()
            if legacy_admin:
                legacy_admin.username = ADMIN_USERNAME
                legacy_admin.email = ADMIN_EMAIL
                legacy_admin.role = "librarian"
                legacy_admin.set_password(ADMIN_PASSWORD)
            else:
                admin = User(username=ADMIN_USERNAME, email=ADMIN_EMAIL, role="librarian")
                admin.set_password(ADMIN_PASSWORD)
                db.session.add(admin)
                added_users += 1
        else:
            admin.email = ADMIN_EMAIL
            admin.role = "librarian"
            admin.set_password(ADMIN_PASSWORD)

        if not User.query.filter_by(username="john_doe").first():
            stu1 = User(username="john_doe", email="john@university.edu", role="student")
            stu1.set_password("Student123!")
            db.session.add(stu1)
            added_users += 1

        existing_books = {(book.title, book.author) for book in Book.query.all()}
        seen = set(existing_books)
        books_to_add = []
        for book in BOOKS_DATA:
            key = (book["title"], book["author"])
            if key in seen:
                continue
            books_to_add.append(Book(**book))
            seen.add(key)

        if books_to_add:
            db.session.add_all(books_to_add)

        db.session.commit()
        print(f"Seed complete. Added users: {added_users}, added books: {len(books_to_add)}")

if __name__ == "__main__":
    seed()
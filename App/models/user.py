from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    user_type = db.Column(db.String(50))

    __mapper_args__ = {
        "polymorphic_identity": "user",
        "polymorphic_on": user_type
    }

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def get_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "user_type": self.user_type
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)


class Student(User):
    __tablename__ = "students"

    id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    student_id = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(100))

    __mapper_args__ = {
        "polymorphic_identity": "student",
    }

    def __init__(self, username, password, student_id, email):
        super().__init__(username, password)
        self.student_id = student_id
        self.email = email

    def get_json(self):
        data = super().get_json()
        data.update({
            "student_id": self.student_id,
            "email": self.email
        })
        return data


class Staff(User):
    __tablename__ = "staff"

    id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    staff_id = db.Column(db.String(20), unique=True)

    __mapper_args__ = {
        "polymorphic_identity": "staff",
    }

    def __init__(self, username, password, staff_id):
        super().__init__(username, password)
        self.staff_id = staff_id

    def get_json(self):
        data = super().get_json()
        data.update({
            "staff_id": self.staff_id
        })
        return data


class Employer(User):
    __tablename__ = "employers"

    id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    employer_id = db.Column(db.String(20), unique=True)
    company = db.Column(db.String(100))

    __mapper_args__ = {
        "polymorphic_identity": "employer",
    }

    def __init__(self, username, password, employer_id, company):
        super().__init__(username, password)
        self.employer_id = employer_id
        self.company = company

    def get_json(self):
        data = super().get_json()
        data.update({
            "employer_id": self.employer_id,
            "company": self.company
        })
        return data

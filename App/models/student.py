from App.database import db
from App.models import (User, Shortlist, Internship)

class Student(User):
    __tablename__ = "students"

    student_id = db.Column(db.Integer, primary_key=True)
    shortlists = db.relationship("Shortlist", backref="student", lazy=True)

    __mapper_args__ = {
        "polymorphic_identity": "student",
    }

    def __init__(self, username, password, student_id):
        super().__init__(username, password)
        self.student_id = student_id

    def get_json(self):
        data = super().get_json()
        data.update({
            "student_id": self.student_id,
        })
        return data
    
    def create_student(username, password):
        newuser = Student(username=username, password=password)
        try:
            db.session.add(newuser)
            db.session.commit()
            return newuser
        except Exception as e:
            print(e)
            return None
        
    def get_all_student():
        return Student.query.all()
    
    def get_student_shortlisted_positions(student_id):
        shortlists = Shortlist.query.filter_by(student_id=student_id).all()
        results = []
        for shortlist in shortlists:
            internship = Internship.get_internship(shortlist.internship_id)
            if internship:
                results.append({
                    "Student ID" :student_id,
                    "Internship ID": internship.id,
                    "Title": internship.title,
                    "Status": internship.status  
                })
        return results
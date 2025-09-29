from App.database import db
from App.models import (User, Shortlist)

class Staff(User):
    __tablename__ = "staff"

    id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    staff_id = db.Column(db.Integer, unique=True)

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
    
    def create_staff(username, password):
        newuser = Staff(username=username, password=password)
        try:
            db.session.add(newuser)
            db.session.commit()
            return newuser
        except:
            return None

    def add_student_to_shortlist(student_id, internship_id):
        shortlist = Shortlist(student_id=student_id, internship_id=internship_id)
        try:
            db.session.add(shortlist)
            db.session.commit()
            return shortlist
        except Exception as e:
            print(e)
            return None
        
    def get_all_staff():
        return Staff.query.all()
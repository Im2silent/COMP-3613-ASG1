from App.database import db

class Shortlist(db.Model):
    __tablename__ = "shortlist"
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False)
    internship_id = db.Column(db.Integer, db.ForeignKey('internship.id'), nullable=False)

    def __init__(self, student_id, internship_id):
        self.student_id = student_id
        self.internship_id = internship_id

    def get_json(self):
        return {
            "Shortlist"
            "student_id ": self.student_id,
            "internship_id ": self.internship_id
        }
    
def get_all_shortlist():
    return Shortlist.query.all()

    
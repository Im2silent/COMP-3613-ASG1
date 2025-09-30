from App.database import db

class Internship(db.Model):
    __tablename__ = "internship"
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    shortlists = db.relationship("Shortlist", backref="internship", lazy=True)
    employer_id = db.Column(db.Integer, db.ForeignKey('employer.emp_id'), nullable=False)

    status = db.Column(db.String(20), default="pending")

    def accept(self):
        self.status = "accepted"

    def reject(self):
        self.status = "rejected"

    def __init__(self, title, employer_id):
        self.title = title
        self.employer_id = employer_id
    
    def get_json(self):
        return {
            "Internship ": self.title,
            "employer_id ": self.employer_id
        }
        
    def get_internship(id):
        return Internship.query.get(id)

def get_all_internship():
    return Internship.query.all()
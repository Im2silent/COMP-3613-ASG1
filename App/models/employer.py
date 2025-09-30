from App.database import db
from App.models import (Internship, User, Shortlist)


class Employer(User):
    __tablename__ = "employers"

    emp_id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(100))
    internships = db.relationship("Internship", backref="employer", lazy=True)

    __mapper_args__ = {
        "polymorphic_identity": "employer",
    }

    def __init__(self, username, password, emp_id, company):
        super().__init__(username, password)
        self.emp_id = emp_id
        self.company = company

    def get_json(self):
        data = super().get_json()
        data.update({
            "employer_id": self.emp_id,
            "company": self.company
        })
        return data
    
    def create_internship(self, title, description):
        internship = Internship(title=title, description=description)
        internship.employer_id = self.emp_id
        try:
            db.session.add(internship)
            db.session.commit()
            return internship
        except Exception as e:
            print(e)
            return None
        
    
    def create_employer(username, password, company):
        newuser = Employer(username=username, password=password, company=company)
        try:
            db.session.add(newuser)
            db.session.commit()
            return newuser
        except Exception as e:
            print(e)
            return None
        
def accept_shortlisted_student(shortlist_id):
    shortlist = Shortlist.query.get(shortlist_id)
    if not shortlist:
        return False
    internship = Internship.get_internship(shortlist.internship_id)
    if not internship:
        return False
    internship.accept()
    try:
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False

def reject_shortlisted_student(shortlist_id):
    shortlist = Shortlist.query.get(shortlist_id)
    if not shortlist:
        return False
    internship = Internship.get_internship(shortlist.internship_id)
    if not internship:
        return False
    internship.reject()
    try:
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False
Commands:

Student
flask student create <username, password, student_id>
flask student shortlist <student_id>

Staff
flask staff create <username, password, staff_id>
flask staff add <student_id,internship_id>

Employer
flask employer create <username, password, emp_id, company>
flask employer internship <emp_id, title,description>
flask employer accept <shortlist_id>
flask employer reject <shortlist_id>

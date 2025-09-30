import click, pytest, sys
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import (User, Student, Staff, Employer, Internship, Shortlist)
from App.models import (get_student_shortlisted_positions, add_student_to_shortlist, accept_shortlisted_student, reject_shortlisted_student)
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize )


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

'''
Student Commands
'''
stud_cli = AppGroup('student', help='Student object commands')

@stud_cli.command("create", help="Creates a student")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_student_command(username,password):
    student = Student.create_student(username, password)
    if student:
        print("Student Created!")
    else:
        print("Failed to create student.")

@stud_cli.command("shortlist", help="displays a students shortlisted positions")
@click.argument("student_id", default=-1)
def student_shortlist_command(student_id):
    shortlist = get_student_shortlisted_positions(student_id)
    if shortlist:
        for list in shortlist:
            print(list)
    else:
        print(f"No shortlisted internships found for student {student_id}")

app.cli.add_command(stud_cli)

'''
Staff Commands
'''
staff_cli = AppGroup('staff', help='Staff object commands')

@stud_cli.command("create", help="Creates a staff")
@click.argument("username", default="kyle")
@click.argument("password", default="kylepass")
def create_staff_command(username,password):
    staff = Staff.create_staff(username, password)
    if staff:
        print("Staff Created!")
    else:
        print("Failed to create staff.")

@stud_cli.command("add", help="Adds student to shortlist")
@click.argument("student_id", default="-1")
@click.argument("internship_id", default="-1")
def add_student_shortlist_command(student_id,internship_id):
    student = add_student_to_shortlist(student_id,internship_id)
    if student:
        print("Student added to shortlist!")
    else:
        print("Failed to add student to shortlist.")

app.cli.add_command(staff_cli)

'''
Employer Commands
'''
emp_cli = AppGroup('employer', help='Employer object commands')

@emp_cli.command("create", help="Creates a employer")
@click.argument("username", default="bob")
@click.argument("password", default="bobpass")
def create_employer_command(username,password):
    employer = Employer.create_employer(username, password)
    if employer:
        print("Employer Created!")
    else:
        print("Failed to create Employer.")

@emp_cli.command("internship", help="Creates an internship")
@click.argument("title", default="Programmer")
@click.argument("description", default="kylea fulltime unpaid programmer")
def create_internship_command(title,description):
    internship = Employer.create_internship(title, description)
    if internship:
        print("Internship Created!")
    else:
        print("Failed to create internship.")

@emp_cli.command("accept", help="accepts a shortlisted student")
@click.argument("shortlist_id", default="-1")
def accept_shortlist_command(shortlist_id):
    accept = accept_shortlisted_student(shortlist_id)
    if accept:
        print("Shortlisted accepted!")
    else:
        print("Error. Could not accept shortlisted student!")

@emp_cli.command("reject", help="rejects a shortlisted student")
@click.argument("shortlist_id", default="-1")
def reject_shortlist_command(shortlist_id):
    reject = reject_shortlisted_student(shortlist_id)
    if reject:
        print("Shortlisted rejected!")
    else:
        print("Error. Could not reject shortlisted student!")

app.cli.add_command(emp_cli)

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)
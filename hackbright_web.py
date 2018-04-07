"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    projects = hackbright.get_project_by_github(github)
    first = projects[0][0]
    last = projects[0][1]
    print projects

    html = render_template("student_info.html",
                           github=github,
                           projects=projects,
                           first=first,
                           last=last
                           )
    return html

    # return "{acct} is the GitHub account for {first} {last}".format(
    #     acct=github, first=first, last=last)


@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student.
    """

    return render_template("student_search.html")


@app.route("/student-new")
def create_new_student():
    """Show form for creating a new student
    """

    return render_template("student_new.html")


@app.route("/student-add", methods=["POST"])
def add_new_student():
    """Add a student to the database using information from student-new.
    """

    github = request.form.get('github')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')

    hackbright.make_new_student(first_name, last_name, github)

    return render_template("student_add.html", github=github,
                           first_name=first_name, last_name=last_name)


@app.route("/project/<title>")
def info_about_project(title):
    """Given a project title, makes a page that lists title, description, and
    max_grade for the project as well as all the students who have completed the
    project and the grade they received.
    """

    # title = request.args.get('title')


    project_title, description, max_grade = hackbright.get_project_by_title(title)

    # project_title = projects[0]
    # description = projects[1]
    # max_grade = projects[2]

    return render_template("project_info.html",
                           title=project_title,
                           description=description,
                           max_grade=max_grade)


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)

from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import mysql
from app import app

app = Blueprint('app', __name__)

@app.route('/')
def index():
    return redirect(url_for('app.students'))

# Define any other app-level routes here
# Add or update the route for the students page ("/students") as follows:
@app.route('/students')
def students():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students")
    students_data = cur.fetchall()

    cur.execute("SELECT * FROM colleges")  # Query the courses table
    colleges_data = cur.fetchall()
    
    cur.execute("SELECT * FROM courses")  # Query the courses table
    courses_data = cur.fetchall()

    cur.close()

    return render_template('students.html', students=students_data, courses=courses_data, colleges=colleges_data)


# Define a route for the "Courses" page
@app.route('/courses')
def courses():
    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM colleges")  # Query the courses table
    colleges_data = cur.fetchall()
    
    cur.execute("SELECT * FROM courses")  # Query the courses table
    courses_data = cur.fetchall()

    cur.close()

    return render_template('courses.html', courses=courses_data, colleges=colleges_data)


# Define a route for the "Colleges" page
@app.route('/colleges')
def colleges():
    # Implement the logic to fetch and display college information
    # Example: Query the database for college data
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM colleges")
    data = cur.fetchall()
    cur.close()

    return render_template('colleges.html', colleges=data)
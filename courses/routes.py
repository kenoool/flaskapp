from flask import Blueprint, render_template, current_app
from app import mysql

courses = Blueprint('courses', __name__)

@courses.route('/courses')
def courses_page():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM courses")
    course_data = cur.fetchall()
    cur.close()
    return render_template('courses.html', courses=course_data)

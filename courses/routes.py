from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import mysql

courses = Blueprint('courses', __name__)

@courses.route('/courses')
def courses_page():
    cur = mysql.connection.cursor()
    cur.execute("SELECT courses.course_id, courses.code, courses.name, colleges.name FROM courses JOIN colleges ON courses.id_college = colleges.college_id")
    course_data = cur.fetchall()
    cur.execute("SELECT * FROM colleges")
    college_data = cur.fetchall()
    cur.close()
    return render_template('courses.html', courses=course_data, colleges=college_data)

@courses.route('/insert_courses', methods=['POST'])
def insert_courses():
    if request.method == 'POST':
        courseDetails = request.form
        code = courseDetails['code']
        name = courseDetails['name']
        college_code = courseDetails['college_code']  # This is the selected college code from the form

        cur = mysql.connection.cursor()

        # Retrieve the college name based on the college_code
        cur.execute("SELECT name FROM colleges WHERE code = %s", (college_code,))
        college = cur.fetchone()

        if college:
            # College code exists, so you can insert the course with the retrieved college_name
            college_name = college[0]
            cur.execute("INSERT INTO courses (code, name, college_name) VALUES (%s, %s, %s)", (code, name, college_name))
            mysql.connection.commit()
            flash("Course Inserted Successfully")
        else:
            # College code doesn't exist, handle the error or show an appropriate message
            flash("Invalid College Code")

        cur.close()  # Close the cursor after the operation
        return redirect(url_for('courses.courses_page'))

@courses.route('/update_courses/<int:course_id>', methods=['POST'])
def update_courses(course_id):
    if request.method == 'POST':
        new_code = request.form['code']
        name = request.form['name']
        college_code = request.form['college_code'] 
        cur = mysql.connection.cursor()
        cur.execute("UPDATE courses SET code = %s, name = %s, college_name = %s WHERE course_id = %s", (new_code, name, college_code, course_id))
        mysql.connection.commit()
        flash("Course Updated Successfully")
        return redirect(url_for('courses.courses_page'))

@courses.route('/delete_courses/<int:course_id>', methods=['GET', 'POST'])
def delete_courses(course_id):
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM courses WHERE course_id = %s", (course_id,))
        mysql.connection.commit()
        flash("Course Deleted Successfully")
        cur.close()  # Close the cursor after the operation
    return redirect(url_for('courses.courses_page'))

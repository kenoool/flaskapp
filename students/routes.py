from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import mysql

students = Blueprint('students', __name__)

@students.route('/students')
def students_page():
    cur = mysql.connection.cursor()
    cur.execute("SELECT students.student_id, students.firstname, students.lastname, students.year, students.gender, courses.name FROM students JOIN courses ON students.id_course = courses.course_id")
    student_data = cur.fetchall()
    cur.execute("SELECT * FROM courses")
    course_data = cur.fetchall()
    cur.close()
    return render_template('students.html', students=student_data, courses=course_data)

@students.route('/insert_students', methods=['POST'])
def insert_students():
    if request.method == 'POST':
        userDetails = request.form
        id = userDetails['id']
        firstname = userDetails['firstname'][:10]
        lastname = userDetails['lastname']
        course_code = userDetails['course_code']
        year = userDetails['year']
        gender = userDetails['gender']

        # Insert course_code into the "students" table
        cur = mysql.connection.cursor()

        # Retrieve the course name based on the course_code
        cur.execute("SELECT name FROM courses WHERE code = %s", (course_code,))
        course = cur.fetchone()

        if course:
            # Student code exists, so you can insert the course with the retrieved course_name
            course_name = course[0]
            cur.execute("INSERT INTO students (id, firstname, lastname, course_name, year, gender) VALUES(%s, %s, %s, %s, %s, %s)", (id, firstname, lastname, course_name, year, gender))
            mysql.connection.commit()
            flash("Student Inserted Successfully")
        else:
            # Student code doesn't exist, handle the error or show an appropriate message
            flash("Invalid Student Code")
        
        cur.close()
        return redirect(url_for('students.students_page'))

@students.route('/update_students/<int:student_id>', methods=['POST','GET'])
def update_students(student_id):
    if request.method == 'POST':
        new_id = request.form['id']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        course_code = request.form['course_code']  # Update this line
        year = request.form['year']
        gender = request.form['gender']

        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE students
        SET id = %s, firstname=%s, lastname=%s, course_name=%s, year=%s, gender=%s
        WHERE student_id=%s
        """, (new_id, firstname, lastname, course_code, year, gender, student_id))
        flash("Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('students.students_page'))


@students.route('/delete_students/<int:student_id>', methods=['POST', 'GET'])
def delete_students(student_id):
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
        mysql.connection.commit()
        flash("Data Deleted Successfully")
        cur.close()
    return redirect(url_for('students.students_page'))

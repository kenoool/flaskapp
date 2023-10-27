from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import mysql

students = Blueprint('students', __name__)

@students.route('/students')
def students_page():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students")
    student_data = cur.fetchall()
    cur.close()
    return render_template('students.html', students=student_data)

@students.route('/insert_students', methods=['POST'])
def insert():
    if request.method == 'POST':
        flash("Data Inserted Successfully")
        userDetails = request.form
        id = userDetails['id']
        firstname = userDetails['firstname'][:10]
        lastname = userDetails['lastname']
        code = userDetails['code']
        year = userDetails['year']
        gender = userDetails['gender']

        # Insert course_code into the "students" table
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO students(id, firstname, lastname, code, year, gender) VALUES(%s, %s, %s, %s, %s, %s)", (id, firstname, lastname, code, year, gender))
        mysql.connection.commit()
        return redirect(url_for('students.students_page'))


@students.route('/update_students/<id>', methods=['POST','GET'])
def update(id):
    if request.method == 'POST':
        id_data = id
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        course_code = request.form['course_code']  # Update this line
        year = request.form['year']
        gender = request.form['gender']

        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE students
        SET firstname=%s, lastname=%s, course_code=%s, year=%s, gender=%s
        WHERE id=%s
        """, (firstname, lastname, course_code, year, gender, id_data))
        flash("Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('students.students_page'))


@students.route('/delete_students/<id_data>', methods=['POST', 'GET'])
def delete(id_data):
    flash("Data Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM students WHERE id = %s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('students.students_page'))

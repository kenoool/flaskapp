from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import mysql

colleges = Blueprint('colleges', __name__)

@colleges.route('/colleges')
def colleges_page():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM colleges")
    college_data = cur.fetchall()
    cur.close()
    return render_template('colleges.html', colleges=college_data)

@colleges.route('/insert_colleges', methods=['POST'])
def insert_colleges():
    if request.method == 'POST':
        userDetails = request.form
        code = userDetails['code']
        name = userDetails['name']

        cur = mysql.connection.cursor()

        # Check if the college code already exists
        cur.execute("SELECT code FROM colleges WHERE code = %s", (code,))
        result = cur.fetchone()

        if result is not None:
            flash("College code already exists")
            return redirect(url_for('colleges.colleges_page'))

        # If the college code doesn't exist, insert the new college
        cur.execute("INSERT INTO colleges(code, name) VALUES(%s, %s)", (code, name))
        mysql.connection.commit()
        flash("College Inserted Successfully")
        return redirect(url_for('colleges.colleges_page'))

@colleges.route('/update_colleges/<code>', methods=['POST'])
def update_colleges(code):
    if request.method == 'POST':
        new_code = request.form['code']
        name = request.form['name'] 
        cur = mysql.connection.cursor()
        cur.execute("UPDATE colleges SET code = %s, name = %s WHERE code = %s", (new_code, name, code))
        mysql.connection.commit()
        flash("College Updated Successfully")
        return redirect(url_for('colleges.colleges_page'))

@colleges.route('/delete_colleges/<code>', methods=['GET', 'POST'])
def delete_colleges(code):
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM colleges WHERE code = %s", (code,))
        mysql.connection.commit()
        flash("College Deleted Successfully")
    return redirect(url_for('colleges.colleges_page'))
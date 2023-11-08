from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import mysql

colleges = Blueprint('colleges', __name__)

@colleges.route('/colleges')
def colleges_page():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM colleges")
    colleges = cur.fetchall()
    cur.close()
    return render_template('colleges.html', colleges=colleges)

@colleges.route('/insert_colleges', methods=['POST'])
def insert_colleges():
    if request.method == 'POST':
        try:
            userDetails = request.form
            college_code = userDetails['code']
            college_name = userDetails['name']

            cur = mysql.connection.cursor()

            # Check if the college code already exists
            cur.execute("SELECT code FROM colleges WHERE code = %s", (college_code,))
            result = cur.fetchone()

            if result is not None:
                flash("College code already exists")
                return redirect(url_for('colleges.colleges_page'))

            # If the college code doesn't exist, insert the new college
            cur.execute("INSERT INTO colleges(code, name) VALUES(%s, %s)", (college_code, college_name))
            mysql.connection.commit()
            flash("College Inserted Successfully")
        except Exception as e:
            flash(f"Error inserting college: {str(e)}")

        cur.close()
        return redirect(url_for('colleges.colleges_page'))

@colleges.route('/update_colleges/<int:college_id>', methods=['POST'])
def update_colleges(college_id):
    if request.method == 'POST':
        try:
            new_code = request.form['code']
            name = request.form['name']
            cur = mysql.connection.cursor()
            cur.execute("UPDATE colleges SET code = %s, name = %s WHERE college_id = %s", (new_code, name, college_id))
            mysql.connection.commit()
            flash("College Updated Successfully")
        except Exception as e:
            flash(f"Error updating college: {str(e)}")

        return redirect(url_for('colleges.colleges_page'))
    
@colleges.route('/delete_colleges/<int:college_id>', methods=['GET', 'POST'])
def delete_colleges(college_id):
    if request.method == 'POST':
        try:
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM colleges WHERE college_id = %s", (college_id,))
            mysql.connection.commit()
            flash("College Deleted Successfully")
            cur.close()
        except Exception as e:
            flash(f"Error deleting college: {str(e)}")

    return redirect(url_for('colleges.colleges_page'))


@colleges.route('/search_colleges', methods=['POST'])
def search_colleges():
    if request.method == 'POST':
        search_input = request.form.get('search')
        cur = mysql.connection.cursor()
        # Perform a search by code or name and fetch matching colleges
        cur.execute("SELECT * FROM colleges WHERE code LIKE %s OR name LIKE %s", ('%' + search_input + '%', '%' + search_input + '%'))
        searched_colleges = cur.fetchall()
        cur.close()

        flash(f'Search results for "{search_input}": {len(searched_colleges)} colleges found')
        return render_template('colleges.html', colleges=searched_colleges)
    return redirect(url_for('colleges.colleges_page'))

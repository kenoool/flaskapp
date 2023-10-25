from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)
app.secret_key = "flash message "

# Configure db
with open('db.yaml', 'r') as yaml_file:
    db = yaml.load(yaml_file, Loader=yaml.FullLoader)

app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)


@app.route('/')
def index():
    return redirect(url_for('students'))

# Add or update the route for the students page ("/students") as follows:
@app.route('/students')
@app.route('/students')
def students():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students")
    student_data = cur.fetchall()
    
    cur.execute("SELECT * FROM courses")  # Query the courses table
    courses_data = cur.fetchall()

    cur.close()

    return render_template('students.html', students=student_data, courses=courses_data)


# Define a route for the "Courses" page
@app.route('/courses')
def courses():
    # Implement the logic to fetch and display course information
    # Example: Query the database for course data
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM courses")
    data = cur.fetchall()
    cur.close()

    return render_template('courses.html', courses=data)

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


@app.route('/insert', methods=['POST'])
def insert():
     if request.method == 'POST':
        flash("Data Inserted Successfully")
        # Fetch form data
        userDetails = request.form
        id = userDetails['id']
        firstname = userDetails['firstname'][:10]
        lastname = userDetails['lastname']
        course = userDetails['course']
        year = userDetails['year']
        gender = userDetails['gender']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO students(id, firstname, lastname, course, year, gender) VALUES(%s, %s, %s, %s, %s, %s)",(id, firstname, lastname, course, year, gender))
        mysql.connection.commit()
        return redirect(url_for('index'))

@app.route('/update/<id>', methods=['POST','GET'])
def update(id):
    if request.method == 'POST':
        id_data = id
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        course = request.form['course']
        year = request.form['year']
        gender = request.form['gender']

        cur = mysql.connection.cursor()
        cur.execute( """
        UPDATE students
        SET firstname=%s, lastname=%s, course=%s, year=%s, gender=%s
        WHERE id=%s
    
        """, (firstname,lastname,course,year,gender,id_data))   
        flash("Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('index'))
    
@app.route('/delete/<id_data>', methods=['POST', 'GET'])
def delete(id_data):
        flash("Data Deleted Successfully")
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM students WHERE id = %s", (id_data,))
        mysql.connection.commit()
        return redirect(url_for('index'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_term = request.form['search_term']
        field = request.form['search_field']
        query = f"SELECT * FROM student WHERE {field} LIKE %s"
        cur = mysql.connection.cursor()
        cur.execute(query, ('%' + search_term + '%',))
        results = cur.fetchall()
        cur.close()
        return render_template('index.html', students=results)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
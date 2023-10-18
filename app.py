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
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students")
    data = cur.fetchall()
    cur.close()

    return render_template('index.html', students= data)

@app.route('/insert', methods=['POST'])
def insert():
     if request.method == 'POST':
        flash("Data Inserted Successfully")
        # Fetch form data
        userDetails = request.form
        id = userDetails['id']
        firstname = userDetails['firstname']
        lastname = userDetails['lastname']
        course = userDetails['course']
        year = userDetails['year']
        gender = userDetails['gender']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO students(id, firstname, lastname, course, year, gender) VALUES(%s, %s, %s, %s, %s, %s)",(id, firstname, lastname, course, year, gender))
        mysql.connection.commit()
        return redirect(url_for('index'))


@app.route('/update',methods=['POST','GET'])
def update():

    if request.method == 'POST':
        id_data = request.form['id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE students
               SET name=%s, email=%s, phone=%s
               WHERE id=%s
            """, (name, email, phone, id_data))
        flash("Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('Index'))







if __name__ == '__main__':
    app.run(debug=True)
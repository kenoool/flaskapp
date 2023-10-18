from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)

# Configure db
with open('db.yaml', 'r') as yaml_file:
    db = yaml.load(yaml_file, Loader=yaml.FullLoader)

app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
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
        cur.close()
        return 'success'
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
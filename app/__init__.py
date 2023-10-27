from flask import Flask
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)
app.secret_key = "flash message"
app.template_folder = "templates"


# Configure the database
with open('db.yaml', 'r') as yaml_file:
    db = yaml.load(yaml_file, Loader=yaml.FullLoader)

app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

# Import and register Blueprints here
from app.routes import app as app_blueprint
app.register_blueprint(app_blueprint)

from students.routes import students
from courses.routes import courses
from colleges.routes import colleges
app.register_blueprint(students)
app.register_blueprint(courses)
app.register_blueprint(colleges)
# app/__init__.py

import cloudinary.uploader
import os
from flask import Flask
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from config import configure_cloudinary

mysql = MySQL()
csrf = CSRFProtect()

# Move the Cloudinary-related functions here

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py', silent=True)
    
    # Load configuration from environment variables
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['MYSQL_USER'] = os.getenv('DB_USER')
    app.config['MYSQL_PASSWORD'] = os.getenv('DB_PASSWORD')
    app.config['MYSQL_DB'] = os.getenv('DB_NAME')
    app.config['MYSQL_HOST'] = os.getenv('DB_HOST')
    app.config['MYSQL_PORT'] = int(os.getenv('DB_PORT', default=3306))
    app.config['BOOTSTRAP_SERVE_LOCAL'] = os.getenv('BOOTSTRAP_SERVE_LOCAL')
    app.config['UPLOAD_FOLDER'] = 'students/'

    mysql.init_app(app)
    csrf.init_app(app)
    configure_cloudinary(app)

    # ... register blueprints and other configurations

    from .students import students as students_blueprint
    app.register_blueprint(students_blueprint)
    from .courses import courses as courses_blueprint
    app.register_blueprint(courses_blueprint)
    from .colleges import colleges as colleges_blueprint
    app.register_blueprint(colleges_blueprint)

    return app

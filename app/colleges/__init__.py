from flask import Blueprint

colleges = Blueprint('colleges', __name__)

from . import routes


# Define any specific configuration for the 'colleges' Blueprint here

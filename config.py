from os import getenv
from dotenv import load_dotenv
import cloudinary
# Import the cloudinary.api for managing assets
import cloudinary.api
# Import the cloudinary.uploader for uploading assets
import cloudinary.uploader

load_dotenv()

SECRET_KEY = getenv("SECRET_KEY")
DB_NAME = getenv("DB_NAME")
DB_USER = getenv("DB_USER")
DB_PASSWORD = getenv("DB_PASSWORD")
DB_HOST = getenv("DB_HOST")
BOOTSTRAP_SERVE_LOCAL = getenv("BOOTSTRAP_SERVE_LOCAL")
DB_PORT = int(getenv("DB_PORT", default=3306))
UPLOAD_FOLDER = 'students/'

# Add a function to configure Cloudinary
def configure_cloudinary(app):
    cloudinary.config(
        cloud_name=getenv("CLOUDINARY_CLOUD_NAME"),
        api_key=getenv("CLOUDINARY_API_KEY"),
        api_secret=getenv("CLOUDINARY_API_SECRET"),
        secure=True  # Use secure URLs (HTTPS) in production
    )

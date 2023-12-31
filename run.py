from app import create_app
from dotenv import load_dotenv

load_dotenv('.env')  # take environment variables from .env.

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

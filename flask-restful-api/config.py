import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "a_default_secret_key"
    DEBUG = os.environ.get("DEBUG", "False") == "True"
    TESTING = os.environ.get("TESTING", "False") == "True"
    DATABASE_URI = os.environ.get("DATABASE_URI") or "sqlite:///app.db"
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", DATABASE_URI)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

from dotenv import load_dotenv
from os import getenv
from datetime import timedelta

load_dotenv()


class Config:
    DEBUG = True

    SECRET_KEY = getenv("SECRET_KEY")

    SQLALCHEMY_DATABASE_URI = getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SENDGRID_API_KEY = getenv("SENDGRID_API_KEY")
    SENDGRID_FROM_EMAIL = getenv("SENDGRID_FROM_EMAIL")

    SESSION_TYPE = "sqlalchemy"
    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = timedelta(weeks=1)

    SESSION_COOKIE_SECURE = getenv("SESSION_COOKIE_SECURE", "False") == "True"
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_HTTPONLY = True

    SESSION_CLEANUP_N_REQUESTS = 200

    SESSION_COOKIE_NAME = "__Secure-Backend-Project-Session"

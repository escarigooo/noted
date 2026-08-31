import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()


class Config:
    """Environment-driven application configuration."""

    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URI", "mysql+mysqlconnector://root@localhost/db_noted"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.getenv("FLASK_DEBUG", "False").lower() in {"true", "1", "yes"}

    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    MAIL_SERVER = os.getenv("MAIL_SERVER", "localhost")
    MAIL_PORT = int(os.getenv("MAIL_PORT", "1025"))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "False").lower() in {"true", "1", "yes"}
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "False").lower() in {"true", "1", "yes"}
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", "noted@example.com")

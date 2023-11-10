import os
import secrets
from flask_sqlalchemy import SQLAlchemy


class Config:
    SECRET_KEY = secrets.token_hex()
    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}@{os.environ['DB_HOST']}/{os.environ['DB_NAME']}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = secrets.token_hex()

    #JWT CONFIG
    #app.config["JWT_COOKIE_SECURE"] = False
    #app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
    #app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this in your code!
    #app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

class Preprodconfig:
    SECRET_KEY = secrets.token_hex()
    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.environ['PRE_DB_USER']}:{os.environ['PRE_DB_PASSWORD']}@{os.environ['PRE_DB_HOST']}/{os.environ['PRE_DB_NAME']}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


db = SQLAlchemy()
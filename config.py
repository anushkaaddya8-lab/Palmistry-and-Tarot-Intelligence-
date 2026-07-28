import os

class Config:
    SECRET_KEY = "mysecretkey"

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "ai_palmistry.db")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
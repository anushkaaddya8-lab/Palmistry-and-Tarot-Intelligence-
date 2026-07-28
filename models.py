from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    fullname = db.Column(db.String(150))
    age_group = db.Column(db.String(50))
    interest = db.Column(db.String(150))
    goal = db.Column(db.String(150))
    reading_preference = db.Column(db.String(100))

    def __repr__(self):
        return f"<User {self.username}>"

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(100))
    image_name = db.Column(db.String(200))

    life = db.Column(db.Text)
    career = db.Column(db.Text)
    love = db.Column(db.Text)
    fortune = db.Column(db.Text)

    created_at = db.Column(db.DateTime)

    prediction_type = db.Column(db.String(20))
    input_data = db.Column(db.String(200))
    result = db.Column(db.Text)
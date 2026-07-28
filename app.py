from flask import Flask
from config import Config
from models import db
from sqlalchemy import text


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

from routes import *

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    
    app.run(host="0.0.0.0", port=5000, debug=True)

    
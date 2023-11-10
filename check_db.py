from dotenv import load_dotenv
from flask import Flask


app = Flask(__name__)
load_dotenv()

from config import db, Preprodconfig
app.config.from_object(Preprodconfig)
db.init_app(app)
print(dir(db))

try:
    with app.app_context():
        db.create_all()
        print("Table Created")
except Exception as e:
    print(e)
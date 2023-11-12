from config import db

class Sea(db.Model):
    __tablename__ = 'seas'
    id_sea = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
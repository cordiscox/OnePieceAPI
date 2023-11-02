from config import db
from datetime import datetime

class Devil_Fruit(db.Model):
    __tablename__ = 'devil_fruits'
    id_devil_fruit = db.Column(db.Integer, primary_key=True)
    id_type = db.Column(db.Integer, db.ForeignKey('types.id_type'), unique=True) 
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(2000), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    #type = db.relationship('Type', back_populates='devil_fruits', uselist=False)

import models.enums as enums
from config import db
from datetime import datetime
from models.devil_fruit import Devil_Fruit
from models.crew import Crew
from models.sea import Sea

class Pirate(db.Model):
    __tablename__ = 'pirates'
    id_pirate = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_crew = db.Column(db.Integer, db.ForeignKey('crew.id_crew'))
    id_sea = db.Column(db.Integer, db.ForeignKey('sea.id_sea'))
    id_devil_fruit = db.Column(db.Integer, db.ForeignKey('devil_fruit.id_devil_fruit'))
    bountly = db.Column(db.Integer)
    name = db.Column(db.String(255), unique=True, nullable=False)
    image = db.Column(db.String(255))
    status = db.Column(enums.statuses_enum, nullable=False, default='Undetermined')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    crew = db.relationship('Crew', backref='pirates')
    sea = db.relationship('Sea', backref='pirates')
    devil_fruit = db.relationship('DevilFruit', backref='devil_fruit')
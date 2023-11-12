import models.enums as enums
from config import db
from datetime import datetime

class Marine(db.Model):
    __tablename__ = 'marines'
    id_marine = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_devil_fruit = db.Column(db.Integer, db.ForeignKey('devil_fruits.id_devil_fruit'))
    name = db.Column(db.String(255), unique=True, nullable=False)
    rank = db.Column(enums.marine_positions_enum, nullable=False, default='Undetermined')
    image = db.Column(db.String(255))
    status = db.Column(enums.statuses_enum, nullable=False, default='Undetermined')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    devil_fruit = db.relationship('Devil_Fruit', back_populates='marines')
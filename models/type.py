import models.enums as enums
from config import db
from datetime import datetime

class Type(db.Model):
    __tablename__ = 'types'
    id_type = db.Column(db.Integer, primary_key=True)
    type = db.Column(enums.fruit_types_enum, nullable=False)
    description = db.Column(db.String(2000), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
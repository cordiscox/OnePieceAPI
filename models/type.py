from app import db
from datetime import datetime

class Type(db.Model):
    __tablename__ = 'types'
    id_type = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(2000), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    devil_fruit = db.relationship('Devil_Fruit', back_populates='type')
    
    #def __init__(self, type, description, created_at, updated_at):
    #    self.name = name
    #    self.email = email

    #def __repr__(self):
    #    return f'<User {self.name!r}>'
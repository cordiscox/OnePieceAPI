import models.enums as enums
from config import db
from datetime import datetime
from models.devil_fruit import Devil_Fruit

class Type(db.Model):
    __tablename__ = 'types'
    id_type = db.Column(db.Integer, primary_key=True)
    '''type = db.Column(db.Enum(
        'Zoan', 'Zoan Ancient', 'Zoan Mythical', 'Zoan Artificial', 'Paramecia', 'Logia', 'Undetermined', name='fruit_types')
        , nullable=False)'''
    type = db.Column(enums.fruit_types_enum, nullable=False)
    description = db.Column(db.String(2000), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    
    devil_fruit = db.relationship('Devil_Fruit', back_populates='type')
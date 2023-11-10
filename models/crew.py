from config import db

class Crew(db.Model):
    __tablename__ = 'crews'
    id_crew = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    pirates = db.relationship('Pirate', backref='crew')
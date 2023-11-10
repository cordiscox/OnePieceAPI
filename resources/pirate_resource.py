from flask import jsonify, request
from flask_restful import Resource
from models.pirate import Pirate
from app import db
from sqlalchemy.exc import IntegrityError 
from flask_jwt_extended import jwt_required

# Agrega más argumentos según las columnas de tu modelo

class PirateListResource(Resource):
    def get(self):
        pirates = Pirate.query.all()
        return [{'id': pirate.id_pirate, 'name': pirate.name, 'bountly': pirate.bountly, 'status': pirate.status} for pirate in pirates]

    def post(self):
        args = parser.parse_args()
        pirate = Pirate(name=args['name'], bountly=args['bountly'], status='Alive')
        # Agrega más atributos según las columnas de tu modelo
        db.session.add(pirate)
        db.session.commit()
        return {'message': 'Pirata creado exitosamente', 'name': pirate.name}, 201

class PirateResource(Resource):
    def get(self, pirate_id):
        pirate = Pirate.query.get(pirate_id)
        if pirate:
            return {'id': pirate.id_pirate, 'name': pirate.name, 'bountly': pirate.bountly, 'status': pirate.status}
        else:
            return {'message': 'Pirata no encontrado'}, 404

    def put(self, pirate_id):
        args = parser.parse_args()
        pirate = Pirate.query.get(pirate_id)
        if pirate:
            pirate.name = args['name']
            pirate.bountly = args['bountly']
            # Actualiza más atributos según las columnas de tu modelo
            db.session.commit()
            return {'message': 'Pirata actualizado exitosamente', 'name': pirate.name}
        else:
            return {'message': 'Pirata no encontrado'}, 404

    def delete(self, pirate_id):
        pirate = Pirate.query.get(pirate_id)
        if pirate:
            db.session.delete(pirate)
            db.session.commit()
            return {'message': 'Pirata eliminado exitosamente'}
        else:
            return {'message': 'Pirata no encontrado'}, 404

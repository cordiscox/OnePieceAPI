from app import logger
from config import db
from flask import jsonify, abort
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from models.pirate import Pirate
from models.crew import Crew
from models.sea import Sea
from models.devil_fruit import Devil_Fruit
from webargs import fields
from webargs.flaskparser import use_args
from sqlalchemy.sql import text
from models.enums import Statuses

pirate_args = {
    'id_crew': fields.Int(required=True),
    'id_sea': fields.Int(required=True),
    'id_devil_fruit': fields.Int(required=True),
    'bountly': fields.Int(required=True),
    'name': fields.Str(required=True),
    'image': fields.Str(required=False),
    'status': fields.Enum(Statuses, required=False)
}


class PirateListResource(Resource):
    def get(self):
        pirates = Pirate.query.all()
        output = []
        for pirate in pirates:
            output.append({
                'id_pirate': pirate.id_pirate, 
                'id_crew': pirate.id_crew, 
                'id_sea': pirate.id_sea, 
                'id_devil_fruit': pirate.id_devil_fruit,
                'bountly': pirate.bountly,
                'name': pirate.name,
                'image': pirate.image,
                'status': pirate.status
                })
        return jsonify({'Pirates': output})

    #@jwt_required()
    @use_args(pirate_args)
    def post(self, args):
        id_crew = args['id_crew'], 
        id_sea = args['id_sea'], 
        id_devil_fruit = args['id_devil_fruit'],
        bountly = args['bountly'],
        name = args['name'],
        image = args['image'],
        status = args['status']
        
        #Validations
        check_crew = Crew.query.get(id_crew)
        if not check_crew:
            abort(404, description=f'Crew with id {id_crew} not exists')
        
        check_sea = Sea.query.get(id_sea)
        if not check_sea:
            abort(404, description=f'Sea with id {id_sea} not exists')

        check_devil_fruit= Devil_Fruit.query.get(id_devil_fruit)
        if not check_devil_fruit:            
            abort(404, description=f'Devil Fruit with {id_devil_fruit} not exists')

        #Insert
        exist_pirate = Pirate.query.filter_by(name=name).first()
        if not exist_pirate:
            new_pirate = Pirate(id_crew=id_crew,
                                id_sea=id_sea,
                                id_devil_fruit= id_devil_fruit,
                                bountly=bountly,
                                name=name,
                                image=image,
                                status=status)
            db.session.add(new_pirate)
            db.session.commit()
            return jsonify({'message': f'Pirate {new_pirate.name} created successfully'})
        else:
            abort(404, description=f'Pirate {new_pirate.name} already exists')

        
"""
class PirateResource(Resource):
    def get(self, pirate_id):
        pirate = Pirate.query.get(pirate_id)
        if pirate:
            return {'id': pirate.id_pirate, 'name': pirate.name, 'bountly': pirate.bountly, 'status': pirate.status}
        else:
            return {'message': 'Pirata no encontrado'}, 404
        

    @jwt_required()
    @use_args(pirate_args)
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


    @jwt_required()
    @use_args(pirate_args)
    def delete(self, pirate_id):
        pirate = Pirate.query.get(pirate_id)
        if pirate:
            db.session.delete(pirate)
            db.session.commit()
            return {'message': 'Pirata eliminado exitosamente'}
        else:
            return {'message': 'Pirata no encontrado'}, 404
"""
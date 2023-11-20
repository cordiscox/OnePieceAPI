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
from models.enums import Statuses

status = Statuses.Statuses()

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
                'crew': pirate.crew.name, 
                'sea': pirate.sea.name, 
                'devil_fruit': pirate.devil_fruit.name,
                'bountly': pirate.bountly,
                'name': pirate.name,
                'image': pirate.image,
                'status': pirate.status
                })
        return jsonify({'Pirates': output})

    @jwt_required()
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

        if status.value not in Statuses.Statuses():
            abort(404, description='status not in enumeration')

        #Insert
        exist_pirate = Pirate.query.filter_by(name=name).first()
        if not exist_pirate:
            new_pirate = Pirate(id_crew=id_crew,
                                id_sea=id_sea,
                                id_devil_fruit= id_devil_fruit,
                                bountly=bountly,
                                name=name,
                                image=image,
                                status=status.value)
            db.session.add(new_pirate)
            db.session.commit()
            return jsonify({'message': f'Pirate {new_pirate.name} created successfully'})
        else:
            abort(404, description=f'Pirate {new_pirate.name} already exists')

        

class PirateResource(Resource):
    def get(self, id_pirate):
        pirate = Pirate.query.get(id_pirate)
        if pirate:
            pirate = {
                'id_pirate': pirate.id_pirate, 
                'crew': pirate.crew.name, 
                'sea': pirate.sea.name, 
                'devil_fruit': pirate.devil_fruit.name,
                'bountly': pirate.bountly,
                'name': pirate.name,
                'image': pirate.image,
                'status': pirate.status 
            }
            return jsonify({'Pirate': pirate})
        else:
            return {'message': 'Pirate not exists'}, 404
        

    @jwt_required()
    @use_args(pirate_args)
    def put(self, args, id_pirate):
        id_crew = args['id_crew'], 
        id_sea = args['id_sea'], 
        id_devil_fruit = args['id_devil_fruit'],
        bountly = args['bountly'],
        name = args['name'],
        image = args['image'],
        status = args['status']

        pirate = Pirate.query.get(id_pirate)
        if not pirate:
            abort(404, description='Pirate not found')

        crew = Crew.query.get(id_crew)
        if not crew:
            abort(404, description='Crew not found')

        sea = Sea.query.get(id_sea)
        if not sea:
            abort(404, description='Sea not found')
        
        devil_fruit = Devil_Fruit.query.get(id_devil_fruit)
        if not devil_fruit:
            abort(404, description='Devil Fruit not found')
            
        if status.value not in Statuses.Statuses():
            abort(404, description='status not in enumeration')
                  
        if bountly and name and image:
            pirate.id_crew = id_crew,
            pirate.id_sea = id_sea, 
            pirate.id_devil_fruit = id_devil_fruit,
            pirate.bountly = bountly,
            pirate.name = name,
            pirate.image = image,
            pirate.status = status.value
            db.session.commit()
            return jsonify({'message': 'Pirate updated successfully'})
        else:
            abort(404, description='Args cannot be empty')


    @jwt_required()
    @use_args(pirate_args)
    def delete(self, id_pirate):
        pirate = Pirate.query.get(id_pirate)
        if pirate:
            try:
                db.session.delete(pirate)
                db.session.commit()
                return jsonify({'Message': 'Pirate deleted successfully'})
            except Exception as e:
                db.session.rollback()
                logger.error("ROLLBACK DONE")
                logger.exception(e)
                from datetime import datetime
                abort(404, description=[f'Exception error you can check log at {datetime.utcnow()}', f'exception: {e}'])
        else:
            abort(404, description="Pirate not found")

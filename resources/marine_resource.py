from app import logger
from config import db
from flask import jsonify, abort
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flasgger import swag_from
from models.marine import Marine
from models.crew import Crew
from models.sea import Sea
from models.devil_fruit import Devil_Fruit
from webargs import fields
from webargs.flaskparser import use_args
from models.enums import Statuses, Marine_positions

status = Statuses.Statuses()

marine_args = {
    'id_devil_fruit': fields.Int(required=True),
    'name': fields.Str(required=True),
    'rank': fields.Enum(Marine_positions, required=False),
    'image': fields.Str(required=False),
    'status': fields.Enum(Statuses, required=False)
}


class MarineListResource(Resource):
    @swag_from('../swagger/marine/get.yml')
    def get(self):
        marines = Marine.query.all()
        output = []
        for marine in marines:
            output.append({
                'id_marine': marine.id_marine,
                'devil_fruit': marine.devil_fruit.name,
                'name': marine.name,
                'rank': marine.rank,
                'image': marine.image,
                'status': marine.status
                })
        return jsonify({'Marines': output})

    @jwt_required()
    @use_args(marine_args)
    @swag_from('../swagger/marine/post.yml')
    def post(self, args):
        id_devil_fruit = args['id_devil_fruit']
        name = args['name']
        rank = args['rank']
        image = args['image']
        status = args['status']
        
        #Validations
        check_devil_fruit= Devil_Fruit.query.get(id_devil_fruit)
        if not check_devil_fruit:            
            abort(404, description=f'Devil Fruit with {id_devil_fruit} not exists')

        if status.value not in Statuses.Statuses():
            abort(404, description='status not in enumeration')

        if rank.value not in Marine_positions.Marine_positions():
            abort(404, description='Marine positions not in enumeration')

        #Insert
        exist_marine = Marine.query.filter_by(name=name).first()
        if not exist_marine:
            new_marine = Marine(id_devil_fruit= id_devil_fruit,
                                name=name,
                                rank=rank.value,
                                image=image,
                                status=status.value)
            db.session.add(new_marine)
            db.session.commit()
            return jsonify({'message': f'Marine {new_marine.name} created successfully'})
        else:
            abort(404, description=f'Marine {new_marine.name} already exists')

        

class MarineResource(Resource):
    def get(self, id_marine):
        marine = Marine.query.get(id_marine)
        if marine:
            marine = {
                'devil_fruit': marine.devil_fruit.name,
                'name': marine.name,
                'rank': marine.rank,
                'image': marine.image,
                'status': marine.status 
            }
            return jsonify({'Marine': marine})
        else:
            abort(404, description='Marine not exists')
        

    @jwt_required()
    @use_args(marine_args)
    def put(self, args, id_marine):
        id_devil_fruit = args['id_devil_fruit']
        name = args['name']
        rank = args['rank']
        image = args['image']
        status = args['status']

        marine = Marine.query.get(id_marine)
        if not marine:
            abort(404, description='Marine doesn''t found')
        
        devil_fruit = Devil_Fruit.query.get(id_devil_fruit)
        if not devil_fruit:
            abort(404, description='Devil Fruit doesn''t found')
            
        if status.value not in Statuses.Statuses():
            abort(404, description='Status not in enumeration')

        if rank.value not in Marine_positions.Marine_positions():
            abort(404, description='Marine positions not in enumeration')  

        if name and image:
            marine.id_devil_fruit = id_devil_fruit,
            marine.rank = rank.value
            marine.name = name,
            marine.image = image,
            marine.status = status.value
            db.session.commit()
            return jsonify({'message': 'Marine updated successfully'})
        else:
            abort(404, description='Args cannot be empty')


    @jwt_required()
    @swag_from('../swagger/marine/delete.yml')
    def delete(self, id_marine):
        marine = Marine.query.get(id_marine)
        if marine:
            try:
                db.session.delete(marine)
                db.session.commit()
                return jsonify({'Message': 'Marine deleted successfully'})
            except Exception as e:
                db.session.rollback()
                logger.error("ROLLBACK DONE")
                logger.exception(e)
                from datetime import datetime
                abort(404, description=[f'Exception error you can check log at {datetime.utcnow()}', f'exception: {e}'])
        else:
            abort(404, description="Marine not found")

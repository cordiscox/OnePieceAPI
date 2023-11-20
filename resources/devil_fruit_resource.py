from app import logger
from config import db
from flask import jsonify, abort
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from models.devil_fruit import Devil_Fruit
from models.type import Type
from webargs import fields
from webargs.flaskparser import use_args
from sqlalchemy.sql import text

fruit_args = {
    'id_type': fields.Int(required=True),
    'name': fields.Str(required=True),
    'description': fields.Str(required=True),
}

class DevilFruitListResource(Resource):
    def get(self):
        devil_fruits = Devil_Fruit.query.all()
        output = []
        for devil_fruit in devil_fruits:
            output.append({'id': devil_fruit.id_devil_fruit, 
                           'type': devil_fruit.type.type, 
                           'name': devil_fruit.name, 
                           'description': devil_fruit.description})
        return jsonify({'Devil_Fruits': output})
    
   # @jwt_required()
    @use_args(fruit_args)
    def post(self, args):
        id_type = args['id_type']
        name = args['name']
        description = args['description']

        check_type = Type.query.get(id_type)
        if not check_type:
            abort(404, description='Type not exists')

        exist_devil_fruit = Devil_Fruit.query.filter_by(name=name).first()
        if not exist_devil_fruit:
            new_devil_fruit = Devil_Fruit(id_type= id_type, 
                                          name=name, 
                                          description=description)
            db.session.add(new_devil_fruit)
            db.session.commit()
            return jsonify({'message': 'Devil_Fruit created successfully'})
        else:
            abort(404, description='Devil_Fruit already exists')

class DevilFruitResource(Resource):
    def get(self, id_devil_fruit):
        devil_fruit = Devil_Fruit.query.get(id_devil_fruit)
        if devil_fruit:
            devil_fruit = {
                'type': devil_fruit.type.type, 
                'name': devil_fruit.name,
                'description': devil_fruit.description
            }
            return jsonify({'Devil_Fruit': devil_fruit})
        else:
            abort(404, description='Devil Fruit not found')
    
    @jwt_required() 
    @use_args(fruit_args)   
    def put(self, args, id_devil_fruit):
        id_type = args['id_type']
        name = args['name']
        description = args['description']

        devil_fruit = Devil_Fruit.query.get(id_devil_fruit)
        if not devil_fruit:
            abort(404, description='Devil_Fruit not found')

        type = Type.query.get(id_type)
        if not type:
            abort(404, description='Type not found')
        
        if id_type and name and description:
            devil_fruit.id_type = id_type
            devil_fruit.name = name
            devil_fruit.description = description
            db.session.commit()
            return jsonify({'message': 'Updated successfully'})
        else:
            abort(404, description='Args cannot be empty')
        
    @jwt_required()    
    def delete(self, id_devil_fruit):
        devil_fruit = Devil_Fruit.query.get(id_devil_fruit)
        if devil_fruit:
            try:
                db.session.delete(devil_fruit)
                db.session.commit()
                return jsonify({'Message': 'Devil_Fruit deleted successfully'})
            except Exception as e:
                db.session.rollback()
                logger.error("ROLLBACK DONE")
                logger.exception(e)
                from datetime import datetime
                abort(404, description=[f'Exception error you can check log at {datetime.utcnow()}', f'exception: {e}'])
        else:
            abort(404, description="Devil_Fruit not found")
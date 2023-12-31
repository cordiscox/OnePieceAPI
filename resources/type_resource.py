from app import logger
from config import db
from flask import jsonify, abort, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flasgger import swag_from
from models import enums
from models.type import Type
from webargs import fields
from webargs.flaskparser import use_args, use_kwargs



type_args = {
    'type': fields.Str(required=True),
    'description': fields.Str(required=True),
}

#Add it.
#limit_args = {'limit': fields.Int()}
#@use_args(limit_args, location="query")

class TypeListResource(Resource):
    @swag_from('../swagger/type/get.yml')
    def get(self):
        types = Type.query.all()
        output = []
        for type in types:
            output.append({'id': type.id_type, 
                           'type': type.type, 
                           'description': type.description})
        return jsonify({'Types': output})
    
    @jwt_required()
    @use_args(type_args)
    @swag_from('../swagger/type/post.yml')
    def post(self, args):
        type = args['type']
        description = args['description']
        
        exist_type = Type.query.filter_by(type=type).first()
        if not exist_type:
            new_type = Type(type, description)
            db.session.add(new_type)
            db.session.commit()
            return jsonify({'message': 'Type created successfully'})
        else:
            abort(404, description='Type already exists')

class TypeResource(Resource):
    #@swag_from('../swagger/get_unique.yml')
    def get(self, id_type):
        type = Type.query.get(id_type)
        if type:
            type = {'id': type.id_type, 'type': type.type, 'description': type.description}
            return jsonify({'Type': type})
        else:
            abort(404, description='Type not found')
    

    @jwt_required() 
    @use_args(type_args)
    #@swag_from('../swagger/type/put.yml')
    def put(self, args, id_type):

        type = Type.query.get(id_type)
        if not type:
            abort(404, description='Type not found')

        if args['type'] in enums.fruit_types:
            type.type = args['type']
            type.description = args['description']
        else:
            abort(404, description='Type not in fruit types enumerator')
         
        db.session.commit()
        return jsonify({'message': 'Type updated'})
    
    @jwt_required()
    #@swag_from('../swagger/type/delete.yml') 
    def delete(self, id_type):
        type = Type.query.get(id_type)
        if type:
            try:
                db.session.delete(type)
                db.session.commit()
                return jsonify({'message': 'Type deleted successfully'})
            except Exception as e:
                db.session.rollback()
                logger.error("ROLLBACK DONE")
                logger.exception(e)
                from datetime import datetime
                abort(404, description=[f'Exception error you can check log at {datetime.utcnow()}', f'exception: {e}'])   
        else:
            abort(404, description='Type not found')
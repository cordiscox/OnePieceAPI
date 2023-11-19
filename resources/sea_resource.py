from app import logger
from config import db
from flask import jsonify, abort
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from models.sea import Sea
from webargs import fields
from webargs.flaskparser import use_args

sea_args = {
    'name': fields.Str(required=True)
}

class SeaListResource(Resource):
    def get(self):
        seas = Sea.query.all()
        output = []
        for sea in seas:
            output.append({'id': sea.id_sea, 'name': sea.name})
        return jsonify({'Seas': output})
    
    @jwt_required()
    @use_args(sea_args)
    def post(self, args):
        name = args['name']

        exist_sea = Sea.query.filter_by(name=name).first()
        if not exist_sea:
            new_sea = Sea(name=name)
            db.session.add(new_sea)
            db.session.commit()
            return jsonify({'message': 'Sea created successfully'})
        else:
            return jsonify({'error': 'Sea already exists'})

class SeaResource(Resource):
    def get(self, id_sea):
        sea = Sea.query.get(id_sea)
        if sea:
            sea = {'id': sea.id_sea, 'name': sea.name}
            return jsonify({'Sea': sea})
        else:
            return jsonify({'error': 'Sea not found'})
    
    @jwt_required()
    @use_args(sea_args)    
    def put(self, args, id_sea):
        name = args['name']
        sea = Sea.query.get(id_sea)

        if not sea:
            abort(404, description='Sea not found')
        
        if name:
            sea.name = name
            db.session.commit()
            return jsonify({'message': 'Updated successfully'})
        else:
            abort(404, description='Cannot be empty')
        
    @jwt_required()    
    def delete(self, id_sea):
        sea = Sea.query.get(id_sea)
        if sea:
            try:
                db.session.delete(sea)
                db.session.commit()
                return jsonify({'Message': 'Sea deleted successfully'})
            except Exception as e:
                db.session.rollback()
                logger.error("ROLLBACK DONE")
                logger.exception(e)
                from datetime import datetime
                abort(404, description=[f'Exception error you can check log at {datetime.utcnow()}', f'exception: {e}'])
        else:
            abort(404, description="Sea not found")
     
    
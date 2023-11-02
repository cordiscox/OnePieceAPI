from flask import jsonify, request
from flask_restful import Resource
from models.sea import Sea
from app import db
from sqlalchemy.exc import IntegrityError 
from flask_jwt_extended import jwt_required

class SeaListResource(Resource):
    def get(self):
        seas = Sea.query.all()
        output = []
        for sea in seas:
            output.append({'id': sea.id_sea, 'name': sea.name})
        return jsonify({'Seas': output})
    
    @jwt_required()
    def post(self):
        data = request.get_json()
        seas = Sea.query.all()
        if data['name'] not in [sea.name for sea in seas]:
            new_sea = Sea(name=data['name'])
            #print(new_sea.name)
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
            return jsonify({'Error': 'Sea not found'})
    
    @jwt_required()    
    def put(self, id_sea):
        data = request.get_json()
        sea = Sea.query.get(id_sea)
        if sea:
            sea.name = data.get('name', sea.name)
            db.session.commit()
            return jsonify({'message': 'Updated successfully'})
        else:
            return jsonify({'message': 'Sea not found.'})
        
    @jwt_required()    
    def delete(self, id_sea):
        sea = Sea.query.get(id_sea)
        if sea:
            try:
                db.session.delete(sea)
                db.session.commit()
            except IntegrityError as e:
                db.session.rollback()
                raise e
        return jsonify({'message': 'Sea deleted successfully'})
       
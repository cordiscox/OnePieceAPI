from flask import jsonify, request
from flask_restful import Resource
from models.type import Type
from app import db
from sqlalchemy.exc import IntegrityError 
from flask_jwt_extended import jwt_required

class TypeListResource(Resource):
    def get(self):
        types = Type.query.all()
        output = []
        for type in types:
            output.append({'id': type.id_type, 'type': type.type, 'description': type.description})
        return jsonify({'Types': output})
    
    @jwt_required()
    def post(self):
        data = request.get_json()
        types = Type.query.all()
        if data['type'] not in [t.type for t in types]:
            new_type = Type(type=data['type'], description=data['description'])
            print(new_type.type, new_type.description)
            db.session.add(new_type)
            db.session.commit()
            return jsonify({'message': 'Tipo creado exitosamente'})
        else:
            return jsonify({'error': 'El tipo ya existe'})

class TypeResource(Resource):
    def get(self, id_type):
        type = Type.query.get(id_type)
        if type:
            type = {'id': type.id_type, 'type': type.type, 'description': type.description}
            return jsonify({'Type': type})
        else:
            return jsonify({'Message': 'fail'})
    
    @jwt_required()    
    def put(self, id_type):
        data = request.get_json()
        type = Type.query.get(id_type)
        if type:
            type.type = data.get('type', type.type)
            type.description = data.get('description', type.description)
            db.session.commit()
            return jsonify({'message': 'Updated'})
        else:
            return jsonify({'message': 'Error.'})
    
    @jwt_required()    
    def delete(self, id_type):
        type = Type.query.get(id_type)
        if type:
            try:
                db.session.delete(type)
                db.session.commit()
            except IntegrityError as e:
                db.session.rollback()
                raise e
        return jsonify({'message': 'Type deleted successfully'})
        #else:
        #    return jsonify({'message': 'Type not found'})
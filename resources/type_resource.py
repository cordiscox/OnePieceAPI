from flask import jsonify, request, abort
from flask_restful import Resource, reqparse
from models.type import Type
from app import db
from sqlalchemy.exc import IntegrityError 
from flask_jwt_extended import jwt_required

parser = reqparse.RequestParser()
parser.add_argument('type', type=str, required=True, help='Type typo need to be str')
parser.add_argument('description', type=str, required=True, help='Description is required')

class TypeListResource(Resource):
    def get(self):
        types = Type.query.all()
        output = []
        for type in types:
            output.append({'id': type.id_type, 'type': type.type, 'description': type.description})
        return jsonify({'Types': output})
    
    #@jwt_required()
    def post(self):
        #data = request.get_json()
        data = parser.parse_args()
        print(f"XXXXXXXXXXX {data['type']} {data['description']} XXXXXXXXXXXXX")
        types = Type.query.all()
        if data['type'] not in [t.type for t in types]:
            new_type = Type(type=data['type'], description=data['description'])
            db.session.add(new_type)
            db.session.commit()
            return jsonify({'Message': 'Type created successfully'})
        else:
            abort(404, description='Type already exists')

class TypeResource(Resource):
    def get(self, id_type):
        type = Type.query.get(id_type)
        if type:
            type = {'id': type.id_type, 'type': type.type, 'description': type.description}
            return jsonify({'Type': type})
        else:
            abort(404, description='Type not found')
    
    @jwt_required()    
    def put(self, id_type):
        data = request.get_json()
        type = Type.query.get(id_type)
        if type:
            type.type = data.get('type', type.type)
            type.description = data.get('description', type.description)
            db.session.commit()
            return jsonify({'Message': 'Updated'})
        else:
            abort(404, description= 'Type not found')
    
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
            return jsonify({'Message': 'Type deleted successfully'})
        else:
            abort(404, description='Type not found')
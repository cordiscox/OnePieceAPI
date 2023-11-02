from flask import jsonify, request
from flask_restful import Resource
from models.crew import Crew
from app import db
from sqlalchemy.exc import IntegrityError 
from flask_jwt_extended import jwt_required

class CrewListResource(Resource):
    def get(self):
        crews = Crew.query.all()
        output = []
        for crew in crews:
            output.append({'id': crew.id_crew, 'name': crew.name})
        return jsonify({'Crews': output})
    
    @jwt_required()
    def post(self):
        data = request.get_json()
        crews = Crew.query.all()
        if data['name'] not in [crew.name for crew in crews]:
            new_crew = Crew(name=data['name'])
            #print(new_crew.name)
            db.session.add(new_crew)
            db.session.commit()
            return jsonify({'message': 'Crew created successfully'})
        else:
            return jsonify({'error': 'Crew already exists'})

class CrewResource(Resource):
    def get(self, id_crew):
        crew = Crew.query.get(id_crew)
        if crew:
            crew = {'id': crew.id_crew, 'name': crew.name}
            return jsonify({'Crew': crew})
        else:
            return jsonify({'Error': 'Crew not found'})
    
    @jwt_required()    
    def put(self, id_crew):
        data = request.get_json()
        crew = Crew.query.get(id_crew)
        if crew:
            crew.name = data.get('crew', crew.name)
            db.session.commit()
            return jsonify({'message': 'Updated successfully'})
        else:
            return jsonify({'message': 'Crew not found.'})
        
    @jwt_required()    
    def delete(self, id_crew):
        crew = Crew.query.get(id_crew)
        if crew:
            try:
                db.session.delete(crew)
                db.session.commit()
            except IntegrityError as e:
                db.session.rollback()
                raise e
        return jsonify({'message': 'Crew deleted successfully'})
       
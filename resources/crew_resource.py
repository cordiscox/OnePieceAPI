from app import logger
from config import db
from flask import jsonify, abort
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from models.crew import Crew
from webargs import fields
from webargs.flaskparser import use_args


crew_args = {
    'name': fields.Str(required=True)
}

class CrewListResource(Resource):
    def get(self):
        crews = Crew.query.all()
        output = []
        for crew in crews:
            output.append({'id': crew.id_crew, 'name': crew.name})
        return jsonify({'Crews': output})
    
    @jwt_required()
    @use_args(crew_args)
    def post(self, args):
        name = args['name']

        exist_crews = Crew.query.filter_by(name=name).first()
        if not exist_crews:
            new_crew = Crew(name=name)
            db.session.add(new_crew)
            db.session.commit()
            return jsonify({'message': 'Crew created successfully'})
        else:
            abort(404, description='Crew already exists')

class CrewResource(Resource):
    def get(self, id_crew):
        crew = Crew.query.get(id_crew)
        if crew:
            crew = {'id': crew.id_crew, 'name': crew.name}
            return jsonify({'Crew': crew})
        else:
            abort(404, description='Crew not found')
    
    @jwt_required() 
    @use_args(crew_args)   
    def put(self, args, id_crew):
        name = args['name']
        crew = Crew.query.get(id_crew)

        if not crew:
            abort(404, description='Crew not found')
        
        if name:
            crew.name = name
            db.session.commit()
            return jsonify({'message': 'Updated successfully'})
        else:
            abort(404, description='Cannot be empty')
        
    @jwt_required()    
    def delete(self, id_crew):
        crew = Crew.query.get(id_crew)
        if crew:
            try:
                db.session.delete(crew)
                db.session.commit()
                return jsonify({'Message': 'Crew deleted successfully'})
            except Exception as e:
                db.session.rollback()
                logger.error("ROLLBACK DONE")
                logger.exception(e)
                from datetime import datetime
                abort(404, description=[f'Exception error you can check log at {datetime.utcnow()}', f'exception: {e}'])
        else:
            abort(404, description="Crew not found")
    
       
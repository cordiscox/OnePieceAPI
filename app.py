import os
from config import db, Config, Preprodconfig
from dotenv import load_dotenv, set_key
from flask import Flask, jsonify
from flask_restful import Api
from flask_migrate import Migrate
from flasgger import Swagger
from flasgger.utils import load_from_file
from logger import logger


from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import JWTManager


from resources.type_resource import TypeListResource, TypeResource
from resources.user_resource import LoginResource, RegisterResource
from resources.sea_resource import SeaListResource, SeaResource
from resources.crew_resource import CrewListResource, CrewResource
from resources.devil_fruit_resource import DevilFruitListResource, DevilFruitResource
from resources.pirate_resource import PirateListResource, PirateResource
from resources.marine_resource import MarineListResource, MarineResource

def create_app():
    logger.debug("Initilization of APP")

    app = Flask(__name__)
    load_dotenv()
    #app.config.from_object(Config)
    app.config.from_object(Preprodconfig)
    db.init_app(app)
    api = Api(app)
    jwt = JWTManager(app)
    migrate = Migrate(app, db)
    swagger = Swagger(app)

    logger.debug(app.config)

    api.add_resource(LoginResource, '/login')
    api.add_resource(RegisterResource, '/register')

    api.add_resource(TypeListResource, '/types')
    api.add_resource(TypeResource, '/types/<int:id_type>')

    api.add_resource(SeaListResource, '/seas')
    api.add_resource(SeaResource, '/seas/<int:id_sea>')

    api.add_resource(CrewListResource, '/crews')
    api.add_resource(CrewResource, '/crews/<int:id_crew>')

    api.add_resource(DevilFruitListResource, '/devil_fruits')
    api.add_resource(DevilFruitResource, '/devil_fruits/<int:id_devil_fruit>')

    api.add_resource(PirateListResource, '/pirates')
    api.add_resource(PirateResource, '/pirates/<int:id_pirate>')

    api.add_resource(MarineListResource, '/marines')
    api.add_resource(MarineResource, '/marines/<int:id_marine>')

    
    @app.errorhandler(422)
    @app.errorhandler(400)
    def handle_error(err):
        headers = err.data.get("headers", None)
        messages = err.data.get("messages", ["Invalid request."])
        if headers:
            return jsonify({"errors": messages}), err.code, headers
        else:
            return jsonify({"errors": messages}), err.code

    #Logica para crear las tablas y los datos --> chequear de cambiarlo a una capa de datos.
    #Logic to create all tables and set the data.
    if os.environ['FIRST_EXECUTION']:
        logger.info("First execution of the application, change config to False")
        os.environ['FIRST_EXECUTION'] = ''
        set_key('.env', 'FIRST_EXECUTION', '')
        with app.app_context():
            from models import crew, sea, type, user, devil_fruit, enums, marine, pirate
            try:
                logger.info("Creating all tables")
                db.create_all()
                logger.info("Creating all data on the tables")
                #import test
                #test.create_sample_data()
            except Exception as e:
                logger.exception(e)
        
    return app


#if __name__ == '__main__':
#    app = create_app()
#    app.run(debug=True)
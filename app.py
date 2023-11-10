from config import db, Config, Preprodconfig
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_restful import Api
from flask_migrate import Migrate
from logger import logger

from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import JWTManager

from resources.type_resource import TypeListResource, TypeResource
from resources.user_resource import LoginResource, RegisterResource
from resources.sea_resource import SeaListResource, SeaResource

def create_app():
    logger.debug("Initilization of APP")

    app = Flask(__name__)
    load_dotenv()
    app.config.from_object(Preprodconfig)
    db.init_app(app)
    api = Api(app)
    jwt = JWTManager(app)
    migrate = Migrate(app, db)

    api.add_resource(TypeListResource, '/types')
    api.add_resource(TypeResource, '/types/<int:id_type>')

    api.add_resource(SeaListResource, '/seas')
    api.add_resource(SeaResource, '/seas/<int:id_sea>')

    api.add_resource(LoginResource, '/login')
    api.add_resource(RegisterResource, '/register')
    
    @app.errorhandler(422)
    @app.errorhandler(400)
    def handle_error(err):
        headers = err.data.get("headers", None)
        messages = err.data.get("messages", ["Invalid request."])
        if headers:
            return jsonify({"errors": messages}), err.code, headers
        else:
            return jsonify({"errors": messages}), err.code
    try:
        
        with app.app_context():
            from models import crew, sea, type, user, devil_fruit, enums,marine, pirate
            db.create_all()
    except Exception as e:
        logger.exception(e)
        
    return app


#if __name__ == '__main__':
#    app = create_app()
#    app.run(debug=True)
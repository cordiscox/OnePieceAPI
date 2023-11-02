from config import db, Config
from dotenv import load_dotenv
from flask import Flask
from flask_restful import Api

from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import JWTManager

from resources.type_resource import TypeListResource, TypeResource
from resources.user_resource import LoginResource
from resources.sea_resource import SeaListResource, SeaResource

def create_app():
    app = Flask(__name__)
    load_dotenv()
    app.config.from_object(Config)
    db.init_app(app)
    api = Api(app)
    jwt = JWTManager(app)

    api.add_resource(TypeListResource, '/types')
    api.add_resource(TypeResource, '/types/<int:id_type>')

    api.add_resource(SeaListResource, '/seas')
    api.add_resource(SeaResource, '/seas/<int:id_sea>')

    api.add_resource(LoginResource, '/login')


    with app.app_context():
        db.create_all()
    
    return app

#if __name__ == '__main__':
#    app = create_app()
#    app.run(debug=True)
from config import db, Config
from dotenv import load_dotenv
from flask import Flask
from flask_restful import Api
from resources.type_resource import TypeListResource, TypeResource


def create_app():
    app = Flask(__name__)
    load_dotenv()
    app.config.from_object(Config)
    db.init_app(app)
    api = Api(app)

    api.add_resource(TypeListResource, '/types')
    api.add_resource(TypeResource, '/types/<int:id_type>')
    
    
    return app

#if __name__ == '__main__':
#    app = create_app()
#    app.run(debug=True)
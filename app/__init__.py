from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import config

db = SQLAlchemy()
ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    app.config.from_object(config.Config)

    db.init_app(app)
    ma.init_app(app)

    
    from app.infra.entities.user_entity import user_entity
    from app.infra.entities.user_ssh_entity import user_ssh_entity
    

    from .routes import init_routes
    jwt = JWTManager(app)
    init_routes(app)

    return app

import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from application.config import app_config

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    api = Api(app)

    from application.models.item import Item
    from application.controllers.welcome import WelcomeResources
    from application.controllers.items import ItemResources

    api.add_resource(WelcomeResources, '/')
    api.add_resource(ItemResources, '/items', '/items/<int:item_id>')

    return app

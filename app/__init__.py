import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

api = Api(app)

from app.models.item import Item
from app.controllers.items import ItemResources
from app.controllers.welcome import WelcomeRoutes

api.add_resource(ItemResources, '/items', '/items/<int:item_id>')

if __name__ == '__main__':
    app.run()

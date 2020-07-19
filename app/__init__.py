import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


from app.models.item import Item
from app.controllers.items import ItemRoutes
from app.controllers.welcome import WelcomeRoutes


if __name__ == '__main__':
    app.run()

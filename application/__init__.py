from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from application.config import app_config
from application.popos.invalid_usage import InvalidUsage
from flask import jsonify

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    api = Api(app)

    from application.models.item import Item
    from application.models.bid import Bid

    from application.controllers.welcome import WelcomeResources
    from application.controllers.items import ItemResources
    from application.controllers.bids import BidResources
    from application.controllers.charities import CharityResources


    api.add_resource(WelcomeResources, '/')
    api.add_resource(ItemResources, '/items', '/items/<int:item_id>')
    api.add_resource(BidResources, '/bids', '/bids/<int:bid_id>')
    api.add_resource(CharityResources, '/charities', '/charities/<string:search_term>')

    @app.errorhandler(InvalidUsage)
    def handle_invalid_usage(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response
    
    return app

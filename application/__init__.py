from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_cors import CORS
from application.config import app_config
from flask_swagger_ui import get_swaggerui_blueprint
import application.static

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    CORS(app)

    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.yml'
    SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "auctionable_change_api"
        }
    )
    app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    api = Api(app)
    CORS(api)

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


    return app

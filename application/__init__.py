from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_cors import CORS
from application.config import app_config
from flask_swagger_ui import get_swaggerui_blueprint

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
            'app_name': "auctionable_change_api",
            'defaultModelsExpandDepth': -1
        }
    )
    app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    api = Api(app)

    from application.models.item import Item
    from application.models.bid import Bid
    from application.models.bid_detail import BidDetail
    from application.models.user import User

    from application.controllers.welcome_controller import WelcomeResources
    from application.controllers.items_controller import ItemResources
    from application.controllers.bids_controller import BidResources
    from application.controllers.bid_details_controller import BidDetailResources
    from application.controllers.charities_controller import CharityResources
    from application.controllers.users_controller import UserResources
    from application.controllers.items.available_controller import AvailableItemResources
    from application.controllers.items.pending_controller import PendingItemResources
    from application.controllers.items.sold_controller import SoldItemResources
    from application.controllers.items.winners_controller import WinnerResources
    from application.controllers.bids.winners_controller import WinnerBidResources
    from application.controllers.auth_controller import LoginResources
    from application.controllers.auth_controller import LogoutResources

    api.add_resource(WelcomeResources, '/')
    api.add_resource(AvailableItemResources, '/items/available')
    api.add_resource(PendingItemResources, '/items/pending')
    api.add_resource(SoldItemResources, '/items/sold')
    api.add_resource(WinnerResources, '/items/winners')
    api.add_resource(ItemResources, '/items', '/items/<int:item_id>')
    api.add_resource(WinnerBidResources, '/bids/winners')
    api.add_resource(BidResources, '/bids', '/bids/<int:bid_id>')
    api.add_resource(CharityResources, '/charities', '/charities/<string:search_term>')
    api.add_resource(BidDetailResources, '/bid_details', '/bid_details/<int:bid_detail_id>')
    api.add_resource(UserResources, '/users', '/users/<int:user_id>')
    api.add_resource(LoginResources, '/login')
    api.add_resource(LogoutResources, '/logout')

    return app

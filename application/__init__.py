# import os
# from flask import Flask, request, jsonify
# from flask_sqlalchemy import SQLAlchemy
# from flask_restful import Api
#
# application = Flask(__name__)
#
# application.config.from_object(os.environ['APP_SETTINGS'])
# application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(application)
#
# api = Api(application)
#
# from application.models.item import Item
# from application.controllers.items import ItemResources
# from application.controllers.welcome import WelcomeRoutes
#
# api.add_resource(ItemResources, '/items', '/items/<int:item_id>')
#
# if __name__ == '__main__':
#     application.run()
import os
from flask import Flask, jsonify
from flask_restful import Api
from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import default_exceptions
from flask_sqlalchemy import SQLAlchemy
from config import app_config

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)

    @app.errorhandler(Exception)
    def handle_error(e):
        code = 500
        if isinstance(e, HTTPException):
            code = e.code
        return jsonify(error=str(e)), code

    for ex in default_exceptions:
        app.register_error_handler(ex, handle_error)

    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    api = Api(app)

    from application.models.item import Item
    from application.controllers.items import ItemResources
    from application.controllers.welcome import WelcomeRoutes

    api.add_resource(ItemResources, '/items', '/items/<int:item_id>')

    return app

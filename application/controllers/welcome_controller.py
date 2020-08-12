from flask_restful import Resource
from flask_restful import fields, marshal

welcome_fields = {
    'welcome': fields.String
}


class WelcomeResources(Resource):
    def get(self):
        return marshal('Hello, World', welcome_fields)

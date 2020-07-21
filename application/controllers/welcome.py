from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, reqparse, request
from flask_restful import fields, marshal_with, marshal

welcome_fields = {
    'welcome': fields.String
}

class WelcomeResources(Resource):
    def get(self):
        return marshal('Hello, World', welcome_fields)

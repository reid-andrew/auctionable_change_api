from app import app, db
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from app.models.item import Item

class ItemRoutes:
    @app.route("/items")
    def get_items():
        try:
            items=Item.query.all()
            return jsonify([e.serialize() for e in items])
        except Exception as e:
            return(str(e))

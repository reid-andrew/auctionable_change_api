import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Item

@app.route("/")
def hello():
    return "Hello World!"


@app.route("/items")
def get_items():
    try:
        items=Item.query.all()
        return jsonify([e.serialize() for e in items])
    except Exception as e:
        return(str(e))

if __name__ == '__main__':
    app.run()

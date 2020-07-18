from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/items")
def get_items():
    return "items : {}".format(item)

if __name__ == '__main__':
    app.run()

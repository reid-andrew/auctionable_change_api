from app import app


class WelcomeRoutes:
    @app.route("/")
    def hello():
        return "Hello World!"

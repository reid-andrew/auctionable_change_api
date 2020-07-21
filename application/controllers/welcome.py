from application import create_app


class WelcomeRoutes:
    @create_app.route("/")
    def hello(self):
        return "Hello World!"

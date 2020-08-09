from flask_restful import Resource, reqparse
from flask_restful import fields, marshal
from application.models.user import User
from flask_login import current_user, login_user

auth_fields = {
    'id': fields.Integer,
    'email': fields.String,
    'password': fields.String
}

auth_list_fields = {
    'count': fields.Integer,
    'auth': fields.List(fields.Nested(auth_fields))
}

user_post_parser = reqparse.RequestParser()
user_post_parser.add_argument(
    'id',
    type=str,
    required=False,
    location=['json']
)
user_post_parser.add_argument(
    'email',
    type=str,
    required=False,
    location=['json']
)
user_post_parser.add_argument(
    'password',
    type=str,
    required=False,
    location=['json']
)


class AuthResources(Resource):
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('Invalid username or password')
                return redirect(url_for('login'))
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('index'))
        return render_template('login.html', title='Sign In', form=form)
    # def get(self, search_term=None):
    #     search_term = "" if search_term is None else search_term
    #     chars = return_charities(search_term)
    #
    #     return marshal({
    #         'count': len(chars),
    #         'charities': [marshal(c, charity_fields) for c in chars]
    #     }, charity_list_fields)

import unittest
import json
from application import create_app, db
from application.models.user import User
import time

class TestUsers(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.test_app = self.app.test_client()
        with self.app.app_context():
            db.create_all()

        user = User(
            first_name="Johnny",
            last_name="McSellingstuff",
            email="jm@example.com",
            password="12345"
        )
        with self.app.app_context():
            user.hash_password(user.password)
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_registered_user_login(self):
        response = self.test_app.post(
            '/login',
            json={
                'email': 'jm@example.com',
                'password': '12345'
            },
            follow_redirects=True
        )
        payload = json.loads(response.data)
        self.assertEquals(payload['message'], 'Successfully logged in.')
        self.assertTrue(payload['user_token'])
        self.assertEquals(response.status_code, 200)

    def test_non_registered_user_login(self):
        response = self.test_app.post(
            '/login',
            json={
                'email': 'johnsmith@example.com',
                'password': '12345'
            },
            follow_redirects=True
        )
        payload = json.loads(response.data)
        self.assertEquals(payload['message'], 'Username or password incorrect')
        self.assertEquals(response.status_code, 400)

    if __name__ == "__main__":
            unittest.main()

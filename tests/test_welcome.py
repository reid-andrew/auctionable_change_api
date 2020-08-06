import unittest
import json
from application import create_app, db


class TestWelcome(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.test_app = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_gets_welcome_screen(self):
        response = self.test_app.get(
            '/',
            follow_redirects=True
        )

        self.assertEquals(response.status, "200 OK")
        payload = json.loads(response.data)
        self.assertEquals(payload, {'welcome': None})


if __name__ == "__main__":
    unittest.main()

import unittest
import json
from application import create_app, db


class TestCharities(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.test_app = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_gets_all_charities(self):
        response = self.test_app.get(
            '/charities',
            follow_redirects=True
        )

        self.assertEquals(response.status, "200 OK")
        payload = json.loads(response.data)
        self.assertEquals(payload['count'], 100)
        self.assertEquals(payload['charities'][0]['id'], 10694045)
        self.assertEquals(payload['charities'][0]['name'], 'Florida Breast Cancer Foundation')

    def test_gets_charities_with_search_term(self):
        response = self.test_app.get(
            '/charities/ohio',
            follow_redirects=True
        )

        self.assertEquals(response.status, "200 OK")
        payload = json.loads(response.data)
        self.assertEquals(payload['count'], 75)
        self.assertEquals(payload['charities'][0]['id'], 261594574)
        self.assertEquals(payload['charities'][1]['name'], 'Restavek Freedom')


if __name__ == "__main__":
    unittest.main()

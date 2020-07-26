import unittest
import json
from application import create_app, db
from application.models.final import Final


class TestUsers(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.test_app = self.app.test_client()
        with self.app.app_context():
            db.create_all()

        final = Final(
            street_address="123 This Is My Street Way",
            city="My City",
            state="Colorado",
            zip_code="12345",
            receipt="img.ul"
          )
        with self.app.app_context():
            db.session.add(final)
            db.session.commit()

        final = Final(
          street_address="123 Sesame Street",
          city="New York",
          state='New York',
          zip_code='10005',
          receipt='img.ul'
          )
        with self.app.app_context():
            db.session.add(final)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_all_items(self):
        response = self.test_app.get(
            '/finals',
            follow_redirects=True
        )

        self.assertEquals(response.status, "200 OK")
        payload = json.loads(response.data)
        self.assertEquals(payload['count'], 2)
        self.assertEquals(payload['finals'][0]['city'], 'My City')
        self.assertEquals(payload['finals'][0]['zip_code'], '12345')
        self.assertEquals(payload['finals'][-1]['street_address'], '123 Sesame Street')
        self.assertEquals(payload['finals'][-1]['state'], 'New York')

    def test_create_items(self):
        response = self.test_app.post(
            '/finals',
            json={
                'street_address': '5600 Hogwarts Way',
                'city': 'Magic',
                'state': 'Spells',
                'zip_code': '09876',
                'receipt': 'img.ul'
            },
            follow_redirects=True
        )

        self.assertEquals(response.status, "200 OK")
        payload = json.loads(response.data)
        self.assertEquals(payload['city'], 'Magic')
        self.assertEquals(payload['zip_code'], '09876')


if __name__ == "__main__":
    unittest.main()

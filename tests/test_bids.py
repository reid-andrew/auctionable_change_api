import unittest
import json
from application import create_app, db
from application.models.bid import Bid
from application.models.item import Item


class TestUsers(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.test_app = self.app.test_client()
        with self.app.app_context():
            db.create_all()

        item = Item(
            description="Antique Tea set",
            donor="Demo McDemoFace",
            donor_email="demomcdemoface@example.com",
            price=140.00,
            status="For Sale",
            title="Tea Set",
            category="furniture",
            charity="Big Cat Rescue",
            charity_url="http://www.thisisatotallyligiturl.com",
            charity_score=4,
            image="img.ul"
        )
        with self.app.app_context():
            db.session.add(item)
            db.session.commit()

        bid = Bid(
            bidder_name="Testy McTesterson",
            bidder_email="testymctesterson@example.com",
            amount=300.00,
            street_address="123 This Is My Street Way",
            city="My City",
            state="Colorado",
            zip_code="12345",
            receipt="img.ul",
            item_id=1
          )
        with self.app.app_context():
            db.session.add(bid)
            db.session.commit()

        bid = Bid(
          bidder_name="Elmo",
          bidder_email="elmo@example.com",
          amount=400.00,
          street_address="123 Sesame Street ",
          city="New York",
          state='New York',
          zip_code='10005',
          receipt='img.ul',
          item_id=1
          )
        with self.app.app_context():
            db.session.add(bid)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_all_bids(self):
        response = self.test_app.get(
            '/bids',
            follow_redirects=True
        )

        self.assertEquals(response.status, "200 OK")
        payload = json.loads(response.data)
        self.assertEquals(payload['count'], 2)
        self.assertEquals(payload['bids'][0]['city'], 'My City')
        self.assertEquals(payload['bids'][0]['zip_code'], '12345')
        self.assertEquals(payload['bids'][-1]['bidder_email'], 'elmo@example.com')
        self.assertEquals(payload['bids'][-1]['amount'], 400.00)

    def test_get_one_bid(self):
        response = self.test_app.get(
            '/bids/2',
            follow_redirects=True
        )

        self.assertEquals(response.status, "200 OK")
        payload = json.loads(response.data)
        self.assertEquals(payload['id'], 2)
        self.assertEquals(payload['bidder_email'], 'elmo@example.com')
        self.assertEquals(payload['amount'], 400.00)
        self.assertEquals(payload['city'], 'New York')

    def test_sad_path_for_nonexistent_bid(self):
        response = self.test_app.get(
            '/bids/10',
            follow_redirects=True
        )

        self.assertEquals(response.status, "404 NOT FOUND")

    def test_create_bids(self):
        response = self.test_app.post(
            '/bids',
            json={
                'bidder_name': 'Hermione',
                'bidder_email': 'granger@example.com',
                'amount': 500.00,
                'street_address': '5600 Hogwarts Way',
                'city': 'Magic',
                'state': 'Spells',
                'zip_code': '09876',
                'receipt': 'img.ul',
                'item_id': 1
            },
            follow_redirects=True
        )

        self.assertEquals(response.status, "200 OK")
        payload = json.loads(response.data)
        self.assertEquals(payload['city'], 'Magic')
        self.assertEquals(payload['zip_code'], '09876')

    def test_sad_path_for_create_bid_with_missing_info(self):
        response = self.test_app.post(
            '/bids',
            json={
                'amount': 500.00,
                'street_address': '5600 Hogwarts Way',
                'city': 'Magic',
                'state': 'Spells',
                'zip_code': '09876',
                'receipt': 'img.ul',
                'item_id': 1
            },
            follow_redirects=True
        )

        self.assertEquals(response.status, "400 BAD REQUEST")

if __name__ == "__main__":
    unittest.main()

import unittest
import json
from application import create_app, db
from application.models.bid_detail import BidDetail
from application.models.bid import Bid
from application.models.item import Item
from application.models.user import User


class TestBidDetails(unittest.TestCase):
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
            db.session.add(user)
            db.session.commit()

        user = User(
            first_name="Jose",
            last_name="De Los Buyingstuff",
            email="jd@example.com",
            password="12345"
        )
        with self.app.app_context():
            db.session.add(user)
            db.session.commit()

        user = User(
            first_name="Jacques",
            last_name="Du Purchaser",
            email="jdp@example.com",
            password="12345"
        )
        with self.app.app_context():
            db.session.add(user)
            db.session.commit()

        item = Item(
            user_id=1,
            title="Tea Set",
            description="Antique Tea set",
            price=140.00,
            category="furniture",
            charity="Big Cat Rescue",
            charity_url="http://www.thisisatotallyligiturl.com",
            charity_score=4,
            charity_score_image="https://d20umu42aunjpx.cloudfront.net/_gfx_/icons/stars/4stars.png",
            image="img.ul",
            auction_length=5
          )
        with self.app.app_context():
            db.session.add(item)
            db.session.commit()

        item = Item(
          user_id=1,
          title="Rocking Chair",
          description="Vintage wood rocking chair",
          price=40.00,
          category='furniture',
          charity='Big Cat Rescue',
          charity_url="http://www.thisisatotallyligiturl.com",
          charity_score=4,
          charity_score_image="https://d20umu42aunjpx.cloudfront.net/_gfx_/icons/stars/4stars.png",
          image='img.ul',
          auction_length=5
          )
        with self.app.app_context():
            db.session.add(item)
            db.session.commit()

        bid = Bid(
            item_id=1,
            user_id=2,
            amount=300.00
          )
        with self.app.app_context():
            db.session.add(bid)
            db.session.commit()

        bid = Bid(
          item_id=1,
          user_id=3,
          amount=400.00,
          )
        with self.app.app_context():
            db.session.add(bid)
            db.session.commit()

        bid_detail = BidDetail(
          bid_id=1,
          street_address="123 Main St.",
          city="Coshocton",
          state="Ohio",
          zip_code="43812",
          receipt="image.com"
          )
        with self.app.app_context():
            db.session.add(bid_detail)
            db.session.commit()

        bid_detail = BidDetail(
          bid_id=2,
          street_address="417 Peach Ave.",
          city="Lakeside",
          state="Ohio",
          zip_code="43440",
          receipt="image.com"
          )
        with self.app.app_context():
            db.session.add(bid_detail)
            db.session.commit()
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_all_bid_details(self):
        response = self.test_app.get(
            '/bid_details',
            follow_redirects=True
        )

        self.assertEquals(response.status, "200 OK")
        payload = json.loads(response.data)
        self.assertEquals(payload['count'], 2)
        self.assertEquals(payload['bid_details'][0]['street_address'], "123 Main St.")
        self.assertEquals(payload['bid_details'][0]['zip_code'], "43812")
        self.assertEquals(payload['bid_details'][-1]['street_address'], "417 Peach Ave.")
        self.assertEquals(payload['bid_details'][-1]['zip_code'], "43440")

    def test_get_one_bid_details(self):
        response = self.test_app.get(
            '/bid_details/1',
            follow_redirects=True
        )

        self.assertEquals(response.status, "200 OK")
        payload = json.loads(response.data)
        self.assertEquals(payload['id'], 1)
        self.assertEquals(payload['street_address'], "123 Main St.")
        self.assertEquals(payload['zip_code'], "43812")
    #
    def test_sad_path_for_nonexistent_bid(self):
        response = self.test_app.get(
            '/bid_details/10',
            follow_redirects=True
        )

        self.assertEquals(response.status, "404 NOT FOUND")

    def test_create_bids(self):
        response = self.test_app.post(
            '/bid_details',
            json={
              'bid_id': 2,
              'street_address': "999 Test St.",
              'city': "West Lafayette",
              'state': "Ohio",
              'zip_code': "43845",
              'receipt': "image.com"
            },
            follow_redirects=True
        )

        self.assertEquals(response.status, "200 OK")
        payload = json.loads(response.data)
        self.assertEquals(payload['bid_id'], 2)
        self.assertEquals(payload['city'], "West Lafayette")
        self.assertEquals(payload['receipt'], "image.com")

    def test_sad_path_for_create_bid_with_missing_info(self):
        response = self.test_app.post(
            '/bid_details',
            json={
              'bid_id': 2,
              'street_address': "999 Test St.",
              'zip_code': "43845",
              'receipt': "image.com"
            },
            follow_redirects=True
        )

        self.assertEquals(response.status, "400 BAD REQUEST")

    def test_sad_path_for_create_bid_with_nonexistent_item(self):
        response = self.test_app.post(
            '/bid_details',
            json={
              'bid_id': 9999,
              'street_address': "999 Test St.",
              'city': "West Lafayette",
              'state': "Ohio",
              'zip_code': "43845",
              'receipt': "image.com"
            },
            follow_redirects=True
        )

        self.assertEquals(response.status, "404 NOT FOUND")

    def test_update_bids_only_updates_selected_fields(self):
        response = self.test_app.put(
            '/bid_details/1',
            json={
              'street_address': "999 Test St.",
              'receipt': "new_image.com"
            },
            follow_redirects=True
        )

        self.assertEquals(response.status, "200 OK")
        payload = json.loads(response.data)
        self.assertEquals(payload['street_address'], "999 Test St.")
        self.assertEquals(payload['receipt'], "new_image.com")
        self.assertEquals(payload['city'], "Coshocton")
        self.assertEquals(payload['state'], "Ohio")

    def test_update_can_update_all_fields(self):
        response = self.test_app.put(
            '/bid_details/2',
            json={
              'street_address': "999 Test St.",
              'city': "New City",
              'state': "New State",
              'zip_code': "99999",
              'receipt': "new_image.com"
            },
            follow_redirects=True
        )

        self.assertEquals(response.status, "200 OK")
        payload = json.loads(response.data)
        self.assertEquals(payload['street_address'], "999 Test St.")
        self.assertEquals(payload['city'], "New City")
        self.assertEquals(payload['state'], "New State")
        self.assertEquals(payload['zip_code'], "99999")
        self.assertEquals(payload['receipt'], "new_image.com")

    def test_sad_path_for_update_bid(self):
        response = self.test_app.put(
            '/bid_details/9090909',
            json={
              'street_address': "999 Test St.",
              'city': "New City",
              'state': "New State",
              'zip_code': "99999",
              'receipt': "new_image.com"
            },
            follow_redirects=True
        )

        self.assertEquals(response.status, "404 NOT FOUND")

    def test_delete_bid(self):
        response = self.test_app.get(
            '/bid_details',
            follow_redirects=True
        )

        self.assertEquals(response.status, "200 OK")
        payload = json.loads(response.data)
        self.assertEquals(payload['count'], 2)

        response = self.test_app.delete(
            '/bid_details/2',
            follow_redirects=True
        )

        self.assertEquals(response.status, "200 OK")
        payload = json.loads(response.data)
        self.assertEquals(payload['id'], 2)

        response = self.test_app.get(
            '/bid_details',
            follow_redirects=True
        )

        self.assertEquals(response.status, "200 OK")
        payload = json.loads(response.data)
        self.assertEquals(payload['count'], 1)

    def test_sad_path_for_delete_item(self):
        response = self.test_app.delete(
            '/bid_details/11111',
            follow_redirects=True
        )

        self.assertEquals(response.status, "404 NOT FOUND")

if __name__ == "__main__":
    unittest.main()

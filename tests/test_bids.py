import unittest
import json
from application import create_app, db
from application.models.bid import Bid
from application.models.item import Item
from application.models.user import User


class TestBids(unittest.TestCase):
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
        self.assertEquals(payload['bids'][0]['user_id'], 2)
        self.assertEquals(payload['bids'][0]['amount'], 300.00)
        self.assertEquals(payload['bids'][0]['winner'], False)
        self.assertEquals(payload['bids'][-1]['user_id'], 3)
        self.assertEquals(payload['bids'][-1]['amount'], 400.00)

    def test_get_one_bid(self):
        response = self.test_app.get(
            '/bids/2',
            follow_redirects=True
        )

        self.assertEquals(response.status, "200 OK")
        payload = json.loads(response.data)
        self.assertEquals(payload['id'], 2)
        self.assertEquals(payload['user_id'], 3)
        self.assertEquals(payload['amount'], 400.00)
        self.assertEquals(payload['winner'], False)

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
                'item_id': 1,
                'user_id': 2,
                'amount': 500.00
            },
            follow_redirects=True
        )

        self.assertEquals(response.status, "200 OK")
        payload = json.loads(response.data)
        self.assertEquals(payload['user_id'], 2)
        self.assertEquals(payload['amount'], 500.00)
        self.assertEquals(payload['winner'], False)

    def test_sad_path_for_create_bid_with_missing_info(self):
        response = self.test_app.post(
            '/bids',
            json={
                'item_id': 1,
                'amount': 500.00
            },
            follow_redirects=True
        )

        self.assertEquals(response.status, "400 BAD REQUEST")

    def test_sad_path_for_create_bid_with_nonexistent_item(self):
        response = self.test_app.post(
            '/bids',
            json={
                'item_id': 1111,
                'user_id': 2,
                'amount': 500.00
            },
            follow_redirects=True
        )

        self.assertEquals(response.status, "404 NOT FOUND")

    def test_update_bids_only_updates_selected_fields(self):
        response = self.test_app.put(
            '/bids/1',
            json={
                'user_id': 3,
                'amount': 999.15
            },
            follow_redirects=True
        )

        self.assertEquals(response.status, "200 OK")
        payload = json.loads(response.data)
        self.assertEquals(payload['user_id'], 3)
        self.assertEquals(payload['amount'], 999.15)
        self.assertEquals(payload['item_id'], 1)
        self.assertEquals(payload['winner'], False)

    def test_update_can_update_all_fields(self):
        response = self.test_app.put(
            '/bids/1',
            json={
                'item_id': 2,
                'user_id': 3,
                'amount': 500.00,
                'winner': True
            },
            follow_redirects=True
        )

        self.assertEquals(response.status, "200 OK")
        payload = json.loads(response.data)
        self.assertEquals(payload['item_id'], 2)
        self.assertEquals(payload['user_id'], 3)
        self.assertEquals(payload['amount'], 500.00)
        self.assertEquals(payload['winner'], True)

    def test_sad_path_for_update_bid(self):
        response = self.test_app.put(
            '/bids/1111',
            json={
                'item_id': 2,
                'user_id': 3,
                'amount': 500.00
            },
            follow_redirects=True
        )

        self.assertEquals(response.status, "404 NOT FOUND")

    def test_delete_bid(self):
        response = self.test_app.get(
            '/bids',
            follow_redirects=True
        )

        self.assertEquals(response.status, "200 OK")
        payload = json.loads(response.data)
        self.assertEquals(payload['count'], 2)

        response = self.test_app.delete(
            '/bids/2',
            follow_redirects=True
        )

        self.assertEquals(response.status, "200 OK")
        payload = json.loads(response.data)
        self.assertEquals(payload['id'], 2)

        response = self.test_app.get(
            '/bids',
            follow_redirects=True
        )

        self.assertEquals(response.status, "200 OK")
        payload = json.loads(response.data)
        self.assertEquals(payload['count'], 1)

    def test_sad_path_for_delete_item(self):
        response = self.test_app.delete(
            '/bids/11111',
            follow_redirects=True
        )

        self.assertEquals(response.status, "404 NOT FOUND")


if __name__ == "__main__":
    unittest.main()

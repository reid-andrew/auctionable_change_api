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

    def test_get_all_bid_winners(self):
        response = self.test_app.get(
            '/bids/winners',
            follow_redirects=True
        )

        self.assertEquals(response.status, "200 OK")
        payload = json.loads(response.data)
        self.assertEquals(payload['count'], 0)

        response = self.test_app.put(
            '/bids/1',
            json={
                'winner': True
            },
            follow_redirects=True
        )

        response = self.test_app.get(
            '/bids/winners',
            follow_redirects=True
        )

        self.assertEquals(response.status, "200 OK")
        payload = json.loads(response.data)
        self.assertEquals(payload['count'], 1)
        self.assertEquals(payload['bids'][0]['item_id'], 1)
        self.assertEquals(payload['bids'][0]['user_id'], 2)

if __name__ == "__main__":
    unittest.main()

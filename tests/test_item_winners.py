import unittest
import json
from application import create_app, db
from application.models.item import Item
from application.models.user import User
from application.models.bid import Bid
from datetime import datetime
from math import trunc


class TestItems(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.test_app = self.app.test_client()
        with self.app.app_context():
            db.create_all()

        user = User(
            first_name="Jimmy",
            last_name="Cocopuff",
            email="jc@example.com",
            password="12345"
        )
        with self.app.app_context():
            db.session.add(user)
            db.session.commit()

        user = User(
            first_name="Jimmy",
            last_name="Cocobeans",
            email="jb@example.com",
            password="12345"
        )
        with self.app.app_context():
            db.session.add(user)
            db.session.commit()

        user = User(
            first_name="Jimmy",
            last_name="Jimmy",
            email="jj@example.com",
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
            auction_end=trunc(datetime.now().timestamp()) - 5
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
          auction_end=trunc(datetime.now().timestamp()) - 5
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
            amount=350.00
          )
        with self.app.app_context():
            db.session.add(bid)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_winners_are_declared(self):
        response = self.test_app.get(
            '/items/available',
            follow_redirects=True
        )

        self.assertEquals(response.status, "200 OK")
        payload = json.loads(response.data)
        self.assertEquals(payload['count'], 2)

        response = self.test_app.get(
            '/items/pending',
            follow_redirects=True
        )

        self.assertEquals(response.status, "200 OK")
        payload = json.loads(response.data)
        self.assertEquals(payload['count'], 0)

        response = self.test_app.post(
            '/items/winners',
            follow_redirects=True
        )

        self.assertEquals(response.status, "200 OK")

        response = self.test_app.get(
            '/items/available',
            follow_redirects=True
        )

        self.assertEquals(response.status, "200 OK")
        payload = json.loads(response.data)
        self.assertEquals(payload['count'], 1)

        response = self.test_app.get(
            '/items/pending',
            follow_redirects=True
        )

        self.assertEquals(response.status, "200 OK")
        payload = json.loads(response.data)
        self.assertEquals(payload['count'], 1)
        self.assertEquals(payload['items'][0]['bids'][0]['winner'], False)
        self.assertEquals(payload['items'][0]['bids'][-1]['winner'], True)

    def test_no_pending_winners_is_handled(self):
        response = self.test_app.post(
            '/items/winners',
            follow_redirects=True
        )

        self.assertEquals(response.status, "200 OK")

        response = self.test_app.post(
            '/items/winners',
            follow_redirects=True
        )

        self.assertEquals(response.status, "404 NOT FOUND")

    def test_no_bids_above_price_reschedules_election(self):
        response = self.test_app.put(
            '/bids/1',
            json={
                'amount': 1.00
            },
            follow_redirects=True
        )

        response = self.test_app.put(
            '/bids/2',
            json={
                'amount': 1.00
            },
            follow_redirects=True
        )

        response = self.test_app.post(
            '/items/winners',
            follow_redirects=True
        )

        self.assertEquals(response.status, "404 NOT FOUND")

        response = self.test_app.get(
            '/items/available',
            follow_redirects=True
        )

        self.assertEquals(response.status, "200 OK")
        payload = json.loads(response.data)
        self.assertEquals(payload['count'], 2)

        response = self.test_app.get(
            '/items/pending',
            follow_redirects=True
        )

        self.assertEquals(response.status, "200 OK")
        payload = json.loads(response.data)
        self.assertEquals(payload['count'], 0)        

if __name__ == "__main__":
    unittest.main()

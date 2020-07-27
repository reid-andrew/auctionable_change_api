import unittest
import json
from application import create_app, db
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

        item = Item(
          description="Vintage wood rocking chair",
          donor="Demo McDemoFace",
          donor_email="demomcdemoface@example.com",
          price=40.00,
          title="Rocking Chair",
          category='furniture',
          charity='Big Cat Rescue',
          charity_url="http://www.thisisatotallyligiturl.com",
          charity_score=4,
          image='img.ul'
          )
        with self.app.app_context():
            db.session.add(item)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_all_items(self):
        response = self.test_app.get(
            '/items',
            follow_redirects=True
        )

        self.assertEquals(response.status, "200 OK")
        payload = json.loads(response.data)
        self.assertEquals(payload['count'], 2)
        self.assertEquals(payload['items'][0]['title'], 'Tea Set')
        self.assertEquals(payload['items'][0]['charity'], 'Big Cat Rescue')
        self.assertEquals(payload['items'][-1]['donor'], 'Demo McDemoFace')
        self.assertEquals(payload['items'][-1]['price'], 40.00)
        self.assertEquals(payload['items'][-1]['status'], 'available')


    def test_get_one_item(self):
        response = self.test_app.get(
            '/items/2',
            follow_redirects=True
        )

        self.assertEquals(response.status, "200 OK")
        payload = json.loads(response.data)
        self.assertEquals(payload['id'], 2)
        self.assertEquals(payload['title'], 'Rocking Chair')
        self.assertNotEqual(payload['title'], 'Antique Tea set')

    def test_sad_path_for_nonexistent_item(self):
        response = self.test_app.get(
            '/items/10',
            follow_redirects=True
        )

        self.assertEquals(response.status, "404 NOT FOUND")

    def test_create_items(self):
        response = self.test_app.post(
            '/items',
            json={
                'description': '12 inch tablet from Samsung',
                'donor': 'Demo McDemoFace',
                'donor_email': "demomcdemoface@example.com",
                'id': 2,
                'price': 56.00,
                'status': 'For Sale',
                'title': 'Android Tablet',
                'category': 'electronics',
                'charity': 'Big Cat Rescue',
                'charity_url': "http://www.thisisatotallyligiturl.com",
                'charity_score': 4,
                'image': 'img.ul'
            },
            follow_redirects=True
        )

        self.assertEquals(response.status, "200 OK")
        payload = json.loads(response.data)
        self.assertEquals(payload['title'], 'Android Tablet')
        self.assertEquals(payload['charity'], 'Big Cat Rescue')

    def test_sad_path_for_create_item_with_missing_info(self):
        try:
            response = self.test_app.post(
                '/items',
                json={
                    'description': '12 inch tablet from Samsung',
                    'donor': 'Demo McDemoFace',
                    'donor_email': "demomcdemoface@example.com",
                    'id': 2,
                    'price': 56.00,
                    'category': 'electronics',
                    'charity': 'Big Cat Rescue',
                    'charity_url': "http://www.thisisatotallyligiturl.com",
                    'charity_score': 4,
                    'image': 'img.ul'
                },
                follow_redirects=True
            )
        except Exception as e:
            return (str(e))

        self.assertEquals(response.status, "400 BAD REQUEST")

    def test_update_items(self):
        response = self.test_app.put(
            '/items/1',
            json={
                'description': 'Updated Item',
                'donor': 'New Donor'
            },
            follow_redirects=True
        )

        self.assertEquals(response.status, "200 OK")
        payload = json.loads(response.data)
        self.assertEquals(payload['description'], 'Updated Item')
        self.assertEquals(payload['donor'], 'New Donor')
        self.assertEquals(payload['category'], 'furniture')
        self.assertEquals(payload['charity'], 'Big Cat Rescue')

        def test_update_items(self):
            response = self.test_app.put(
                '/items/1111',
                json={
                    'description': 'Updated Item',
                    'donor': 'New Donor'
                },
                follow_redirects=True
            )

            self.assertEquals(response.status, "400 BAD REQUEST")
            
if __name__ == "__main__":
    unittest.main()

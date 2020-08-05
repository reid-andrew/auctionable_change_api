import unittest
import json
from application import create_app, db
from application.models.item import Item
from application.models.user import User



class TestUsers(unittest.TestCase):
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
                'user_id': 1,
                'title': 'Android Tablet',
                'description': '12 inch tablet from Samsung',
                'price': 56.00,
                'category': 'electronics',
                'charity': 'Big Cat Rescue',
                'charity_url': "http://www.thisisatotallyligiturl.com",
                'charity_score': 4,
                'charity_score_image': "https://d20umu42aunjpx.cloudfront.net/_gfx_/icons/stars/4stars.png",
                'image': 'img.ul'
            },
            follow_redirects=True
        )

        self.assertEquals(response.status, "200 OK")
        payload = json.loads(response.data)
        self.assertEquals(payload['title'], 'Android Tablet')
        self.assertEquals(payload['charity'], 'Big Cat Rescue')

    def test_sad_path_for_create_item_with_missing_info(self):
        response = self.test_app.post(
            '/items',
            json={
                'user_id': 1,
                'description': '12 inch tablet from Samsung',
                'price': 56.00,
                'category': 'electronics',
                'charity': 'Big Cat Rescue',
                'charity_url': "http://www.thisisatotallyligiturl.com",
                'charity_score': 4,
                'charity_score_image': "https://d20umu42aunjpx.cloudfront.net/_gfx_/icons/stars/4stars.png",
                'image': 'img.ul'
            },
            follow_redirects=True
        )

        self.assertEquals(response.status, "400 BAD REQUEST")

    def test_update_items_only_updates_selected_fields(self):
        response = self.test_app.put(
            '/items/1',
            json={
                'description': 'Updated Item',
                'price': 1999.88
            },
            follow_redirects=True
        )

        self.assertEquals(response.status, "200 OK")
        payload = json.loads(response.data)
        self.assertEquals(payload['description'], 'Updated Item')
        self.assertEquals(payload['price'], 1999.88)
        self.assertEquals(payload['category'], 'furniture')
        self.assertEquals(payload['charity'], 'Big Cat Rescue')

    def test_update_can_update_all_fields(self):
        response = self.test_app.put(
            '/items/1',
            json={
                'user_id': 2,
                'title': 'Updated Title',
                'description': 'Updated Item',
                'price': 9999.99,
                'status': 'sold',
                'category': 'New Category',
                'charity': 'New Charity',
                'charity_url': 'www.newcharity.org',
                'charity_score': 1,
                'charity_score_image': 'www.newimage.com',
                'image': 'www.newimage.com'
            },
            follow_redirects=True
        )

        self.assertEquals(response.status, "200 OK")
        payload = json.loads(response.data)
        self.assertEquals(payload['user_id'], 2)
        self.assertEquals(payload['title'], 'Updated Title')
        self.assertEquals(payload['description'], 'Updated Item')
        self.assertEquals(payload['price'], 9999.99)
        self.assertEquals(payload['status'], 'sold')
        self.assertEquals(payload['category'], 'New Category')
        self.assertEquals(payload['charity'], 'New Charity')
        self.assertEquals(payload['charity_url'], 'www.newcharity.org')
        self.assertEquals(payload['charity_score'], 1)
        self.assertEquals(payload['charity_score_image'], 'www.newimage.com')
        self.assertEquals(payload['image'], 'www.newimage.com')

    def test_sad_path_for_update_item(self):
        response = self.test_app.put(
            '/items/1111',
            json={
                'description': 'Updated Item',
                'charity': 'New New Charity'
            },
            follow_redirects=True
        )

        self.assertEquals(response.status, "404 NOT FOUND")

    def test_delete_item(self):
        response = self.test_app.get(
            '/items',
            follow_redirects=True
        )

        self.assertEquals(response.status, "200 OK")
        payload = json.loads(response.data)
        self.assertEquals(payload['count'], 2)

        response = self.test_app.delete(
            '/items/2',
            follow_redirects=True
        )

        self.assertEquals(response.status, "200 OK")
        payload = json.loads(response.data)
        self.assertEquals(payload['id'], 2)

        response = self.test_app.get(
            '/items',
            follow_redirects=True
        )

        self.assertEquals(response.status, "200 OK")
        payload = json.loads(response.data)
        self.assertEquals(payload['count'], 1)

    def test_sad_path_for_delete_item(self):
        response = self.test_app.delete(
            '/items/11111',
            follow_redirects=True
        )

        self.assertEquals(response.status, "404 NOT FOUND")


if __name__ == "__main__":
    unittest.main()

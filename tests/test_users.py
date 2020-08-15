import unittest
import json
from application import create_app, db
from application.models.user import User


class TestUsers(unittest.TestCase):
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

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_all_users(self):
        response = self.test_app.get(
            '/users',
            follow_redirects=True
        )

        self.assertEquals(response.status, "200 OK")
        payload = json.loads(response.data)
        self.assertEquals(payload['count'], 2)
        self.assertEquals(payload['users'][0]['first_name'], 'Johnny')
        self.assertEquals(payload['users'][0]['email'], 'jm@example.com')
        self.assertEquals(payload['users'][-1]['last_name'], 'De Los Buyingstuff')
        self.assertEquals(payload['users'][-1]['id'], 2)

    def test_get_one_user(self):
        response = self.test_app.get(
            '/users/1',
            follow_redirects=True
        )

        self.assertEquals(response.status, "200 OK")
        payload = json.loads(response.data)
        self.assertEquals(payload['id'], 1)
        self.assertEquals(payload['first_name'], 'Johnny')
        self.assertEquals(payload['email'], 'jm@example.com')

    def test_sad_path_for_nonexistent_user(self):
        response = self.test_app.get(
            '/users/11111',
            follow_redirects=True
        )

        self.assertEquals(response.status, "404 NOT FOUND")

    def test_create_users(self):
        response = self.test_app.post(
            '/users',
            json={
                'first_name': 'Joe',
                'last_name': 'Strummer',
                'email': 'clash@punk.rock',
                'password': 'Lond0n(alling'
            },
            follow_redirects=True
        )

        self.assertEquals(response.status, "200 OK")
        payload = json.loads(response.data)
        self.assertEquals(payload['first_name'], 'Joe')
        self.assertEquals(payload['last_name'], 'Strummer')

    def test_sad_path_for_create_item_with_missing_info(self):
        response = self.test_app.post(
            '/users',
            json={
                'first_name': 'Joe',
                'email': 'clash@punk.rock',
                'password': 'Lond0n(alling'
            },
            follow_redirects=True
        )

        self.assertEquals(response.status, "400 BAD REQUEST")

    def test_update_items_only_updates_selected_fields(self):
        response = self.test_app.put(
            '/users/1',
            json={
                'first_name': 'Mick'
            },
            follow_redirects=True
        )

        self.assertEquals(response.status, "200 OK")
        payload = json.loads(response.data)
        self.assertEquals(payload['first_name'], 'Mick')
        self.assertEquals(payload['last_name'], 'McSellingstuff')

    def test_update_can_update_all_fields(self):
        response = self.test_app.put(
            '/users/2',
            json={
                'first_name': 'Joe',
                'last_name': 'Strummer',
                'email': 'clash@punk.rock',
                'password': 'Lond0n(alling'
            },
            follow_redirects=True
        )

        self.assertEquals(response.status, "200 OK")
        payload = json.loads(response.data)
        self.assertEquals(payload['first_name'], 'Joe')
        self.assertEquals(payload['last_name'], 'Strummer')
        self.assertEquals(payload['email'], 'clash@punk.rock')

    def test_sad_path_for_update_user(self):
        response = self.test_app.put(
            '/users/999',
            json={
                'first_name': 'Joe',
                'last_name': 'Strummer'
            },
            follow_redirects=True
        )

        self.assertEquals(response.status, "404 NOT FOUND")

    def test_delete_user(self):
        response = self.test_app.get(
            '/users',
            follow_redirects=True
        )

        self.assertEquals(response.status, "200 OK")
        payload = json.loads(response.data)
        self.assertEquals(payload['count'], 2)

        response = self.test_app.delete(
            '/users/1',
            follow_redirects=True
        )
        self.assertEquals(response.status, "200 OK")

        response = self.test_app.get(
            '/users',
            follow_redirects=True
        )

        self.assertEquals(response.status, "200 OK")
        payload = json.loads(response.data)
        self.assertEquals(payload['count'], 1)

    def test_sad_path_for_delete_user(self):
        response = self.test_app.delete(
            '/users/8888',
            follow_redirects=True
        )

        self.assertEquals(response.status, "404 NOT FOUND")

if __name__ == "__main__":
    unittest.main()

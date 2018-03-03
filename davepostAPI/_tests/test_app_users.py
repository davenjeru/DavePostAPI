from flask_testing import TestCase

from davepostAPI import app
from davepostAPI.api.v1 import api_v1
from davepostAPI.api.v1.auth import Login
from davepostAPI.api.v1.users import AllUsers, SingleUser, SingleUserAllPosts


class AppTestCase(TestCase):
    def create_app(self):
        app.testing = True
        return app

    def setUp(self):
        self.client = self.create_app().test_client()

    def tearDown(self):
        pass

    def test_c1_view_all_users(self):
        rv = self.client.get(api_v1.url_for(AllUsers))
        self.assert200(rv)
        self.assertIn(b'{"users": [', rv.data)

    def test_c2_view_single_user(self):
        rv = self.client.get(api_v1.url_for(SingleUser, user_id=1))
        self.assert200(rv)
        self.assertIn(b'{"user":', rv.data)
        self.assertIn(b'"email":', rv.data)
        self.assertIn(b'"url":', rv.data)

    def test_c3_view_user_posts_empty(self):
        rv = self.client.get(api_v1.url_for(SingleUserAllPosts, user_id=1))
        self.assert200(rv)
        self.assertIn(b'"posts": []', rv.data)

    def test_c4_delete_user(self):
        rv = self.client.delete(api_v1.url_for(SingleUser, user_id=1))
        self.assert401(rv)
        data = dict(email='email@company.com', password='password.Pa55word')
        self.client.post(api_v1.url_for(Login), data=str(data), content_type='application/json')
        rv = self.client.delete(api_v1.url_for(SingleUser, user_id=1))
        self.assertEqual(204, rv.status_code)

    def test_c5_view_all_users_empty(self):
        rv = self.client.get(api_v1.url_for(AllUsers))
        self.assert200(rv)
        self.assertIn(b'{"users": []', rv.data)

    def test_c6_view_single_user_fail(self):
        rv = self.client.get(api_v1.url_for(SingleUser, user_id=1))
        self.assert400(rv)
        self.assertIn(b'User not found!', rv.data)

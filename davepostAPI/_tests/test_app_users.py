from flask_testing import TestCase

from davepostAPI import app
from davepostAPI.api.v1 import api_v1
from davepostAPI.api.v1.users import AllUsers, SingleUser


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

    def test_c2_view_single_user_(self):
        rv = self.client.get(api_v1.url_for(SingleUser, user_id=1))
        self.assert200(rv)
        self.assertIn(b'{"user":', rv.data)
        self.assertIn(b'"email":', rv.data)
        self.assertIn(b'"url":', rv.data)

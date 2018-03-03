from flask_testing import TestCase

from davepostAPI import app
from davepostAPI.api.v1 import api_v1
from davepostAPI.api.v1.posts import AllPosts, SinglePost


class AppTestCase(TestCase):
    def create_app(self):
        app.testing = True
        return app

    def setUp(self):
        self.client = self.create_app().test_client()

    def tearDown(self):
        pass

    def test_b1_view_all_posts(self):
        rv = self.client.get(api_v1.url_for(AllPosts))
        self.assert200(rv)
        self.assertIn(b'[]', rv.data)

    def test_b2_view_single_post_fail(self):
        rv = self.client.get(api_v1.url_for(SinglePost, post_id=1))
        self.assert400(rv)
        self.assertIn(b'Post not found!', rv.data)

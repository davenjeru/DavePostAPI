from flask_restplus import Resource
from flask_restplus.namespace import Namespace

posts_ns = Namespace('posts')


class AllPosts(Resource):
    def get(self):
        """
        View all posts
        :return: a list of all posts under 'posts'

        :rtype dict

        """
        pass

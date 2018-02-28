from flask_restplus import Resource
from flask_restplus.namespace import Namespace

posts_ns = Namespace('posts')


class SinglePost(Resource):
    @posts_ns.response(200, "Success")
    @posts_ns.response(400, "Post not found. Invalid 'post_id' provided")
    def get(self, post_id: int):
        """
        View a single post
        """
        pass

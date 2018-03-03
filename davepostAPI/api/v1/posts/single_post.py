from flask_restplus import Resource
from flask_restplus.namespace import Namespace

from davepostAPI.api.v1.boilerplate import check_id_availability, safe_post_output
from davepostAPI.models import posts_list

posts_ns = Namespace('posts')


class SinglePost(Resource):
    @posts_ns.response(200, "Success")
    @posts_ns.response(400, "Post not found. Invalid 'post_id' provided")
    def get(self, post_id: int):
        """
        View a single post
        """
        return dict(post=safe_post_output(self, check_id_availability(post_id, posts_list, 'post')))

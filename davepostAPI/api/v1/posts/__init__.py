from flask_restplus.namespace import Namespace

from davepostAPI.api.v1.posts.all_posts import AllPosts
from davepostAPI.api.v1.posts.single_post import SinglePost

posts_ns = Namespace('posts', description='Operations on posts only')

posts_ns.add_resource(AllPosts, '/')
posts_ns.add_resource(SinglePost, '/<int:post_id>')

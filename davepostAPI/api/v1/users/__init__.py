from flask_restplus.namespace import Namespace

from davepostAPI.api.v1.users.all_users import AllUsers
from davepostAPI.api.v1.users.single_user import SingleUser
from davepostAPI.api.v1.users.single_user_all_posts import SingleUserAllPosts
from davepostAPI.api.v1.users.single_user_single_post import SingleUserSinglePost

users_ns = Namespace('users', description='Operations related to users')

users_ns.add_resource(AllUsers, '/')

users_ns.add_resource(SingleUser, '/<int:user_id>')

users_ns.add_resource(SingleUserAllPosts, '/<int:user_id>/posts')

users_ns.add_resource(SingleUserSinglePost, '/<int:user_id>/posts/<int:post_id>')

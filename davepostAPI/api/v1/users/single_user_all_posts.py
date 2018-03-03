from flask_restplus import Resource
from flask_restplus.namespace import Namespace

from davepostAPI.api.v1.boilerplate import check_id_availability, PayloadExtractionError
from davepostAPI.models import users_list, User

users_ns = Namespace('users')


class SingleUserAllPosts(Resource):
    @users_ns.response(200, "Success")
    @users_ns.response(400, "Post not found. Invalid 'post_id' provided")
    def get(self, user_id: int):
        """
        View all posts from a single user
        """
        this_user = None
        try:
            this_user = check_id_availability(user_id, users_list, str(User.__name__))
        except PayloadExtractionError as e:
            users_ns.abort(e.abort_code, e.msg)
        my_posts_list = this_user.get_my_posts()
        my_posts_list_output = []
        for a_post in my_posts_list:
            my_posts_list_output.append(a_post.serialize)
        return dict(posts=my_posts_list_output)

    @users_ns.response(201, 'Post created successfully')
    @users_ns.response(400, 'Bad request')
    @users_ns.response(401, 'Not logged in hence unauthorized')
    @users_ns.response(403, 'Logged in but forbidden from performing this action')
    def post(self, user_id: int):
        """
        Add a post

        1. User must be logged in to create a post
        2. Your title should have between 10 and 70 characters
        3. Your body should have between 40 and 500 characters
        4. Duplicate posts will not be created

        """
        pass

    @users_ns.response(204, 'Post deleted successfully')
    @users_ns.response(400, 'Bad request')
    @users_ns.response(401, 'Not logged in hence unauthorized')
    @users_ns.response(403, 'Logged in but forbidden from performing this action')
    def delete(self, user_id: int):
        """
        Batch delete all user's posts

        1. User must be logged in to delete all their posts
        2. This deletes all posts that a user has created
        3. This process os of course irreversible
        """
        pass

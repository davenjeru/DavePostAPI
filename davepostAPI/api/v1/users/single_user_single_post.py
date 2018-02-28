from flask_restplus import Resource
from flask_restplus.namespace import Namespace

users_ns = Namespace('users')


class SingleUserSinglePost(Resource):
    def get(self, user_id: int, post_id: int):
        """
        View a single post from a specific user
        """
        pass

    @users_ns.response(200, 'Post modified successfully')
    @users_ns.response(400, 'Bad request')
    @users_ns.response(401, 'Not logged in hence unauthorized')
    @users_ns.response(403, 'Logged in but forbidden from performing this action')
    def patch(self, user_id: int, post_id: int):
        """
        Modify a post

        1. User should be logged in.
        2. Your title should have between 10 and 70 characters
        3. Your body should have between 40 and 500 characters
        4. Duplicate posts will not be created
        """
        pass

    @users_ns.response(204, 'Post deleted successfully')
    @users_ns.response(400, 'Bad request')
    @users_ns.response(401, 'Not logged in hence unauthorized')
    @users_ns.response(403, 'Logged in but forbidden from performing this action')
    def delete(self, user_id: int, post_id: int):
        """
        Delete a post

        1. User needs to be logged in
        2. This deletes the post whose ID is specified on the url
        3. This process is irreversible
        """
        pass

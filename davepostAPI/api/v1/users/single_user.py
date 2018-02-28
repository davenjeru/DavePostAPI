from flask_restplus import Resource
from flask_restplus.namespace import Namespace

users_ns = Namespace('users')


class SingleUser(Resource):
    def get(self, user_id: int):
        """
        View a single user
        """
        pass

    @users_ns.response(204, 'User has been deleted successfully')
    @users_ns.response(401, 'Not logged in hence unauthorized')
    @users_ns.response(403, 'Logged in but not allowed to perform this action on the current url')
    def delete(self, user_id: int):
        """
        Delete a user account

        1. This deletes a user account. However it does not delete their posts.
        Their posts remain and would no longer be editable or deletable.
        2. The user must be logged into their account in order for them to delete it.
        3. After deletion, the user will be logged out
        4. If the user re-registers, a new ID will be given to them, hence they are unable to access their previous posts
        5. This process is indeed irreversible
        """
        pass
